#!/usr/bin/python
import time
from MCP342X import *

class wind_direction(object):
    def __init__(self, adc_channel = 0, margin = 10):        
        self.lookup = [
        12926, #N
        3234, #NNE
        3981, #NE
        462, #ENE
        520, #E
        358, #ESE
        1128, #SE
        726, #SSE
        1966, #S
        1593, #SSW
        7205, #SW
        6469, #WSW
        28030, #W
        15414, #WNW
        20352, #NW
        9378 #NNW
        ]

        self.adc_channel = adc_channel
        self.margin = margin

    def get_dir(self, adc_value):
        angle = None

        for i, value in enumerate(self.lookup):
            bottom_end = value - self.margin
            top_end = value + self.margin

            if adc_value >= bottom_end and adc_value <= top_end:
                angle = i * 22.5
                break

        return angle
        
    def get_value(self, length = 5):
        adc = MCP342X.shared
        data = []
        print "Measuring wind direction for", length, "seconds..."
        start_time = time.time()

        while time.time() - start_time <= length:
            adc_value = adc.read(0)
            direction = self.get_dir(adc_value)
            if direction != None: # keep only good measurements
                data.append(direction)

        average = None

        if len(data) > 0:
            average = sum(data) / len(data)

        return average
