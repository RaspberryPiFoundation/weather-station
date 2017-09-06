#!/usr/bin/python3
import bmpBackend

class BMP085(object):
    def __init__(self):
        self.bmp = bmpBackend.BMP085(bus=1)
        self.temperature = 0
        self.pressure = 0
        self.lastValue = (0, 0)

    def get_pressure(self):
        return self.bmp.readPressure() * 0.01 #hPa

    def get_temperature(self):
        return self.bmp.readTemperature()
