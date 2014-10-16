#!/usr/bin/python
from interrupt_client import *
from database import *

from MCP342X import * #ADC
from wind_direction import * #Wind direction
from HTU21D import * #Humidity and Temp
from bmp085 import * #Pressure and Temp
from tgs2600 import * #Air Quality
from ds18b20_therm import * #Temperature Probe

pressure = BMP085()
temp_probe = DS18B20()
air_qual = TGS2600(adc_channel = 1)
humidity = HTU21D()
wind_dir = wind_direction(adc_channel = 0, margin = 20)
interrupts = interrupt_client(port = 49501)

db = weather_database() #Local MySQL db

wind_average = wind_dir.get_value(10) #ten seconds

print "Inserting..."
db.insert(humidity.read_tmperature(), temp_probe.read_temp(), air_qual.get_value(), pressure.get_pressure(), humidity.read_humidity(), wind_average, interrupts.get_wind(), interrupts.get_wind_gust(), interrupts.get_rain())
print "done"

interrupts.reset()
