#!/bin/bash

echo 'Please ensure your Weather Station HAT is connected to you Raspberry Pi, with the battery installed.'
echo 'Please ensure your Raspberry Pi is connected to the Internet'
echo 'Press any key to continue'

read -n 1 -s

##Update and upgrade - especially important for old NOOBS installs and I2C integration
sudo apt-get update && sudo apt-get upgrade -y

##Update config files.
echo "dtoverlay=w1-gpio" | sudo tee -a /boot/config.txt
echo "dtoverlay=pcf8523-rtc" | sudo tee -a /boot/config.txt

#sudo tee /boot/config.txt <<EOF
#dtoverlay=w1-gpio
#dtoverlay=pcf8523-rtc
#EOF

echo "i2c-dev" | sudo tee -a /etc/modules
echo "w1-therm" | sudo tee -a /etc/modules
#sudo tee /etc/modules <<EOF
#i2c-dev
#w1-therm
#EOF

##Check the RTC exists
if ls /dev/rtc** 1> /dev/null 2>&1; then
    echo "RTC found"
else
    echo "No RTC found - please follow manual setup to Troubleshoot."
    exit 1
fi

#Initialise RTC with correct time
echo "The current date set is:"
date
read -r -p "Is this correct [y/N] " response
response=${response,,}    # tolower
if [[ $response =~ ^(yes|y)$ ]]; then
    sudo hwclock -w
else
    read -p "Enter todays date and time (yyyy-mm-dd hh:mm:ss): " user_date
    sudo hwclock --set --date="$user_date" --utc #set hardware clock 
fi
#update system clock
sudo hwclock -s

#Update hwclock config
sudo perl -pi -e 's/systz/hctosys/g' /lib/udev/hwclock-set

#Remove hwc package
sudo update-rc.d fake-hwclock remove
sudo apt-get remove fake-hwclock -y

sudo apt-get install i2c-tools python-smbus telnet -y

echo "Install Complete"
echo "Please run <sudo i2cdetect -y 1> upon restart to test the sensors"
echo "System will now reboot"
sudo reboot
