#!/usr/bin/env python3
import math
import os
import time
import paho.mqtt.client as mqtt
from gpiozero import MCP3008

volts = {0.4: 0.0,
         1.4: 22.5,
         1.2: 45.0,
         2.8: 67.5,
         2.7: 90.0,
         2.9: 112.5,
         2.2: 135.0,
         2.5: 157.5,
         1.8: 180.0,
         2.0: 202.5,
         0.7: 225.0,
         0.8: 247.5,
         0.1: 270.0,
         0.3: 292.5,
         0.2: 315.0,
         0.6: 337.5}

adc = MCP3008(channel=0)

interval = 60  # how often (seconds) to report

mqtt_host = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else '192.168.2.104'
mqtt_client_id = os.getenv('HOSTNAME') if os.getenv('HOSTNAME') else 'ws1-anemometer'
mqtt_topic_base = os.getenv('MQTT_TOPIC') if os.getenv('MQTT_TOPIC') else f"{mqtt_client_id}/ads-ws1"
mqtt_wind_direction_topic = f"{mqtt_topic_base}/wind_direction1"

def mqtt_on_connect():
    print('mqtt connected')

mqtt_client = mqtt.Client(client_id=mqtt_client_id)
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.connect(mqtt_host, 1883)

def get_average(angles):
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average

def get_value(length):
    data = []
    start_time = time.time()
    print(f"gathering wind_direction data for {length} seconds")
    while time.time() - start_time <= length:
        wind = round(adc.value * 3.3, 1)
        if not wind in volts:
            print(f"unknown value: {wind}")
        else:
            data.append(volts[wind])

    return get_average(data)

while True:
    wind_direction = get_value(interval)
    print(f"topic:{mqtt_wind_direction_topic} payload:{wind_direction}")
    mqtt_client.publish(mqtt_wind_direction_topic, payload=wind_direction)
