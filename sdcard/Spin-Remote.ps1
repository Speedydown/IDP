<#
.SYNOPSIS
  Minimal keyboard remote for the spider (spInOS, TCP 1337).

.EXAMPLE
  .\Spin-Remote.ps1                      # connects to spin.local
  .\Spin-Remote.ps1 -Address 192.168.1.123
  .\Spin-Remote.ps1 -Command 'ping'      # one command, print reply

  Keys:  hold W forward  S back  A left  D right  Q left-fwd  E right-fwd
         Z left-back  C right-back  (release = stop)   Space stop
         1..8 mode (1 walk, 3 spider gap, 4 dance, 5 balloon race, 8 dance 2)
         + / -  height up/down    H horn    L log    P ping    X quit
#>
param(
    [string]$Address = 'spin.local',
    [int]$Port = 1337,
    [string]$Command
)

$client = [System.Net.Sockets.TcpClient]::new()
$client.ReceiveTimeout = 15000
$client.Connect($Address, $Port)
$stream = $client.GetStream()
$enc = [System.Text.Encoding]::UTF8

function Send-Spin([string]$cmd) {
    $bytes = $enc.GetBytes("$cmd<EOF>")
    $stream.Write($bytes, 0, $bytes.Length)
    $sb = [System.Text.StringBuilder]::new()
    $buf = New-Object byte[] 65536
    while (-not $sb.ToString().Contains('<EOF>')) {
        $n = $stream.Read($buf, 0, $buf.Length)
        if ($n -le 0) { throw 'connection closed' }
        [void]$sb.Append($enc.GetString($buf, 0, $n))
    }
    $reply = $sb.ToString()
    return $reply.Substring(0, $reply.IndexOf('<EOF>'))
}

try {
    if ($Command) { Send-Spin $Command; return }

    Write-Host "Connected to $Address`:$Port - $(Send-Spin 'ping')"
    $height = 75
    $keys = @{
        'W' = 'move 11'; 'S' = 'move 15'; 'A' = 'move 17'; 'D' = 'move 13'
        'Q' = 'move 18'; 'E' = 'move 12'; 'Z' = 'move 16'; 'C' = 'move 14'
        'Spacebar' = 'move 10'; 'H' = 'horn'; 'L' = 'glog'; 'P' = 'ping'
    }
    # A console cannot see key-up. Hold-to-walk is emulated with the keyboard's
    # auto-repeat: a move is sent once, repeats of the same key are ignored, and
    # when the repeats stop (key released) the spider gets 'move 10'.
    $releaseMs = 700       # > Windows' initial key-repeat delay
    $moving = $null; $lastKey = [DateTime]::MinValue
    function Show($c) { Write-Host ("{0,-10} -> {1}" -f $c, (Send-Spin $c)) }
    while ($true) {
        if (-not [Console]::KeyAvailable) {
            if ($moving -and ((Get-Date) - $lastKey).TotalMilliseconds -gt $releaseMs) { Show 'move 10'; $moving = $null }
            Start-Sleep -Milliseconds 30
            continue
        }
        $k = [Console]::ReadKey($true)
        $name = $k.Key.ToString()
        $cmd = $null
        if ($name -eq 'X') { break }
        elseif ($keys.ContainsKey($name)) { $cmd = $keys[$name] }
        elseif ($k.KeyChar -match '^[1-8]$') { $cmd = "smde $($k.KeyChar)" }
        elseif ($k.KeyChar -eq '+') { $height = [Math]::Min(150, $height + 10); $cmd = 'shgt {0:000}' -f $height }
        elseif ($k.KeyChar -eq '-') { $height = [Math]::Max(40, $height - 10); $cmd = 'shgt {0:000}' -f $height }
        if (-not $cmd) { continue }
        if ($cmd -like 'move 1[1-8]') {
            $lastKey = Get-Date
            if ($cmd -eq $moving) { continue }   # auto-repeat of the held key
            $moving = $cmd
        } elseif ($cmd -eq 'move 10') { $moving = $null }
        Show $cmd
    }
}
finally {
    try { Send-Spin 'move 10' | Out-Null } catch {}
    $client.Close()
}
