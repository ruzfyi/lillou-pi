from gpiozero import Servo
import time

class Step_servo:
	def __init__(self, Pin, min, max):
		self.servo = Servo(Pin, min_pulse_width= float(min), max_pulse_width= float(max))
	
	def max_position(self):
		self.servo.max()
		time.sleep(2)

	def mid_position(self):
		self.servo.mid()
		time.sleep(2)
	
	def min_position(self):
		self.servo.min()
		time.sleep(2)

	def servo_detach(self):
		self.servo.detach()

	def servo_value(self, position):
		self.servo.value = float(position)


#Continue testing position  value testing

#min_pulse_width=0.0005, max_pulse_width=0.0024
#mini_bot_servo = step_servo(12, 0.0005, 0.0024)

#mini_bot_servo.servo_value(0)
#print("Initial position")
#time.sleep(2)

#mini_bot_servo.servo_value(-0.5)
#print("Final")
#time.sleep(2)



