from gpiozero import Button

import math
import time

RADIUS_CM = 9.0 # Radius of wind speed sensor
WIND_INTERVAL = 5 # Time gathering counts
CIRCUMFERENCE_CM = (2 * math.pi) * RADIUS_CM

def spin():
    global wind_count
    wind_count = wind_count + 1
    
# Calculate speed in cm/s
def calculate_speed(time_sec):
    global wind_count

    rotations = wind_count / 2.0
    dist_cm = CIRCUMFERENCE_CM * rotations
    speed = dist_cm / time_sec
    return(speed)

wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin

while True:
    wind_count = 0
    time.sleep(WIND_INTERVAL)
    print((calculate_speed(WIND_INTERVAL) * 0.036), "km/h")
