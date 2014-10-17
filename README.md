Weather Station
==============

Data logging code for the Raspberry Pi Weather Station HAT

## Instructions to deploy

1. Start with a fresh install of Raspbian. Boot up as per usual and expand the filesystem to fill the SD card.
1. Un-blacklist the Pi i2c modules.

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
