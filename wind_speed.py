#!/usr/bin/env python3
import math
import os
import statistics
import time
import paho.mqtt.client as mqtt
from gpiozero import Button

CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
KM_TO_MI = 0.621371

anemometer_pin = 24  # originally 5
wind_count = 0  # count half-rotations of anemometer
radius_cm = 9.0  # radius in cm of anemometer
circumference_cm = (2 * math.pi) * radius_cm
wind_interval = 60  # how often (seconds) to report
anemometer_factor = 1.18  # default anemometer factor
store_speeds = []

mqtt_host = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else '192.168.2.104'
mqtt_client_id = os.getenv('HOSTNAME') if os.getenv('HOSTNAME') else 'ws1-anemometer'
mqtt_topic_base = os.getenv('MQTT_TOPIC') if os.getenv('MQTT_TOPIC') else f"{mqtt_client_id}/ads-ws1"
mqtt_anemometer_topic = f"{mqtt_topic_base}/anemometer1"
mqtt_wind_vane_topic = f"{mqtt_topic_base}/anemometer1"
mqtt_rain_gauge_topic = f"{mqtt_topic_base}/anemometer1"

def mqtt_on_connect():
    print('mqtt connected')

mqtt_client = mqtt.Client(client_id=mqtt_client_id)
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.connect(mqtt_host, 1883)

def spin():
    global wind_count
    wind_count = wind_count + 1
    # print("spint" + str(wind_count))

def calculate_speed(time_sec):
    global wind_count
    rotations = wind_count / 2.0
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR
    corrected_km_per_hour = km_per_hour * anemometer_factor
    corrected_mph = corrected_km_per_hour * KM_TO_MI
    return corrected_km_per_hour

def reset_wind():
    global wind_count
    wind_count = 0

wind_speed_sensor = Button(anemometer_pin)
wind_speed_sensor.when_pressed = spin

while True:
    reset_wind()
    time.sleep(wind_interval)
    wind_speed = calculate_speed(wind_interval)
    print(f"topic:{mqtt_anemometer_topic} payload:{wind_speed}")
    mqtt_client.publish(mqtt_anemometer_topic, payload=wind_speed)
