#!/usr/bin/python3
import time, os, sys, socket

class interrupt_client(object):
    def __init__(self, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", port))
        assert(self.get_data() == "OK")
        print("Connected to interrupt daemon")
            
    def get_data(self):
        buf = self.client.recv(128)
        return buf.decode('utf-8').strip()
        
    def send_command(self, command):
        self.client.sendall(command.encode('utf-8'))
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
        self.client.sendall(b"RESET")
        assert(self.get_data() == "OK")
        print("Counts reset")
        
    def __del__(self):
        self.client.sendall("BYE".encode('utf-8'))
        self.client.close()
        print("Connection closed")

if __name__ == "__main__":
    obj = interrupt_client(49501)
    print("RAIN: %s" % obj.get_rain())
    print("WIND: %s" % obj.get_wind())
    print("GUST: %s" % obj.get_wind_gust())
