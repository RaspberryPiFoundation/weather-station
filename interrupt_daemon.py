#!/usr/bin/python3
import time, os, sys, socket, math, atexit
import RPi.GPIO as GPIO
try:
    import thread
except ImportError:
    import _thread as thread

class interrupt_watcher(object):
    def __init__(self, sensorPin, bounceTime, peak_sample = 5, peak_monitor = False):
        self.interrupt_count = 0
        self.running = True
        self.interrupt_peak_count = 0
        self.interrupt_peak_max = 0
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(sensorPin, GPIO.FALLING, callback=self.interrupt_call_back, bouncetime=bounceTime)
        
        if peak_monitor:
            thread.start_new_thread(self.peak_monitor, (peak_sample,))
        
    def interrupt_call_back(self, channel):        
        self.interrupt_count += 1
        self.interrupt_peak_count += 1
    
    def get_value(self):
        return self.interrupt_count
        
    def get_peak(self):
        return self.interrupt_peak_max
        
    def reset_count(self):
        self.interrupt_count = 0
        self.interrupt_peak_count = 0
        self.interrupt_peak_max = 0
    
    def peak_monitor(self, sample_period):
        while self.running:
            time.sleep(sample_period)
            if self.interrupt_peak_count > self.interrupt_peak_max:
                self.interrupt_peak_max = self.interrupt_peak_count
            self.interrupt_peak_count = 0
        
    def __del__(self):
        self.running = False
        
class wind_speed_interrupt_watcher(interrupt_watcher):
    def __init__(self, radius_cm, sensorPin, bounceTime, calibration = 2.36):
        super(wind_speed_interrupt_watcher, self).__init__(sensorPin, bounceTime, peak_sample = 5, peak_monitor = True)
        
        circumference_cm = (2 * math.pi) * radius_cm
        self.circumference = circumference_cm / 100000.0 #circumference in km
        self.calibration = calibration
        self.last_time = time.time()
        
    def calculate_speed(self, interrupt_count, interval_seconds):
        rotations = interrupt_count / 2.0
        distance_per_second = (self.circumference * rotations) / interval_seconds
        speed_per_hour = distance_per_second * 3600
        return speed_per_hour * self.calibration
        
    def get_wind_speed(self):
        return self.calculate_speed(self.get_value(), time.time() - self.last_time)
        
    def get_wind_gust_speed(self):
        return self.calculate_speed(self.get_peak(), 5) #5 seconds
        
    def reset_timer(self):
        self.last_time = time.time()
        
class rainfall_interrupt_watcher(interrupt_watcher):
    def __init__(self, tip_volume, sensorPin, bounceTime):
        super(rainfall_interrupt_watcher, self).__init__(sensorPin, bounceTime)
        self.tip_volume = tip_volume
        
    def get_rainfall(self):
        return self.tip_volume * self.get_value()
        
class interrupt_daemon(object):
    def __init__(self, port):
        self.running = False
        self.port = port
        self.socket_data = "{0}\n"
        
    def setup(self):
        self.rain = rainfall_interrupt_watcher(0.2794, 6, 300) #Maplin rain gauge = 0.2794 ml per bucket tip, was 27 on prototype
        self.wind = wind_speed_interrupt_watcher(9.0, 5, 1) #Maplin anemometer = radius of 9 cm, was 17 on prototype
        
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.bind(("127.0.0.1", self.port))
            self.running = True
        except socket.error as e:
            print(e)
            raise
        
        self.skt.listen(10)
        
    def send(self, conn, s):
        conn.sendall(self.socket_data.format(s).encode('utf-8'))
        
    def receive(self, conn, length):
        data = conn.recv(length)
        return data.decode('utf-8')
    
    def handle_connection(self, conn):
        connected = True
        self.send(conn, "OK")    
        
        while connected and self.running:
            data = self.receive(conn, 128)
            if len(data) > 0:
                data = data.strip()
                if data == "RAIN":
                    self.send(conn, self.rain.get_rainfall())
                elif data == "WIND":                    
                    self.send(conn, self.wind.get_wind_speed())
                elif data == "GUST":
                    self.send(conn, self.wind.get_wind_gust_speed())
                elif data == "RESET":
                    self.reset_counts()
                    self.send(conn, "OK")
                elif data == "BYE":
                    connected = False
                elif data == "STOP":
                    connected = False
                    self.stop()
                
        conn.close()
        
    def reset_counts(self):
        self.rain.reset_count()
        self.wind.reset_count()
        self.wind.reset_timer()
        
    def daemonize(self):
        # do the UNIX double-fork magic, see Stevens' "Advanced Programming in the UNIX Environment" for details (ISBN 0201563177)        
        # first fork
        try:
            self.pid = os.fork()
            if self.pid > 0:
                sys.exit(0)
        except OSError as e:
            print(e)
            raise
        
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)        
        
        # second fork
        try:
            self.pid = os.fork()
            if self.pid > 0:
                sys.exit(0)
        except OSError as e:
            print(e)
            raise
            
        # close file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        
    def start(self):
        try:
            self.daemon_pid = None
            self.daemonize()
            self.daemon_pid = os.getpid()
            print("PID: %d" % self.daemon_pid)
            self.setup()
            while self.running:
                conn, addr =  self.skt.accept() #blocking call
                if self.running:
                    thread.start_new_thread(self.handle_connection, (conn,))
        except Exception:
            if self.running:
                self.stop()
        finally:
            if self.daemon_pid == os.getpid():
                self.skt.shutdown(socket.SHUT_RDWR)
                self.skt.close()
                GPIO.cleanup()
                print("Stopped")
        
    def stop(self):
        self.running = False        
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("localhost", self.port)) #release blocking call

def send_stop_signal(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", port))
    client.sendall("STOP".encode('utf-8'))
    client.close()

if __name__ == "__main__":
    server_port = 49501
    if len(sys.argv) >= 2:
        arg = sys.argv[1].upper()
        if arg == "START":
            interrupt_daemon(server_port).start()
        elif arg == "STOP":
            send_stop_signal(server_port)            
        elif arg == "RESTART":
            send_stop_signal(server_port)
            time.sleep(1)
            interrupt_daemon(server_port).start()
    else:
        print("usage: sudo {0} start|stop|restart".format(sys.argv[0]))
