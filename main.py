# version 3 program

#from Step_servo import Step_servo
from LCD_driver import LCD
from ESP32_driver import ESP32
from Keypad_driver import Keypad
import time, serial

display = LCD(addr=0x3F) # LCD init
esp = ESP32(port='/dev/ttyUSB0') # comm with esp
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

def esp_get_color():
    esp.connect()
    color = esp.get_color()
    if color:
        esp.close()
    else:
        return None
    return color

print("functions initialized")

print("testing esp")

display.clear()
# This portion performs a sanity check for the ESP connection
display.message("CHECK ESP", line=1)

if (esp.connect()):
    display.message("GOOD CONN", line=2)
    time.sleep(0.5)
    esp.close()
else:
    while True:
        display.message("ESP NO CONN", line-2)

display.clear()
display.message("ESP OKAY", line=1)

time.sleep(0.5)

print("esp tested")

display.clear()
display.message("PI READY", line=1)

print("testing pico")

"""
# Make sure PICO is connected 
response = send_command("RESET")

waiting = True
while waiting:
    response = pico_msg()
    print("PICO:", response)
    if response == "ISON":
        waiting = False
"""
response = send_command("PI_READY")
print("PICO:",response)
if response == "ACK: OK":
    print("pico passed")
    display.message("PICO READY", line=2)
    time.sleep(0.5)
else:
    print("pico failed")
    print("PICO:", response)
    while True:
        display.message("RED BUZZER", line=2)

# Reset all the servos
keypad.full_reset()

# STAND BY mode
display.clear()
display.message("STANDING BY", line=1)

waiting = True
while waiting:
    response = pico_msg()
    print("PICO:", response)
    if response == "START":
        waiting = False
        display.clear()
        display.message("STARTED", line=1)
        print("STARTING RUN")

# RUNNING -> BUTTON -> GET COLOR

waiting = True
while waiting:
    response = pico_msg()
    print("PICO:", response)
    if response == "COLOR_1_READY":
        waiting = False
        display.clear()
        display.message("COLOR 1", line=1)

colors[0] = esp_get_color()

if colors[0]:
    print("COLOR 1:", colors[0])
    print("COLORS:", colors)
    display.message("DONE", line=2)
else:
    while True:
        display.message("ERR", line=2)

response = send_command("COLOR_1_DONE")

print("PICO:", response)


if response == "ACK: OK":
    display.clear()
    display.message("KEYPAD", line=1)
else:
    while True:
        display.message("MISTIME", line=1)

keypad.prep()

time.sleep(0.5)

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
colors[1] = esp_get_color()
print("COLOR 2:", colors[1])
print("COLORS:",colors)

response = send_command("KEYPAD_DONE")
print("PICO:", response)

if response == "ACK: OK":
    print("PICO:", response)
    display.clear()
    display.message("COLOR_2_DONE", line=1)
    display.message("DONE", line=2)

waiting = True
while waiting:
    response = pico_msg()
    print("PICO:", response)
    if response == "LIST_COLORS":
        waiting = False
        display.clear()
        string_1 = colors[0] + " " + colors[1]
        # string_2 = colors[2] + colors[3]
        display.message(string_1, line=1)
        # display.message(string_2, line=2)

