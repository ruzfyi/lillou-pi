import serial
import time

class ESP32:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.prefix = "CAMERAPROG: RPISEND: "
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(
                    self.port,
                    self.baudrate,
                    timeout=1,
                    xonxoff=False,
                    rtscts=False,
                    dsrdtr=False
                )

            self.ser.dtr = False
            self.ser.rts = False
            time.sleep(0.1)
            self.ser.dtr = True

            print(f"Connected to {self.port} and Reset triggered")
            time.sleep(2)
            return True
        except serial.SerialException as e:
            print(f"Connection Error: {e}")
            return False
    
    def get_color(self, timeout=10):
        if not self.ser or not self.ser.is_open:
            print("Driver not connected.")
            return None

        start_time = time.time()
        while (time.time() - start_time) < timeout:
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if self.prefix in line:
                        color = line.split(self.prefix)[-1].strip()
                        return color
                except Exception as e:
                    print(f"Read error: {e}")
        print("Timed out waiting for ESP32 color output.")
        return None

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
