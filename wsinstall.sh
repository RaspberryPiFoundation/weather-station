#!/bin/bash

echo 'Please ensure your Weather Station HAT is connected to your Raspberry Pi, with the battery installed.'
echo 'Please ensure your Raspberry Pi is connected to the Internet'

## Check ready to start
echo "Do you want to install the Weather Station software?"
read -r -p "$1 [y/N] " response < /dev/tty
if [[ $response =~ ^(yes|y|Y)$ ]]; then
    echo "Starting"
else
    echo "Exiting"
    exit
fi

echo 'Updating Raspbian'
## Update and upgrade - especially important for old NOOBS installs and I2C integration
sudo apt-get update && sudo apt-get upgrade -y

# These pacakages needed if using Stretch-lite image

sudo apt-get install python3-smbus git python3-pip -y
sudo pip3 install RPi.GPIO
##E nable I2C
echo ' Enabling I2C'
sudo raspi-config nonint do_i2c 0

## Update config files.
echo "dtoverlay=w1-gpio" | sudo tee -a /boot/config.txt
echo "dtoverlay=pcf8523-rtc" | sudo tee -a /boot/config.txt
echo "i2c-dev" | sudo tee -a /etc/modules
echo "w1-therm" | sudo tee -a /etc/modules

echo 'Setting up RTC'
## Check the RTC exists
if ls /dev/rtc** 1> /dev/null 2>&1; then
    echo "RTC found"
else
    echo "No RTC found - please follow manual setup to Troubleshoot."
    exit 1
fi

## Initialise RTC with correct time
echo "The current date and time set is:"
date
read -r -p "Is this correct [y/N] " response2 < /dev/tty
response2=${response2,,}    # tolower
if [[ $response2 =~ ^(yes|y)$ ]]; then
    sudo hwclock -w
else
    read -p "Enter todays date and time (yyyy-mm-dd hh:mm:ss): "  user_date < /dev/tty
    sudo hwclock --set --date="$user_date" --utc #set hardware clock
fi

#update system clock
sudo hwclock -s

#Update hwclock config
sudo perl -pi -e 's/systz/hctosys/g' /lib/udev/hwclock-set

#Remove hwc package
sudo update-rc.d fake-hwclock remove
sudo apt-get remove fake-hwclock -y

echo 'Installing required packages'
## Install com tools
sudo apt-get install i2c-tools python-smbus telnet -y

## Set password for mysql-server
echo 'Please choose a password for your database'
read -s -p "Password: " PASS1 < /dev/tty
echo
read -s -p "Password (again): " PASS2 < /dev/tty

# check if passwords match and if not ask again
while [ "$PASS1" != "$PASS2" ];
do
    echo
    echo "Please try again"
    read -s -p "Password: " PASS1 < /dev/tty
    echo
    read -s -p "Password (again): " PASS2 < /dev/tty
done

echo 'Installing local database'
sudo apt-get install -y mariadb-server mariadb-client libmariadbclient-dev
# sudo apt-get install -y apache2 php5 libapache2-mod-php5 php-mysql
sudo pip3 install mysqlclient


## Create a database and weather table
echo 'Creating Database'
sudo mysql  <<EOT
create user pi IDENTIFIED by '$PASS1';
grant all privileges on *.* to 'pi' with grant option;
CREATE DATABASE weather;
USE weather;
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
EOT

## Get the weather station python files
cd ~
git clone https://github.com/raspberrypi/weather-station.git

## Setup rc.local to start weatherstaion daemon
sudo sed -i '/exit 0/d' /etc/rc.local
echo 'echo "Starting Weather Station daemon..."' | sudo tee -a /etc/rc.local
echo '/home/pi/weather-station/interrupt_daemon.py start' | sudo tee -a /etc/rc.local
echo 'exit 0' | sudo tee -a /etc/rc.local

## Add in correct sql credentials
cd weather-station
git checkout stretch
cat <<EOT > credentials.mysql
{
"HOST": "localhost",
"USERNAME": "pi",
"PASSWORD": "$PASS1",
"DATABASE": "weather"
}
EOT

## Alter crontab for periodic uploads
crontab < crontab.save

## Add credentials for weather station
echo 'You should have registered you weather station at'
echo 'https://apex.oracle.com/pls/apex/f?p=81290:LOGIN_DESKTOP:0:::::&tz=1:00'
echo 'You should have a Weather Station Name'
echo 'You should have a Weather Station Key'
read -p "Please type in your Weather Station Name: " name < /dev/tty
read -p "Please type in your Weather Station Key: " key < /dev/tty

cat <<EOT > credentials.oracle
{
"WEATHER_STN_NAME": "$name",
"WEATHER_STN_PASS": "$key"
}
EOT
echo "All done - rebooting"
sudo reboot
