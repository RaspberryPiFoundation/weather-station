import bme280
import smbus2
from time import sleep

port = 1
address = 0x77
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def read_all():
    bme280_data = bme280.sample(bus,address)
    humidity  = bme280_data.humidity
    pressure  = bme280_data.pressure
    ambient_temperature = bme280_data.temperature
    return(humidity, pressure, ambient_temperature)

# print(read_all())
