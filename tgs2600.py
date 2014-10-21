#!/usr/bin/python
import MCP342X

class TGS2600(object):
    def __init__(self, adc_channel = 1):
        self.adc_channel = adc_channel
        
    def get_value(self):
        adc = MCP342X.MCP342X.shared
        adc_value = adc.read(self.adc_channel)
        return (100.0 / adc.max) * (adc.max - adc_value) #as percentage
