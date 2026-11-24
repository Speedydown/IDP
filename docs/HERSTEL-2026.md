# De spin weer tot leven (november 2026)

Verslag van het herstel van de robotspin uit het IDP-project van 2014 (NHL, groep 9 "Tracheata").
De spin stond nog in de kast, maar de SD-kaart van de Raspberry Pi was corrupt. Dit document beschrijft
wat er mis was, wat er is aangepast en hoe je alles opnieuw opbouwt.

## In het kort

| | |
|---|---|
| Oorzaak | De oude SD-kaart was fysiek kapot: alles voorbij ~1 GB werd niet meer opgeslagen. |
| Nieuw OS | Raspberry Pi OS (Legacy, 32-bit) Lite, Bookworm (2026-10-06) op een andere microSD. |
| Code | `IDPSpin/` geport van Python 2 naar Python 3; bugs uit 2014 en CPU-gebruik verbeterd. |
| Nieuw | Livecamera + webafstandsbediening (`IDPSpin/CameraStream.py`), toetsenbordbesturing (`sdcard/Spin-Remote.ps1`), en **SpinZoeker**: de spin zoekt zelf voorwerpen met Claude en vertelt hardop wat hij ziet (`SpinZoeker/`). |
| Status | Loopt (vooruit, achteruit, draaien, dansen), toeter werkt, camera streamt, zoekt en vindt voorwerpen. |

## Hardware (zoals aangetroffen)

| Onderdeel | Details |
|---|---|
| Computer | Raspberry Pi 1 Model B Rev 2 (ARMv6, 700 MHz, 512 MB) |
| Servo's | 18 servo's (6 poten × heup/knie/enkel) op 2× PCA9685 (I2C 0x40 en 0x41), 60 Hz |
| Gyro | MPU6050 (I2C 0x68), meet alleen kanteling, geen draaiing |
| ADC | MCP3008 via SPI (commando `gspi`) |
| Camera | Pi Camera v1 (OV5647) |
| Toeter | GPIO 30 en 31 (P5-header van de Pi 1 Rev 2) |
| WiFi | Edimax EW-7811Un USB-dongle (RTL8188CUS), **alleen 2,4 GHz** |

## Wat er mis was

1. **SD-kaart kapot.** Bij het opnieuw schrijven gaf de kaart rond 1006 MB een hardwarefout en verdween hij uit
   de lezer. Een tweede poging leek te lukken, maar bij teruglezen bleek alles vanaf 1006 MB niet opgeslagen.
   Waarschijnlijk versleten flash; het originele programma schreef bij **elk** commando het hele logbestand
   opnieuw naar de kaart, wat dat niet hielp.
2. **De oude software** was Python 2 op een NOOBS/Raspbian-installatie uit 2014. Die draait niet meer op
   een actueel besturingssysteem.

## Nieuwe installatie

- Image: `2026-10-06-raspios-bookworm-armhf-lite.img` (de nieuwste 32-bit Lite die een Pi 1 nog ondersteunt),
  SHA256 van de uitgepakte image `340d17e3…edc4b9`, na het schrijven teruggelezen en vergeleken.
- Eerste opstart via `sdcard/firstrun.sh` (hetzelfde mechanisme als Raspberry Pi Imager): hostname `spin`,
  gebruiker `pi`, SSH, WiFi, tijdzone, `i2c-dev`, code naar `/home/pi/IDPSpin`, services aanzetten.
  Voortgang komt in `firstrun.log` op de boot-partitie.
- Services: `spin` (besturing, TCP 1337), `spin-camera` (HTTP 8080), `spin-extras` (optionele pakketten; uitgezet, zie hieronder).
- Tools om dit te herhalen: `sdcard/Write-SpinSdCard.ps1` (schrijven + verifiëren + payload, ook op een
  andere PC via PS Remoting) en `sdcard/Set-SpinWifi.ps1` (WiFi achteraf wijzigen). Zie [`sdcard/README.md`](../sdcard/README.md).

## Aanpassingen aan de code (`IDPSpin/`)

### Python 2 → 3
- `print`-statements, `except X, e`, de `thread`-module, bytes/str op de socket.
- I2C via `smbus` → `smbus2` → eigen `smbus_compat.py` (pure Python, `/dev/i2c-1`), zodat er geen extra pakketten nodig zijn.
- I2C-bus vast op `/dev/i2c-1` (de oude revisiedetectie klopt niet met device-tree-kernels).
- Camera: `picamera2` met `picamera` als terugval, en draaien zonder camera kan ook. Het ongebruikte `pygame` is weg.
- GPIO (toeter): `rpi-lgpio` weigert de oude revisiecodes van de Pi 1, dus `IOPIN.py` valt terug op `lgpio`.

### Bugs uit 2014
- Eén mislukt commando (bijv. `ggyr` zonder gyro) liet de hele command-thread sterven: de spin reageerde niet meer. Nu komt er een foutmelding terug.
- Wisselen weg van dansmodus (`Dance.exit`) crashte door verkeerde attribuutnamen.
- Een verbroken verbinding liet de luister-thread eindeloos rondjes draaien; meerdere commando's in één pakket gingen verloren.
- `exit` stopte alleen een thread, niet het programma.
- Typfouten in `GyroData.py` (`bus`, `gyro.xout`).

### Prestaties op de Pi 1
- De command- en bewegingslus pollden 1000× per seconde. Met de camera erbij kwam een stop-commando tot 30 s te laat binnen. Nu 100 Hz: de besturing ging van ~25% naar ~10% CPU.
- Command-log naar `/run/spin` (RAM) in plaats van de SD-kaart.
- `spin-extras` (installatie van `picamera2` en `pyserial`) maakte de Pi zo druk dat het lopen hapert; die service staat uit.

## Nieuw

### Livecamera + webafstandsbediening
`IDPSpin/CameraStream.py` (service `spin-camera`): MJPEG via HTTP op poort 8080.

- http://spin.local:8080/ — livebeeld met pijlknoppen (vasthouden = lopen, loslaten = stop), snelheid, dansen, toeter. Werkt in elke browser, ook op een telefoon.
- `/stream.mjpg` (VLC, OBS) en `/snapshot.jpg` (één foto).
- De camera (`rpicam-vid`) draait alleen als iemand kijkt; 640×480 haalt ~5 fps en kost de Pi 1 ~60% CPU.
- Alleen een vaste lijst bewegingscommando's mag via de webpagina (niet bijvoorbeeld herstarten).
- Veiligheid: wisselen van venster of tabblad stuurt `move 10`.

### Toetsenbordbesturing
`sdcard/Spin-Remote.ps1`: W/A/S/D vasthouden = lopen, loslaten = stop (een console ziet geen key-up; het
script stopt zodra de toetsherhaling ophoudt). De eerste versie stuurde bij elke toetsherhaling opnieuw een
commando en nooit een stop, waardoor de spin bleef rondjes draaien. Dat is opgelost.

### SpinZoeker — de spin zoekt zelf
`SpinZoeker/` (.NET 10 console-app, zie [`SpinZoeker/README.md`](../SpinZoeker/README.md)). Je typt een voorwerp
("het potje"), en de app herhaalt: foto → de Claude CLI (`claude -p`) kijkt en kiest een actie → een Nederlandse
stem (Piper, `nl_NL-ronnie-medium`) vertelt wat de spin ziet en doet → de spin beweegt. Bij "klaar" steekt hij
zijn voorpoten uit en toetert. In de test vond hij "het potje" in 20 stappen.

## Protocol (TCP 1337)

Een bericht is `<commando> <argument><EOF>`; het antwoord eindigt ook op `<EOF>`.

| Commando | Betekenis |
|---|---|
| `ping` | antwoordt `ping` |
| `move NN` | 10 stop · 11 vooruit · 12 rechts-vooruit · 13 rechtsom · 14 rechts-achteruit · 15 achteruit · 16 links-achteruit · 17 linksom · 18 links-vooruit · 20/21 zijwaarts · 25 turbo · 26 lift |
| `smde N` / `gmde` | modus zetten/lezen: 1 lopen · 2 vingerbesturing (seriële handschoen) · 3 spider gap · 4 dans · 5 ballonrace (voorpoten vooruit) · 8 dans 2 |
| `smul N` / `gmul` | stapgrootte 1–5 (sneller) |
| `sdeg NN` / `gdeg` | paslengte in graden (9–34, standaard 20) |
| `shgt NNN` / `slen NNN` | hoogte (40–150) / poot-lengte (50–200) |
| `horn` | toeter |
| `ggyr` / `gspi` | gyro (kanteling x\|y) / ADC-waarde |
| `gimg` / `gifm` | camerabeeld als base64 (alleen met `picamera2`) |
| `glog` / `cllg` | command-log lezen / wissen |
| `gcpu` / `cocl` | CPU-gebruik / aantal verbonden clients |
| `exit` / `rebt` / `shtd` | programma stoppen / herstarten / uitzetten |

## Goed om te weten

- **WiFi**: de Edimax-dongle kan geen 5 GHz. Kies de 2,4 GHz-netwerknaam van de router.
- **Eerste opstart**: duurt op een Pi 1 met een trage kaart 10–15 minuten. Stroom eraf halen halverwege
  breekt `firstrun.sh` af; hij draait dan bij de volgende start gewoon opnieuw.
- **Draaien**: `move 17` 2,5 s ≈ 30°. Wisselen van draairichting laat de spin eerst een stukje terugdraaien
  (de poten gaan terug naar de beginstand). Vooruit lopen trekt een beetje naar links.
- **CPU**: de Pi 1 is de bottleneck. Livestream, softwarepakketten installeren en lopen tegelijk is te veel;
  sluit de livestream als de spin vlot moet lopen.
- **Trage kaarten**: de gebruikte microSD schrijft ~1 MB/s. Een nieuwe A1-kaart van een bekend merk (8–32 GB) is sneller en betrouwbaarder.
- **Inloggen**: `ssh pi@spin.local`; logs met `journalctl -u spin -f` en `journalctl -u spin-camera -f`.
