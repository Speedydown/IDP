<#
.SYNOPSIS
  Writes Raspberry Pi OS Lite to an SD card (local or on a remote PC via PS Remoting),
  verifies it by reading it back, and installs the spInOS first-boot payload.

.EXAMPLE
  .\Write-SpinSdCard.ps1 -ComputerName server -DiskNumber 2 `
      -ImagePath D:\spin-sd\2026-10-06-raspios-bookworm-armhf-lite.img `
      -ExpectedSha256 340d17e344724aebe42f5ca7d16fa569d99a64ceb9304942b551defed4edc4b9 `
      -WifiSsid 'MyWifi' -WifiPassword 'secret' -UserPassword 'kies-een-wachtwoord'

  -ImagePath is a path on the machine that has the card reader (decompressed .img).
  Needs admin rights there (a PS Remoting session is elevated by default).
#>
param(
    [string]$ComputerName = 'localhost',
    [Parameter(Mandatory)][int]$DiskNumber,
    [Parameter(Mandatory)][string]$ImagePath,
    [string]$ExpectedSha256,
    [string]$WifiSsid = '',
    [string]$WifiPassword = '',
    [Parameter(Mandatory)][string]$UserPassword,   # password for user 'pi'
    [switch]$SkipWrite
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$session = New-PSSession -ComputerName $ComputerName

try {
    # ---- 1. write + verify --------------------------------------------------
    if (-not $SkipWrite) {
        Invoke-Command -Session $session -ArgumentList $DiskNumber, $ImagePath, $ExpectedSha256 -ScriptBlock {
            param($n, $img, $expected)
            $ErrorActionPreference = 'Stop'
            $d = Get-Disk -Number $n
            if ($d.IsSystem -or $d.IsBoot -or $d.BusType -notin 'USB', 'SD', 'MMC' -or $d.Size -lt 4GB -or $d.Size -gt 128GB) {
                throw "Disk $n ($($d.FriendlyName), $($d.BusType), $($d.Size) bytes) does not look like an SD card - refusing."
            }
            Clear-Disk -Number $n -RemoveData -RemoveOEM -Confirm:$false
            Start-Sleep 2
            [long]$len = (Get-Item $img).Length
            $buf = New-Object byte[] (1MB)
            $sw = [Diagnostics.Stopwatch]::StartNew()
            $src = [IO.File]::OpenRead($img)
            $dst = New-Object IO.FileStream("\\.\PhysicalDrive$n", [IO.FileMode]::Open, [IO.FileAccess]::ReadWrite, [IO.FileShare]::ReadWrite, 4096, [IO.FileOptions]::WriteThrough)
            try { while (($r = $src.Read($buf, 0, $buf.Length)) -gt 0) { $dst.Write($buf, 0, $r) }; $dst.Flush() }
            finally { $dst.Close(); $src.Close() }
            "written $len bytes in $([int]$sw.Elapsed.TotalSeconds)s"

            $sw.Restart()
            $rd = New-Object IO.FileStream("\\.\PhysicalDrive$n", [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
            $sha = [Security.Cryptography.SHA256]::Create(); [long]$left = $len
            try { while ($left -gt 0) { $r = $rd.Read($buf, 0, [int][Math]::Min([long]$buf.Length, $left)); if ($r -le 0) { break }; [void]$sha.TransformBlock($buf, 0, $r, $null, 0); $left -= $r } }
            finally { $rd.Close() }
            [void]$sha.TransformFinalBlock((New-Object byte[] 0), 0, 0)
            $got = [BitConverter]::ToString($sha.Hash).Replace('-', '').ToLower()
            "read back in $([int]$sw.Elapsed.TotalSeconds)s, sha256 $got"
            if ($expected -and $got -ne $expected.ToLower()) { throw "VERIFY FAILED: card content differs from the image - the card is probably bad." }
            Update-Disk -Number $n
        }
    }

    # ---- 2. mount boot partition ---------------------------------------------
    $letter = Invoke-Command -Session $session -ArgumentList $DiskNumber -ScriptBlock {
        param($n)
        Update-Disk -Number $n; Start-Sleep 3
        $p = Get-Partition -DiskNumber $n -PartitionNumber 1
        if (-not $p.DriveLetter -or $p.DriveLetter -eq [char]0) { $p | Add-PartitionAccessPath -AssignDriveLetter; Start-Sleep 2; $p = Get-Partition -DiskNumber $n -PartitionNumber 1 }
        if (-not (Test-Path "$($p.DriveLetter):\cmdline.txt")) { throw "No cmdline.txt on $($p.DriveLetter): - not a Raspberry Pi OS boot partition" }
        [string]$p.DriveLetter
    }
    "boot partition on ${ComputerName}: ${letter}:"

    # ---- 3. build payload locally --------------------------------------------
    $tmp = Join-Path ([IO.Path]::GetTempPath()) ("spin-payload-" + [guid]::NewGuid())
    New-Item -ItemType Directory -Force "$tmp\spin\IDPSpin" | Out-Null
    $openssl = (Get-Command openssl -ErrorAction SilentlyContinue).Source
    if (-not $openssl) { $openssl = 'C:\Program Files\Git\usr\bin\openssl.exe' }
    $hash = (& $openssl passwd -6 $UserPassword).Trim()
    function Esc([string]$s) { $s.Replace("'", "'\''") }
    $fr = [IO.File]::ReadAllText("$PSScriptRoot\firstrun.sh").Replace('__PASSHASH__', $hash)
    if ($WifiSsid) {
        $fr = $fr.Replace("WIFI_SSID='__WIFI_SSID__'", "WIFI_SSID='$(Esc $WifiSsid)'").Replace("WIFI_PASS='__WIFI_PASS__'", "WIFI_PASS='$(Esc $WifiPassword)'")
    }
    [IO.File]::WriteAllText("$tmp\firstrun.sh", $fr.Replace("`r`n", "`n"))
    foreach ($f in 'spin.service', 'spin-extras.service', 'spin-camera.service') { [IO.File]::WriteAllText("$tmp\spin\$f", [IO.File]::ReadAllText("$PSScriptRoot\$f").Replace("`r`n", "`n")) }
    Get-ChildItem "$repo\IDPSpin\*.py" | ForEach-Object { [IO.File]::WriteAllText("$tmp\spin\IDPSpin\$($_.Name)", [IO.File]::ReadAllText($_.FullName).Replace("`r`n", "`n")) }

    # ---- 4. copy payload + patch cmdline.txt / config.txt ---------------------
    Copy-Item -ToSession $session -Path "$tmp\firstrun.sh" -Destination "${letter}:\firstrun.sh" -Force
    Copy-Item -ToSession $session -Path "$tmp\spin" -Destination "${letter}:\" -Recurse -Force
    Remove-Item -Recurse -Force $tmp

    Invoke-Command -Session $session -ArgumentList $letter -ScriptBlock {
        param($l)
        $cmd = (Get-Content "${l}:\cmdline.txt" -Raw).Trim()
        if ($cmd -notmatch 'systemd\.run=') {
            $cmd += ' systemd.run=/boot/firmware/firstrun.sh systemd.run_success_action=reboot systemd.unit=kernel-command-line.target'
        }
        [IO.File]::WriteAllText("${l}:\cmdline.txt", $cmd + "`n")
        $cfg = Get-Content "${l}:\config.txt" -Raw
        if ($cfg -notmatch '(?m)^\s*dtparam=i2c_arm=on') {
            $cfg = $cfg.TrimEnd() + "`n`n# spInOS: servo boards + gyro (I2C), MCP3008 (SPI)`ndtparam=i2c_arm=on`ndtparam=spi=on`n"
        }
        [IO.File]::WriteAllText("${l}:\config.txt", $cfg.Replace("`r`n", "`n"))
        "cmdline.txt: " + (Get-Content "${l}:\cmdline.txt" -Raw).Trim()
        Get-ChildItem "${l}:\firstrun.sh", "${l}:\spin" | Select-Object Name, Length | Out-String
        (Get-ChildItem "${l}:\spin\IDPSpin").Count.ToString() + " python files"
        # flush + release the drive letter so the card can be pulled
        Write-VolumeCache -DriveLetter $l
        Get-Partition -DriveLetter $l | Remove-PartitionAccessPath -AccessPath "${l}:\"
        "card ready - safe to remove"
    }
}
finally {
    Remove-PSSession $session
}
