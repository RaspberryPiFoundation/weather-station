#!/usr/bin/python
import struct, array, time, i2c_base

CHANNEL_0 = 0
CHANNEL_1 = 1

CMD_ZERO = "\x00"
CMD_RESET = "\x06"
CMD_LATCH = "\x04"
CMD_CONVERSION = "\x08"
CMD_READ_CH0_16BIT = "\x88"
CMD_READ_CH1_16BIT = "\xA8"

msleep = lambda x: time.sleep(x/1000.0)

class MCP342X(object):
    shared = None
    def __init__(self, address = 0x69):
        self.dev = i2c_base.i2c(address, 1)
        self.max = 32767.0 #15 bits
        if MCP342X.shared == None:
            MCP342X.shared = self
        self.reset()

    def reset(self):
        self.dev.write(CMD_ZERO)
        self.dev.write(CMD_RESET)
        msleep(1)

    def latch(self):
        self.dev.write(CMD_ZERO)
        self.dev.write(CMD_LATCH)
        msleep(1)

    def conversion(self):
        self.dev.write(CMD_ZERO)
        self.dev.write(CMD_CONVERSION)
        msleep(1)

    def configure(self, channel = 0):
        if channel == 1:
            self.dev.write(CMD_READ_CH1_16BIT)
        else:
            self.dev.write(CMD_READ_CH0_16BIT)
        msleep(300)

    def read(self, channel = None):
        if channel != None:
            self.configure(channel)

        data = self.dev.read(3)
        buf = array.array('B', data)

        status = buf[2]
        result = None

        if status & 128 != 128: #check ready bit = 0
            result = buf[0] << 8 | buf[1]
        else:
            print "Not ready"

        return result

if MCP342X.shared == None:
    MCP342X()

if __name__ == "__main__":
    adc = MCP342X.shared
    adc.conversion()
    print "CH0:", adc.read(CHANNEL_0)
    print "CH1:", adc.read(CHANNEL_1)
