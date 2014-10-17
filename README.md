Weather Station
==============

Data logging code for the Raspberry Pi Weather Station HAT

## Instructions to deploy

1. Start with a fresh install of Raspbian. Boot up as per usual and expand the filesystem to fill the SD card.
1. Un-blacklist the I²C module.

  `sudo nano /etc/modprobe.d/raspi-blacklist.conf`

  Comment out the line `blacklist i2c-bcm2708` by putting a hash `#` at the start of the line.
  
  Press `Ctrl - O` to save and `Ctrl - X` to quit nano.

1. Set the required modules to load automatically on boot.

  `sudo nano /etc/modules`
  
  Add the following lines:
  
  ```
  i2c-dev
  rtc_pcf8523
  w1-gpio
  w1-therm
  ```
  
  Press `Ctrl - O` to save and `Ctrl - X` to quit nano.

1. Enable the RTC driver and the setting of the system clock at boot time.

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
  
  You will be prompted to create and confirm a password for the root user of the MySQL database server. The password you choose will need to be put into `database.py` (line 87) unless you use `raspberry`.
  
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
  
  - `40` = HTU21D. Humidity and temperature sensor.
  - `77` = BMP180. Barometric pressure sensor.
  - `68` = PCF8523. Real Time Clock, after a reboot it will show as UU because it's reserved for the driver.
  - `69` = MCP3427. Analogue to Digital Converter.

  Note: `40` and `77` will only show if you have connected the **AIR** board to the main board.

1. Download the data logging code.

  ```
  cd ~
  git clone https://github.com/raspberrypi/weather-station.git
  ```
  
  This will create a new folder in the home directory called `weather-station`.

1. Set up the required database with MySQL. Enter the password that you chose during installation.

  `mysql -u root -p`
  
  You'll now be at the MySQL prompt `mysql>`, first create the database:
  
  `CREATE DATABASE weather;`
  
  Switch to that database:
  
  `use weather;`
  
  Create the table that will store all of the weather measurements:
  
  ```
  CREATE TABLE WEATHER_MEASUREMENT(
    ID BIGINT NOT NULL AUTO_INCREMENT,
    REMOTE_ID BIGINT,
    AMBIENT_TEMPERATURE DECIMAL(6,2) NOT NULL,
    GROUND_TEMPERATURE DECIMAL(6,2) NOT NULL,
    AIR_QUALITY DECIMAL(6,2) NOT NULL,
    AIR_PRESSURE DECIMAL(6,2) NOT NULL,
    HUMIDITY DECIMAL(6,2) NOT NULL,
    WIND_DIRECTION DECIMAL(6,2) NULL,
    WIND_SPEED DECIMAL(6,2) NOT NULL,
    WIND_GUST_SPEED DECIMAL(6,2) NOT NULL,
    RAINFALL DECIMAL (6,2) NOT NULL,
    CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ( ID )
  );
  ```
  
  Press `Ctrl - D` to exit MySQL.
  
1. Set the Weather Station daemon to automatically start at boot time.

  `sudo nano /etc/rc.local`
  
  Insert the following lines before `exit 0` at the bottom of the file:
  
  ```
  echo "Starting Weather Station daemon..."
  /home/pi/weather-station/interrupt_daemon.py start
  ```
  
1. Register your Weather Station with **Oracle** if you wish to upload your data so that it can be used by others.

  Go [here](https://apex.oracle.com/pls/apex/f?p=28028:LOGIN_DESKTOP:127844066638258:&tz=1:00)
  
  You will need to complete a form whereupon an activation email will be sent to you containing a code. Log in using your school name for the username and the password that you chose. You will then be prompted for the activation code from the email.
  
  Many weather stations can belong to one school. Once you have logged in you'll need to create a new weather station under your school. The *latitude* and *longitude* of the weather station will be required for this. Once you have created a weather station it will have its own password automatically generated, this is used by the individual weather station itself when it uploads its measurements to Oracle.
