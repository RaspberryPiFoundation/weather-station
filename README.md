Weather Station
==============

Data logging code for the Raspberry Pi Weather Station HAT

## Instructions to deploy

1. Start with a fresh install of Raspbian. Boot up as per usual and expand the filesystem to fill the SD card.
1. Un-blacklist the I²C module.

  `sudo nano /etc/modprobe.d/raspi-blacklist.conf`

  Comment out the line `blacklist i2c-bcm2708` by putting a hash `#` at the start of the line.
  
  Press `Ctrl - O` then `Enter` to save and `Ctrl - X` to quit nano.

1. Set the required modules to load automatically on boot.

  `sudo nano /etc/modules`
  
  Add the following lines to the bottom of the file:
  
  ```
  i2c-dev
  rtc_pcf8523
  w1-gpio
  w1-therm
  ```
  
  Press `Ctrl - O` then `Enter` to save and `Ctrl - X` to quit nano.

1. Ensure that a CR1225 coin cell battery has been inserted.
1. Enable the Real Time Clock (RTC).

  `echo "pcf8523 0x68" > /sys/class/i2c-adapter/i2c-1/new_device`
  
  Check that that it now appears in `/dev`
  
  `ls /dev/rtc*`
  
  Expect result: `/dev/rtc0`
  
1. Initialise the RTC with the correct time.

  Use the `date` command to check the current system time is correct, if it you can set the RTC time (from the system clock) with the following command:
  
  `sudo hwclock -w`
  
  If not then you can set the RTC time manually using the command below (you'll need to change the `--date` parameter, this example will set the date to the 1st of January 2014 at midnight):
  
  `sudo hwclock --set --date="2014-01-01 00:00:00" --utc`
  
  Then set the system clock from the RTC time.
  
  `sudo hwclock -s`

1. Enable the RTC driver and setting of the system clock at boot time.

  `sudo nano /etc/rc.local`
  
  Insert the following lines before `exit 0` at the bottom of the file:
  
  ```
  echo "pcf8523 0x68" > /sys/class/i2c-adapter/i2c-1/new_device
  sleep 2
  echo "Setting System clock from RTC..."
  hwclock -s
  hwclock -r
  ```
  
  Press `Ctrl - O` then `Enter` to save and `Ctrl - X` to quit nano.

1. Install the necessary software packages.

  ```
  sudo apt-get update
  sudo apt-get install i2c-tools python-smbus apache2 mysql-server php5 libapache2-mod-php5 php5-mysql python-mysqldb telnet -y
  ```
  
  This will take some time. You will be prompted to create and confirm a password for the root user of the MySQL database server. The password you choose will need to be put into `database.py` (line 87) unless you use `raspberry`.
  
1. Set up the required database with MySQL. Enter the password that you chose during installation.

  `mysql -u root -p`
  
  You'll now be at the MySQL prompt `mysql>`, first create the database:
  
  `CREATE DATABASE weather;`
  
  Expected result: `Query OK, 1 row affected (0.00 sec)`
  
  Switch to that database:
  
  `USE weather;`
  
  Expected result: `Database changed`
  
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
  
  Expected result: `Query OK, 0 rows affected (0.05 sec)`
  
  Press `Ctrl - D` to exit MySQL.
  
1. Remove the fake hardware clock package.

  `sudo apt-get remove fake-hwclock -y`

1. Reboot for the changes to take effect.

  `sudo reboot`

1. Log in as usual. Test that the I²C devices are online and working.

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
  60: -- -- -- -- -- -- -- -- UU 69 -- -- -- -- -- --
  70: -- -- -- -- -- -- -- 77
  ```
  
  - `40` = HTU21D. Humidity and temperature sensor.
  - `77` = BMP180. Barometric pressure sensor.
  - `68` = PCF8523. Real Time Clock, it will show as `UU` because it's reserved by the driver.
  - `69` = MCP3427. Analogue to Digital Converter.

  Note: `40` and `77` will only show if you have connected the **AIR** board to the main board.

1. Download the data logging code.

  ```
  cd ~
  git clone https://github.com/raspberrypi/weather-station.git
  ```
  
  This will create a new folder in the home directory called `weather-station`.
  
1. Set the Weather Station daemon to automatically start at boot time.

  `sudo nano /etc/rc.local`
  
  Insert the following lines before `exit 0` at the bottom of the file:
  
  ```
  echo "Starting Weather Station daemon..."
  /home/pi/weather-station/interrupt_daemon.py start
  ```
  
1. If you wish you can register your Weather Station with a cloud based **Oracle** database so that it can be used by other schools.

  [Oracle Apex Database](https://apex.oracle.com/pls/apex/f?p=28028:LOGIN_DESKTOP:127844066638258:&tz=1:00)
  
  You will need to complete a form whereupon an activation email will be sent to you containing a code. Log in using your school name for the username and the password that you chose. You will then be prompted for the activation code from the email.
  
  Many weather stations can belong to one school. Once you have logged in you'll need to create a new weather station under your school. The *latitude* and *longitude* of the weather station will be required for this. Once you have created a weather station it will have its own password automatically generated, this is used by the weather station itself when it uploads the measurements to Oracle and is separate to your school login.
  
1. Add the weather station name and password to the local credentials file. This allows the code that uploads to Oracle to know what credentials to use.

  `cd ~/weather-station`
  
  `nano credentials.template`
  
  Replace the `name` and `key` parameters with the name and password of the weather station as specified in Oracle. The double quotes `"` enclosing these values are important so take care not to remove them by mistake.
  
  Press `Ctrl - O` then `Enter` to save and `Ctrl - X` to quit nano.
  
1. Rename the credentials template file to enable it.

  `mv credentials.template credentials`

1. Enable the cron scheduler to automatically start taking measurements and uploading them to Oracle.

  `crontab < crontab.save`

1. The weather station will be ready when it comes up after a reboot.

  `sudo reboot`
