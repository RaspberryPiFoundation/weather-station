#!/usr/bin/env python3
import os
import time
import paho.mqtt.client as mqtt
from gpiozero import MCP3008

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

while True:
    adc = MCP3008(channel=0)
    resistance = adc.value
    print(f"topic:{mqtt_wind_direction_topic} payload:{resistance}")
    mqtt_client.publish(mqtt_wind_direction_topic, payload=resistance)
    time.sleep(interval)
