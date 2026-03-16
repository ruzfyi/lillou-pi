from gpiozero import LEDBoard
import time

class Keypad:
    def __init__(self, m1_1 = 19, m1_2 = 26, m2_3 = 13, m2_4 = 6, m3_1 = 12, m3_2 = 16, m4_3 = 20, m4_4 = 21):
        self.m1_in1 = m1_1
        self.m1_in2 = m1_2

        self.m2_in3 = m2_3
        self.m2_in4 = m2_4

        self.m3_in1 = m3_1
        self.m3_in2 = m3_2

        self.m4_in3 = m4_3
        self.m4_in4 = m4_4

        self.tis_pins = LEDBoard(
                self.m1_in1, 
                self.m1_in2, 
                self.m2_in3, 
                self.m2_in4, 
                self.m3_in1, 
                self.m3_in2, 
                self.m4_in3, 
                self.m4_in4
        )

    def run(self):
        print("Running actuators")
        
        # 3
        self.tis_pins.value = (0, 0, 0, 0, 1, 0, 1, 0)
        time.sleep(1)
        # -7
        self.tis_pins.value = (0, 0, 0, 0, 0, 1, 1, 0)
        time.sleep(1)
        # -3
        self.tis_pins.value = (0, 0, 0, 0, 0, 1, 0, 1)
        time.sleep(1)
        # 7
        self.tis_pins.value = (0, 0, 0, 0, 1, 0, 0, 0)
        time.sleep(1)
        # 3
        self.tis_pins.value = (0, 0, 0, 0, 1, 0, 1, 0)
        time.sleep(1)
        # -7
        self.tis_pins.value = (0, 0, 0, 0, 0, 1, 1, 0)
        time.sleep(1)
        # -3
        self.tis_pins.value = (0, 0, 0, 0, 0, 1, 0, 1)
        time.sleep(1)
        # 8
        self.tis_pins.value = (1, 0, 0, 0, 0, 0, 0, 1)
        time.sleep(1)
        # pound
        self.tis_pins.value = (1, 0, 1, 0, 0, 0, 0, 0)
        time.sleep(1)
        # -8
        self.tis_pins.value = (0, 1, 1, 0, 0, 0, 0, 0)
        time.sleep(1)
        # reset
        self.tis_pins.value = (0, 1, 0, 1, 0, 1, 0, 1)
        time.sleep(2)
        print("Done")

    def prep(self):
        print("Prepping actuator")
        # 7
        self.tis_pins.value = (0, 0, 0, 0, 1, 0, 0, 0)
        time.sleep(0.5)
        self.tis_pins.value = (0, 0, 0, 0, 0, 0, 0, 0)
        time.sleep(0.5)
    
    def full_reset(self):
        self.tis_pins.value = (0, 1, 0, 1, 0, 1, 0, 1)
        time.sleep(3)
