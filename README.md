Weather Station
==============

Data logging code for the Raspberry Pi Weather Station HAT

## Instructions to deploy

1. Start with a fresh install of Raspbian. Boot up as per usual and expand the filesystem to fill the SD card.
1. Un-blacklist the I²C module.

  `sudo nano /etc/modprobe.d/raspi-blacklist.conf`

  Comment out the line `blacklist i2c-bcm2708` but putting a hash `#` at the start of the line.
  
  Press `Ctrl - O` to save and `Ctrl - X` to quit nano.

1. Set the modules that load automatically on boot.

  `sudo nano /etc/modules`
  
  Add the following lines:
  
  ```
  i2c-dev
  rtc_pcf8523
  w1-gpio
  w1-them
  ```
  
  Press `Ctrl - O` to save and `Ctrl - X` to quit nano.

1. Enable the RTC driver and the setting of the system clock from it at boot time.

  `sudo nano /etc/rc.local`
  
  Insert the following lines before `exit 0` at the bottom of the file:
  
  ```
  echo "pcf8523 0x68" > /sys/class/i2c-adapter/i2c-1/new_device
  sleep 2
  echo "Setting System clock from RTC..."
  hwclock -s
  hwclock -r
  ```
  
  Press `Ctrl - O` to save and `Ctrl - X` to quit nano.

1. Install the necessary software packages.

  ```
  sudo apt-get update
  sudo apt-get install i2c-tools python-smbus apache2 mysql-server php5 libapache2-mod-php5 php5-mysql python-mysqldb telnet -y
  ```
  
  You will be prompted to create and confirm a password for the root user of the MySQL database server. The password you choose will need to be put into `database.py` unless you use `raspberry`.
  
1. Remove the fake hardware clock package.

  `sudo apt-get remove fake-hwclock -y`

1. Test that the I²C devices are online and working.

  `sudo i2cdetect -y 1`
  
  Expected output:
  
  ```
       0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
  00:          -- -- -- -- -- -- -- -- -- -- -- -- --
  10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  60: -- -- -- -- -- -- -- -- 68 69 -- -- -- -- -- --
  70: -- -- -- -- -- -- -- 77
  ```
  
  - 40 = HTU21D. Humidity and temperature sensor.
  - 77 = BMP180. Barometric pressure sensor.
  - 68 = PCF8523. Real Time Clock, maybe shown as UU because it's reserved for the driver.
  - 69 = MCP3427. Analogue to Digital Converter.
