import smbus
import time
class lcd:
    # Define some device parameters
    I2C_ADDR  = 0 # I2C device address
    LCD_WIDTH = 0   # Maximum characters per line

    # Define some device constants
    LCD_CHR = 1 # Mode - Sending data
    LCD_CMD = 0 # Mode - Sending command

    LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
    LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
    LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

    LCD_BACKLIGHT       = 0x08  # On
    LCD_BACKLIGHT_OFF   = 0x00  # Off

    ENABLE = 0b00000100 # Enable bit

    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005
    BACKLIGHTTOGGLED = False
    bus = smbus.SMBus(1) # Rev 2 Pi uses 1

    def __init__(self, addr, rows):
        self.I2C_ADDR = addr
        self.LCD_WIDTH = rows
    
    def lcd_init(self):
      # Initialise display
      self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
      self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
      self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
      self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
      self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
      self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
      time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
      # Send byte to data pins
      # bits = the data
      # mode = 1 for data
      #        0 for command

      bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
      bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT

      # High bits
      self.bus.write_byte(self.I2C_ADDR, bits_high)
      self.lcd_toggle_enable(bits_high)

      # Low bits
      self.bus.write_byte(self.I2C_ADDR, bits_low)
      self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
      # Toggle enable
      time.sleep(self.E_DELAY)
      self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
      time.sleep(self.E_PULSE)
      self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
      time.sleep(self.E_DELAY)

    def lcd_toggle_backlight(self, onoff):
        if(onoff == 1):
            self.bus.write_byte(self.I2C_ADDR, 0x08)
        elif(onoff == 0):
            self.bus.write_byte(self.I2C_ADDR, 0x00)

        self.BACKLIGHTTOGGLED != self.BACKLIGHTTOGGLED
    def lcd_string(self, message,line):
      # Send string to display

      message = message.ljust(self.LCD_WIDTH," ")

      self.lcd_byte(line, self.LCD_CMD)

      for i in range(self.LCD_WIDTH):
        self.lcd_byte(ord(message[i]),self.LCD_CHR)

    def lcd_close(self):
        self.lcd_byte(0x01, self.LCD_CMD)
