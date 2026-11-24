IDP
===

Code voor IDP groep 9

Project IDP : Robot Spin

Inhoud:
- Windows 8 App (`IDPApp/`)
- Python besturing (`IDPSpin/`, spInOS)
- Netwerktest
- Website
- SpinOS

Contact:  riem1203@student.nhl.nl
          @spiderdp

Copyright NHL projectteam 9 "Tracheata"

2026: de spin loopt weer
------------------------

In november 2026 is de spin weer tot leven gebracht: nieuwe SD-kaart, de besturing geport naar Python 3,
een livecamera met webafstandsbediening, en een app waarmee de spin zelf voorwerpen zoekt en hardop vertelt
wat hij ziet.

- Verslag van het herstel: [`docs/HERSTEL-2026.md`](docs/HERSTEL-2026.md)
- SD-kaart maken, WiFi, camera en besturing: [`sdcard/README.md`](sdcard/README.md)
- De spin laat zoeken (Claude + Nederlandse stem): [`SpinZoeker/README.md`](SpinZoeker/README.md)

Snel aan de slag (spin aan, zelfde netwerk):

- Browser: http://spin.local:8080/ — livebeeld + loopknoppen
- Toetsenbord: `sdcard\Spin-Remote.ps1 -Address spin.local`
- Zoeken: `cd SpinZoeker; dotnet run -c Release -- "de beer"`
