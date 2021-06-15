#!/usr/bin/env python3
from gpiozero import MCP3008
import time
adc = MCP3008(channel=0)

while True:
    print(adc.value)
    time.sleep(3)
