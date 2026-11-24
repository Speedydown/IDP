# SD-kaart voor de spin (spInOS)

Alles wat nodig is om een nieuwe SD-kaart voor de Raspberry Pi 1 van de spin te maken.
Het volledige verslag van het herstel staat in [`docs/HERSTEL-2026.md`](../docs/HERSTEL-2026.md).

- OS: Raspberry Pi OS (Legacy, 32-bit) **Lite**, Bookworm, 2026-10-06 (armhf; draait nog op een Pi 1).
- Code: `IDPSpin/` (geport naar Python 3), komt op de Pi in `/home/pi/IDPSpin`.
- Services:
  - `spin.service`: de besturing (`python3 Test.py`, TCP-poort 1337).
  - `spin-camera.service`: livebeeld + webafstandsbediening op poort 8080 (`CameraStream.py`).
  - `spin-extras.service`: installeert eenmalig `python3-serial` (vingerbesturing, modus 2) en `python3-picamera2`.
    Op een Pi 1 vreet die installatie de CPU op; op de huidige spin staat hij daarom uit (`systemctl disable spin-extras`).
    Lopen, dansen en de camerastream hebben hem niet nodig.
- I2C (servo-boards 0x40/0x41, gyro 0x68) en SPI staan aan in `config.txt`; `i2c-dev` in `/etc/modules`.
- `rpi-lgpio`, `smbus2` en `spidev` zitten al in de Lite-image: de spin loopt ook zonder internet.
- De command-log staat in `/run/spin` (RAM). Het origineel schreef bij elk commando het hele logbestand naar de SD-kaart.

## Kaart maken

Automatisch, ook op een andere PC via PS Remoting (schrijft, leest terug, vergelijkt de hash en zet daarna de payload op de boot-partitie):

```powershell
.\Write-SpinSdCard.ps1 -ComputerName server -DiskNumber <n> -ImagePath <img op die PC> `
    -ExpectedSha256 <hash> -WifiSsid "MijnWifi-2.4GHz" -WifiPassword "..." -UserPassword "..."
```

Handmatig:

1. Schrijf de image naar de kaart (Raspberry Pi Imager zonder aanpassingen, of raw).
2. Kopieer naar de boot-partitie (`bootfs`):
   - `firstrun.sh` (vul `__PASSHASH__` met de uitvoer van `openssl passwd -6`, en eventueel `__WIFI_SSID__`/`__WIFI_PASS__`)
   - map `spin/` met `IDPSpin/`, `spin.service`, `spin-extras.service`, `spin-camera.service`
3. Voeg aan het eind van de (enige) regel in `cmdline.txt` toe:
   ` systemd.run=/boot/firmware/firstrun.sh systemd.run_success_action=reboot systemd.unit=kernel-command-line.target`
4. Voeg aan `config.txt` toe: `dtparam=i2c_arm=on` en `dtparam=spi=on`.

De eerste boot op een Pi 1 duurt **10–15 minuten** (partitie vergroten, firstrun, herstart). Haal de stroom er
in die tijd niet af. `firstrun.sh` schrijft zijn voortgang naar `firstrun.log` op de boot-partitie; die kun je
in Windows lezen als het misgaat.

## WiFi

De Edimax EW-7811Un kan alleen **2,4 GHz**. Gebruik de 2,4 GHz-netwerknaam van je router (veel routers hebben
aparte namen voor 2,4 en 5 GHz). WiFi achteraf wijzigen, met de kaart in een kaartlezer:

```powershell
.\Set-SpinWifi.ps1 -DiskNumber 1 -WifiSsid "MijnWifi-2.4GHz" -WifiPassword "..."                        # lokaal
.\Set-SpinWifi.ps1 -ComputerName server -DiskNumber 2 -WifiSsid "MijnWifi-2.4GHz" -WifiPassword "..."   # andere PC
```

## Camera en afstandsbediening

- Browser: http://spin.local:8080/ — livebeeld (640×480, ~5 fps op een Pi 1) met pijlknoppen
  (ingedrukt houden = lopen, loslaten = stop) en knoppen voor snelheid, dansen en toeter.
  Losse stream: `/stream.mjpg`, één foto: `/snapshot.jpg`. De camera draait alleen als iemand kijkt.
- Toetsenbord: `.\Spin-Remote.ps1 -Address spin.local`. W/A/S/D vasthouden = lopen, loslaten = stop,
  1–8 = modus, H = toeter, X = afsluiten.
- Inloggen: `ssh pi@spin.local`. Logs: `journalctl -u spin -f`.
