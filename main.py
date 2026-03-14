# version 3 program

#from Step_servo import Step_servo
from LCD_driver import LCD
from ESP32_driver import ESP32
from Keypad_driver import Keypad
import time, serial

display = LCD(addr=0x3F) # LCD init
#esp = ESP32(port='/dev/ttyUSB0') # comm with esp
pico = serial.Serial('/dev/ttyACM0', 115200, timeout=1) # comm with pico
keypad = Keypad() # keypad init

colors = ["","","",""] # list for the colors

"""
The supposed order for the colors is 1 -> 4 -> 2 -> 3
"""

def send_command(cmd):
    pico.write((cmd+'\n').encode('utf-8'))
    line = pico.readline().decode('utf-8').strip()
    return line

def pico_msg():
    line = pico.readline().decode('utf-8').strip()
    return line

print("functions initialized")

print("testing esp")

display.clear()
"""
# This portion performs a sanity check for the ESP connection
display.message("CHECK ESP", line=1)

if (esp.connect()):
    display.message("GOOD CONN", line=2)
    time.sleep(0.5)
else:
    while True:
        display.message("ESP NO CONN", line-2)

display.clear()
display.message("ESP OKAY", line=1)

time.sleep(0.5)
"""

print("esp tested")

display.clear()
display.message("PI READY", line=1)

print("testing pico")

# Make sure PICO is connected 
response = send_command("PI_READY")
print("PICO:",response)
if response == "ACK: OK":
    print("pico passed")
    display.message("PICO READY", line=2)
    time.sleep(0.5)
else:
    print("pico failed")
    print(response)
    while True:
        display.message("RED BUZZER", line=2)

# Reset all the servos
keypad.full_reset()
#minibot_servo.servo_value(-0.5)

# STAND BY mode
display.clear()
display.message("STANDING BY", line=1)

waiting = True
while waiting:
    response = pico_msg()
    print(response)
    if response == "START":
        waiting = False
        display.clear()
        display.message("STARTED", line=1)
        print("PI: STARTING RUN")

# Start run

"""
Release camera
"""

"""
Get camera into position for button
"""
display.clear()
display.message("KEYPAD", line=1)
waiting = True
while waiting:
    response = pico_msg()
    print(response)
    if response == "AT_KEYPAD":
        keypad.run()
        waiting = False
        display.message("DOING",line=2)

print("Doing camera")
colors[1] = esp.get_color()

response = send_command("KEYPAD_DONE")

if response == "ACK: OK":
    display.clear()
    display.message("KEYPAD", line=1)
    display.message("DONE", line=2)
