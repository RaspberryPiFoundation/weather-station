#!/usr/bin/python3
import interrupt_client, MCP342X, wind_direction, HTU21D, bmp085, tgs2600, ds18b20_therm
import database # requires MySQLdb python 2 library which is not ported to python 3 yet

pressure = bmp085.BMP085()
temp_probe = 21
#temp_probe = ds18b20_therm.DS18B20()
air_qual =  0
#air_qual = tgs2600.TGS2600(adc_channel = 0)
humidity = 50
#humidity = HTU21D.HTU21D()
wind_dir = 0
#wind_dir = wind_direction.wind_direction(adc_channel = 0, config_file="wind_direction.json")
#interrupts = interrupt_client.interrupt_client(port = 49501)
wind =0
gust =0
rain=0
temp=20

db = database.weather_database() #Local MySQL db

wind_average = 0
#wind_average = wind_dir.get_value(10) #ten seconds

print("Inserting...")
db.insert(temp, temp_probe, air_qual, pressure.get_pressure(), humidity, wind_average, wind, gust, rain)
print("done")

#interrupts.reset()
