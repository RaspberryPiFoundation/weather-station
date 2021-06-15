#!/usr/bin/env python3

# r1 = 10000  # ohms
r1 = 4700  # ohms
resistances = [33000, 6570, 8200, 891,
               1000, 688, 2200, 1410,
               39000, 3140, 16000, 14120,
               120000, 42120, 64900, 21880]

def voltage_divider(r1, r2, vin):
    vout = (vin * r1) / (r1 + r2)
    return round(vout, 1)

for i in range(len(resistances)):
    r = resistances[i]
    v = voltage_divider(r1, r, 3.3)
    print(f"r: {r}, v: {v}")
