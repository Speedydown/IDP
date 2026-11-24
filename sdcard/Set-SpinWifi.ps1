<#
.SYNOPSIS
  Changes the WiFi network of an already prepared spin SD card (card in a reader,
  local or on a remote PC via PS Remoting).

  - firstrun.sh still on the card (Pi never booted it): patches SSID/password in it.
  - firstrun.sh already ran: drops wifi-fix.sh on the boot partition and hooks it
    into cmdline.txt; it runs once on the next boot, sets the WiFi and removes itself.

  NB: the Edimax EW-7811Un is 2.4 GHz only - use the 2.4 GHz SSID of the router.

.EXAMPLE
  .\Set-SpinWifi.ps1 -DiskNumber 1 -WifiSsid 'MijnWifi-2.4GHz' -WifiPassword '...'   # card in this laptop
.EXAMPLE
  .\Set-SpinWifi.ps1 -ComputerName server -DiskNumber 2 -WifiSsid 'MijnWifi-2.4GHz' -WifiPassword '...'
#>
param(
    [string]$ComputerName = 'localhost',
    [Parameter(Mandatory)][int]$DiskNumber,
    [Parameter(Mandatory)][string]$WifiSsid,
    [Parameter(Mandatory)][string]$WifiPassword,
    [string]$Country = 'NL'
)
$ErrorActionPreference = 'Stop'
function Esc([string]$s) { $s.Replace("'", "'\''") }

$fix = @"
#!/bin/bash
# spInOS: one-shot WiFi change, removes itself
set +e
BOOT=/boot/firmware; [ -f "`$BOOT/cmdline.txt" ] || BOOT=/boot
/usr/lib/raspberrypi-sys-mods/imager_custom set_wlan '$(Esc $WifiSsid)' '$(Esc $WifiPassword)' '$Country'
rm -f "`$BOOT/wifi-fix.sh"
sed -i 's| systemd.run.*||g' "`$BOOT/cmdline.txt"
exit 0
"@.Replace("`r`n", "`n")

$work = {
    param($n, $ssid, $pass, $fix)
    $ErrorActionPreference = 'Stop'
    function Esc([string]$s) { $s.Replace("'", "'\''") }
    try { Update-HostStorageCache } catch {}
    $d = Get-Disk -Number $n
    if ($d.Size -eq 0) { throw "No card in disk $n" }
    $p = Get-Partition -DiskNumber $n -PartitionNumber 1
    if (-not $p.DriveLetter -or $p.DriveLetter -eq [char]0) { $p | Add-PartitionAccessPath -AssignDriveLetter; Start-Sleep 2; $p = Get-Partition -DiskNumber $n -PartitionNumber 1 }
    $l = $p.DriveLetter
    if (-not (Test-Path "${l}:\cmdline.txt")) { throw "${l}: is not a Raspberry Pi boot partition" }

    if (Test-Path "${l}:\firstrun.sh") {
        $t = [IO.File]::ReadAllText("${l}:\firstrun.sh")
        $t = [regex]::Replace($t, "(?m)^WIFI_SSID=.*$", "WIFI_SSID='$(Esc $ssid)'")
        $t = [regex]::Replace($t, "(?m)^WIFI_PASS=.*$", "WIFI_PASS='$(Esc $pass)'")
        [IO.File]::WriteAllText("${l}:\firstrun.sh", $t.Replace("`r`n", "`n"))
        "firstrun.sh had not run yet - patched SSID in it"
    } else {
        [IO.File]::WriteAllText("${l}:\wifi-fix.sh", $fix)
        $cmd = (Get-Content "${l}:\cmdline.txt" -Raw).Trim() -replace ' systemd\.run.*$', ''
        $cmd += ' systemd.run=/boot/firmware/wifi-fix.sh systemd.run_success_action=reboot systemd.unit=kernel-command-line.target'
        [IO.File]::WriteAllText("${l}:\cmdline.txt", $cmd + "`n")
        "firstrun.sh already ran (Pi did boot) - wifi-fix.sh installed for next boot"
        if (Test-Path "${l}:\spin\INSTALLED.txt") { "INSTALLED.txt: " + (Get-Content "${l}:\spin\INSTALLED.txt") }
    }
    "cmdline.txt: " + (Get-Content "${l}:\cmdline.txt" -Raw).Trim()
    try { Write-VolumeCache -DriveLetter $l } catch {}
    # only release the letter where we may (remote admin session); locally just eject via Explorer
    try { Get-Partition -DriveLetter $l | Remove-PartitionAccessPath -AccessPath "${l}:\" -ErrorAction Stop; "card ready - safe to remove" } catch { "card ready - eject ${l}: in Explorer, then remove it" }
}

if ($ComputerName -in 'localhost', '.', $env:COMPUTERNAME) {
    & $work $DiskNumber $WifiSsid $WifiPassword $fix
} else {
    Invoke-Command -ComputerName $ComputerName -ArgumentList $DiskNumber, $WifiSsid, $WifiPassword, $fix -ScriptBlock $work
}
