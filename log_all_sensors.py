#!/usr/bin/python
import interrupt_client, MCP342X, wind_direction, HTU21D, tgs2600, ds18b20_therm
import database # requires MySQLdb python 2 library which is not ported to python 3 yet

from Adafruit_BME280 import *
sensor = BME280(mode=BME280_OSAMPLE_8)
pascals = sensor.read_pressure()
hectopascals = pascals / 100
bme280_humidity = sensor.read_humidity()
print "BME280_humidity =", bme280_humidity
print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)

temp_probe = ds18b20_therm.DS18B20()
air_qual = tgs2600.TGS2600(adc_channel = 1)
print 'Air Quality  = ',air_qual.get_value(),'%'
humidity = HTU21D.HTU21D()
wind_dir = wind_direction.wind_direction(adc_channel = 0, config_file="wind_direction.json")
interrupts = interrupt_client.interrupt_client(port = 49501)

db = database.weather_database() #Local MySQL db

wind_average = wind_dir.get_value(10) #ten seconds

print("Inserting...")
#db.insert(humidity.read_temperature(), temp_probe.read_temp(), air_qual.get_value(), pressure.get_pressure(), humidity.read_humidity(), wind_average, interrupts.get_wind(), interrupts.get_wind_gust(), interrupts.get_rain())
db.insert(humidity.read_temperature(), temp_probe.read_temp(), air_qual, hectopascals, humidity.read_humidity(), wind_average, interrupts.get_wind(), interrupts.get_wind_gust(), interrupts.get_rain())
print("done")

interrupts.reset()
