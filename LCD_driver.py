import time
from smbus2 import SMBus

class LCD:
    # Logic Constants from your implementation
    LCD_CHR = 1
    LCD_CMD = 0
    LINE_1 = 0x80
    LINE_2 = 0xC0
    ENABLE = 0b00000100
    BACKLIGHT = 0x08 # High bit to keep light on

    def __init__(self, addr=0x3F, port=1, width=16):
        self.addr = addr
        self.bus = SMBus(port)
        self.width = width
        
        # Initialization Sequence
        self._send_byte(0x33, self.LCD_CMD) # 110011 Initialise
        self._send_byte(0x32, self.LCD_CMD) # 110010 Initialise
        self._send_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
        self._send_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self._send_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
        self._send_byte(0x01, self.LCD_CMD) # 000001 Clear display
        time.sleep(0.005)

    def _toggle_enable(self, bits):
        time.sleep(0.0005)
        self.bus.write_byte(self.addr, (bits | self.ENABLE))
        time.sleep(0.0005)
        self.bus.write_byte(self.addr, (bits & ~self.ENABLE))
        time.sleep(0.0005)

    def _send_byte(self, bits, mode):
        # High bits
        bits_high = mode | (bits & 0xF0) | self.BACKLIGHT
        self.bus.write_byte(self.addr, bits_high)
        self._toggle_enable(bits_high)

        # Low bits
        bits_low = mode | ((bits << 4) & 0xF0) | self.BACKLIGHT
        self.bus.write_byte(self.addr, bits_low)
        self._toggle_enable(bits_low)

    def message(self, text, line=1):
        """Write a string to the specified line (1 or 2)."""
        target_line = self.LINE_1 if line == 1 else self.LINE_2
        
        # Pad string to match LCD width
        text = text.ljust(self.width, " ")
        
        self._send_byte(target_line, self.LCD_CMD)
        for i in range(self.width):
            self._send_byte(ord(text[i]), self.LCD_CHR)

    def clear(self):
        """Clear the display and return to home."""
        self._send_byte(0x01, self.LCD_CMD)
        time.sleep(0.005)

    def backlight_off(self):
        """Turn off the backlight."""
        self.bus.write_byte(self.addr, 0x00)
