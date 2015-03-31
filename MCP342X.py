#!/usr/bin/python3
import struct, array, time, i2c_base

CHANNEL_0 = 0
CHANNEL_1 = 1

CMD_ZERO = b"\x00"
CMD_RESET = b"\x06"
CMD_LATCH = b"\x04"
CMD_CONVERSION = b"\x08"
CMD_READ_CH0_16BIT = b"\x88"
CMD_READ_CH1_16BIT = b"\xA8"

msleep = lambda x: time.sleep(x/1000.0)

class MCP342X(object):
    def __init__(self, address = 0x69):
        self.dev = i2c_base.i2c(address, 1)
        self.max = 32767.0 #15 bits
        self.vref = 2.048
        self.tolerance_percent = 0.5
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

        if status & 128 != 128: # check ready bit = 0
            result = buf[0] << 8 | buf[1]
        else:
            print("Not ready")

        return result

if __name__ == "__main__":
    adc_main = MCP342X(address = 0x69) # ADC on the main HAT board
    adc_main.conversion()

    adc_air = MCP342X(address = 0x6A) # ADC on the snap off part with the AIR sensors
    adc_air.conversion()

    print("MAIN CH0: %s" % adc_main.read(CHANNEL_0)) # wind vane
    print("MAIN CH1: %s" % adc_main.read(CHANNEL_1)) # not populated

    print("AIR CH0: %s" % adc_air.read(CHANNEL_0)) # air quality
    print("AIR CH1: %s" % adc_air.read(CHANNEL_1)) # not populated
