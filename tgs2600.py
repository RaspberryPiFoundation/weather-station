#!/usr/bin/python3
import MCP342X

class TGS2600(object):
    def __init__(self, adc_channel = 0):
        self.adc_channel = adc_channel
        
    def get_value(self):
        adc = MCP342X.MCP342X(address = 0x6a)
        adc_value = adc.read(self.adc_channel)
        return (100.0 / adc.max) * (adc.max - adc_value) #as percentage

if __name__ == "__main__":
    obj = TGS2600(0)
    print("Air Quality: %s %%" % obj.get_value())
