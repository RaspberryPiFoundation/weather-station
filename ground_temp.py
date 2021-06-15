#!/usr/bin/env python3
import os, glob, time
import paho.mqtt.client as mqtt

interval = 60  # seconds

mqtt_host = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else '192.168.2.104'
mqtt_client_id = os.getenv('HOSTNAME') if os.getenv('HOSTNAME') else 'ws1-groundtemp'
mqtt_topic_base = os.getenv('MQTT_TOPIC') if os.getenv('MQTT_TOPIC') else f"{mqtt_client_id}/ads-ws1"
mqtt_ground_temp_topic = f"{mqtt_topic_base}/ground_temp1"

def mqtt_on_connect():
    print('mqtt connected')

mqtt_client = mqtt.Client(client_id=mqtt_client_id)
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.connect(mqtt_host, 1883)

class DS18B20(object):
    def __init__(self):        
        self.device_file = glob.glob("/sys/bus/w1/devices/28*")[0] + "/w1_slave"
        
    def read_temp_raw(self):
        f = open(self.device_file, "r")
        lines = f.readlines()
        f.close()
        return lines
        
    def crc_check(self, lines):
        return lines[0].strip()[-3:] == "YES"
        
    def read_temp(self):
        temp_c = -255
        attempts = 0
        
        lines = self.read_temp_raw()
        success = self.crc_check(lines)
        
        while not success and attempts < 3:
            time.sleep(.2)
            lines = self.read_temp_raw()            
            success = self.crc_check(lines)
            attempts += 1
        
        if success:
            temp_line = lines[1]
            equal_pos = temp_line.find("t=")            
            if equal_pos != -1:
                temp_string = temp_line[equal_pos+2:]
                temp_c = float(temp_string)/1000.0
        
        return temp_c

    def read_temp_f(self):
        temp_c = self.read_temp()
        temp_f = (temp_c * 1.8) + 32
        return temp_f

if __name__ == "__main__":
    obj = DS18B20()
    while True:
        ground_temp_f = obj.read_temp_f()
        print(f"topic:{mqtt_ground_temp_topic} payload:{ground_temp_f}")
        print(mqtt_client.publish(topic=mqtt_ground_temp_topic, payload=ground_temp_f))
        time.sleep(interval)
