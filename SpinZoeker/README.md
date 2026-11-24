# SpinZoeker

Console-app (Windows, .NET 10) die de robotspin een voorwerp laat zoeken met zijn camera.
Een Nederlandse stem (Piper) leest voor wat de spin ziet en doet.

Elke ronde:
1. Foto van de spin (`http://<spin>:8080/snapshot.jpg`, zie `IDPSpin/CameraStream.py`).
2. De Claude CLI (`claude -p`, model `sonnet`) bekijkt de foto en kiest een actie: draaien, vooruit, achteruit of klaar.
3. Piper (`nl_NL-ronnie-medium`) leest een korte zin voor, voor kinderen.
4. De spin voert de actie uit via spInOS (TCP 1337) en stopt daarna altijd.

Bij "klaar" steekt de spin zijn voorpoten uit (ballonmodus `smde 5`), toetert en gaat terug naar loopmodus.

## Starten

```powershell
cd C:\git\projects\IDP\SpinZoeker
dotnet run -c Release -- "het potje"            # direct zoeken
dotnet run -c Release                           # vraagt wat hij moet zoeken (leeg = stoppen)
dotnet run -c Release -- --host 192.168.1.123 --model sonnet --stappen 40 "de haai"
```

Ctrl+C stopt de poten altijd.

## Benodigd (eenmalig)

- De Claude CLI, ingelogd (`claude` in het PATH).
- Piper + stem in `tools\` (niet in git):

```powershell
$t = "$PWD\tools"; New-Item -ItemType Directory -Force "$t\voices" | Out-Null
curl.exe -sSL -o "$t\piper.zip" https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip
Expand-Archive "$t\piper.zip" -DestinationPath $t -Force; Remove-Item "$t\piper.zip"
$v = 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/nl/nl_NL/ronnie/medium'
curl.exe -sSL -o "$t\voices\nl_NL-ronnie-medium.onnx" "$v/nl_NL-ronnie-medium.onnx"
curl.exe -sSL -o "$t\voices\nl_NL-ronnie-medium.onnx.json" "$v/nl_NL-ronnie-medium.onnx.json"
```

## Goed om te weten

- De foto's van elke zoektocht staan in `%TEMP%\spinzoeker\<datum-tijd>\`.
- Een ronde duurt ongeveer 15 seconden: Claude ~7 s, plus bewegen en wachten op een scherpe foto.
- Wisselen van draairichting laat de spin eerst een stukje terugdraaien, en vooruit lopen trekt naar links. Dat staat in de prompt.
- Staat de livestream in de browser open, dan heeft de Pi 1 het druk; de app werkt dan nog steeds, alleen trager.
