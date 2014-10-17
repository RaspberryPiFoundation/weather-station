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
  
  Insert the following lines before `exit 0` at the bottom of the file.
  
  ```
  echo "pcf8523 0x68" > /sys/class/i2c-adapter/i2c-1/new_device
  sleep 2
  echo "Setting System clock from RTC..."
  hwclock -s
  hwclock -r
  ```
  
  Press `Ctrl - O` to save and `Ctrl - X` to quit nano.
