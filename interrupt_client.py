#!/usr/bin/python
import time, os, sys, socket, thread

class interrupt_client(object):
    def __init__(self, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", port))
        assert(self.get_data() == "OK")
        print("Connected to interrupt daemon")
            
    def get_data(self):
        buf = self.client.recv(128)
        return buf.strip()
        
    def send_command(self, command):
        self.client.sendall(command)
        data = self.get_data()
        try:
            return float(data)
        except ValueError:
            return None

    def get_rain(self):
        return self.send_command("RAIN")

    def get_wind(self):
        return self.send_command("WIND")
        
    def get_wind_gust(self):
        return self.send_command("GUST")
        
    def reset(self):
        self.client.sendall("RESET")
        assert(self.get_data() == "OK")
        print("Counts reset")
        
    def __del__(self):
        self.client.sendall("BYE")
        self.client.close()
        print("Connection closed")
