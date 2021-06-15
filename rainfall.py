#!/usr/bin/env python3
import os, time
import paho.mqtt.client as mqtt
from gpiozero import Button

BUCKET_SIZE = 0.2794  # mm
MM_TO_IN = 0.0393701

rain_sensor = Button(5)  # originally 6
count = 0
interval = 60  # seconds
verbose = False

mqtt_host = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else '192.168.2.104'
mqtt_client_id = os.getenv('HOSTNAME') if os.getenv('HOSTNAME') else 'ws1-rainfall'
mqtt_topic_base = os.getenv('MQTT_TOPIC') if os.getenv('MQTT_TOPIC') else f"{mqtt_client_id}/ads-ws1"
mqtt_rainfall_topic = f"{mqtt_topic_base}/rainfall1"

def mqtt_on_connect():
    print('mqtt connected')

mqtt_client = mqtt.Client(client_id=mqtt_client_id)
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.connect(mqtt_host, 1883)

def bucket_tipped():
    global count
    count += 1
    print(count * BUCKET_SIZE)

def reset_rainfall():
    global count
    count = 0

def calculate_rainfall(interval):
    global count
    rainfall_mm = count * BUCKET_SIZE
    rainfall_in = rainfall_mm * MM_TO_IN
    return rainfall_in

rain_sensor.when_pressed = bucket_tipped

while True:
    reset_rainfall()
    rainfall = calculate_rainfall(interval)
    res, _msg_id = mqtt_client.publish(topic=mqtt_rainfall_topic, payload=rainfall)
    if res == mqtt.MQTT_ERR_SUCCESS:
        if verbose:
            print(f"topic:{mqtt_rainfall_topic} payload:{rainfall}")
    else:
        print(f"error publishing mqtt: {res}")
    time.sleep(interval)

