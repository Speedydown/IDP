#!/bin/bash
# spInOS first boot - runs once via cmdline.txt (systemd.run=...), same mechanism
# Raspberry Pi Imager uses. Sets up hostname/user/ssh/wifi, installs the spider
# code from the boot partition and enables the spin service. Removes itself.
set +e

SPIN_HOSTNAME="spin"
SPIN_USER="pi"
SPIN_PASSHASH='__PASSHASH__'
WIFI_SSID='__WIFI_SSID__'
WIFI_PASS='__WIFI_PASS__'
WIFI_COUNTRY='NL'

BOOT=/boot/firmware
[ -d "$BOOT/spin" ] || BOOT=/boot
# progress log on the boot partition (readable from Windows); no set -x: it would log the wifi password
exec >>"$BOOT/firstrun.log" 2>&1
echo "=== firstrun start $(date)"
IMAGER=/usr/lib/raspberrypi-sys-mods/imager_custom

# --- hostname ---
echo "--- hostname $(date +%T)"
CURRENT_HOSTNAME=$(tr -d " \t\n\r" < /etc/hostname)
if [ -f "$IMAGER" ]; then
   "$IMAGER" set_hostname "$SPIN_HOSTNAME"
else
   echo "$SPIN_HOSTNAME" > /etc/hostname
   sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$SPIN_HOSTNAME/g" /etc/hosts
fi

# --- ssh ---
echo "--- ssh $(date +%T)"
if [ -f "$IMAGER" ]; then
   "$IMAGER" enable_ssh
else
   systemctl enable ssh
fi

# --- user ---
echo "--- user $(date +%T)"
if [ -f /usr/lib/userconf-pi/userconf ]; then
   /usr/lib/userconf-pi/userconf "$SPIN_USER" "$SPIN_PASSHASH"
else
   echo "$SPIN_USER:$SPIN_PASSHASH" | chpasswd -e
fi

# --- wifi (optional, only when a USB wifi dongle is used) ---
echo "--- wifi (optional, only when a USB wifi dongle is used) $(date +%T)"
if [ -n "$WIFI_SSID" ] && [ "$WIFI_SSID" != "__WIFI_SSID__" ] && [ -f "$IMAGER" ]; then
   "$IMAGER" set_wlan "$WIFI_SSID" "$WIFI_PASS" "$WIFI_COUNTRY"
fi

# --- locale / time ---
echo "--- locale / time $(date +%T)"
if [ -f "$IMAGER" ]; then
   "$IMAGER" set_keymap 'us'
   "$IMAGER" set_timezone 'Europe/Amsterdam'
fi

# --- I2C (servo boards 0x40/0x41, MPU6050 gyro 0x68) and SPI (MCP3008) ---
echo "--- I2C (servo boards 0x40/0x41, MPU6050 gyro 0x68) and SPI (MCP3008) $(date +%T)"
grep -q '^i2c-dev' /etc/modules || echo 'i2c-dev' >> /etc/modules

# --- spider code ---
echo "--- spider code $(date +%T)"
HOMEDIR=$(getent passwd "$SPIN_USER" | cut -d: -f6)
[ -n "$HOMEDIR" ] || HOMEDIR=/home/$SPIN_USER
mkdir -p "$HOMEDIR/IDPSpin"
cp -r "$BOOT/spin/IDPSpin/." "$HOMEDIR/IDPSpin/"
chown -R "$SPIN_USER:$SPIN_USER" "$HOMEDIR/IDPSpin"

sed "s|/home/pi|$HOMEDIR|g" "$BOOT/spin/spin.service" > /etc/systemd/system/spin.service
cp "$BOOT/spin/spin-extras.service" /etc/systemd/system/spin-extras.service
cp "$BOOT/spin/spin-camera.service" /etc/systemd/system/spin-camera.service
systemctl enable spin.service
systemctl enable spin-extras.service
systemctl enable spin-camera.service

echo "spInOS installed $(date)" > "$BOOT/spin/INSTALLED.txt"

# --- clean up: run only once ---
echo "--- clean up: run only once $(date +%T)"
rm -f "$BOOT/firstrun.sh"
sed -i 's| systemd.run.*||g' "$BOOT/cmdline.txt"
exit 0
