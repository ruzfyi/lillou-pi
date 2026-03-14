#import Servo_driver as LServos
from LCD_driver import LCD
#from ESP32_driver import ESP32
#from Keypad_driver import Keypad
import time, serial

display = LCD(addr=0x3F) # LCD init
#esp = ESP32(port='/dev/ttyUSB0') # comm with esp
pico = serial.Serial('/dev/ttyACM0', 115200, timeout=1) # comm with pico
#keypad = Keypad() # keypad init

colors = [] # list for the colors

"""
The supposed order for the colors is 1 -> 4 -> 2 -> 3
"""

def send_command(cmd):
    pico.write((cmd+'\n').encode('utf-8'))
    line = pico.readline().decode('utf-8').rstrip()
    return line

def pico_msg():
    line = pico.readline().decode('utf-8').rstrip()
    return line

display.clear()
"""
# This script performs a sanity check for the ESP connection
display.message("CHECK ESP", line=1)

if (esp.connect()):
    display.message("GOOD CONN", line=2)
    time.sleep(0.5)
else:
    while True:
        display.message("ESP NO CONN", line-2)

display.clear()
display.message("COLOR", line=1)

color = esp.get_color(timeout=10)

if color:
    display.message(color, line=2)
else:
    display.message("ERROR", line=2)

display.clear()
"""
display.message("CHECK PICO", line=1)

response = send_command("SYS_CHECK")

display.message(response, line=2)

time.sleep(0.5)

display.clear()

display.message("PICO REC", line=1)

# snippet for waiting for the pico response
waiting = True

while waiting:
    response = pico_msg()
    if response == "True":
        waiting = False
        display.message(response, line=2)
        print("PICO", response)
        time.sleep(1)
