#!/usr/bin/python3
import io, fcntl 
I2C_SLAVE=0x0703 

class i2c(object):
   def __init__(self, device, bus):
      self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
      self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
      # set device address
      fcntl.ioctl(self.fr, I2C_SLAVE, device)
      fcntl.ioctl(self.fw, I2C_SLAVE, device)
   def write(self, bytes):
      self.fw.write(bytes)
   def read(self, bytes):
      return self.fr.read(bytes)
   def close(self):
      self.fw.close()
      self.fr.close()
