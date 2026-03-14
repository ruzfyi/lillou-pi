from LCD_driver import LCD
#from ESP32_driver import ESP32
from Keypad_driver import Keypad
import time, serial

display = LCD(addr=0x3F) # LCD init
#esp = ESP32(port='/dev/ttyUSB0') # comm with esp
#pico = serial.Serial('/dev/ttyACM0', 115200, timeout=1) # comm with pico
keypad = Keypad() # keypad init

colors = [] # list for the colors

"""
The supposed order for the colors is 1 -> 4 -> 2 -> 3
"""
def line_one(string):
    display.clear()
    display.message(string, line=1)

def line_two(string):
    display.message(string, line=2)

line_one("KEYPAD")
line_two("RESETING")
keypad.full_reset()

time.sleep(2)

line_one("KEYPAD")
line_two("RUNNING")
keypad.run()

time.sleep(2)

line_one("KEYPAD")
line_two("DONE")
