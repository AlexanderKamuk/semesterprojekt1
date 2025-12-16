# Source: Electrocredible.com, Language: MicroPython

# Import necessary modules
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time


class Display:
    def __init__(self,sda=8,scl=9):
        # Pin numbers for I2C communication
        sda_pin=Pin(sda)
        scl_pin=Pin(scl)
        # Display dimensions
        WIDTH =128 
        HEIGHT= 64
        # Set up I2C communication
        i2c=I2C(0,scl=scl_pin,sda=sda_pin,)
        time.sleep(0.1)
        # Initialize SSD1306 display with I2C interface
        self.oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
    def clear(self):
        self.oled.fill(0)
        self.oled.show()
    def test(self):
        # text, x-position, y-position
        self.oled.text("Hello,", 42, 20)
        self.oled.text("World !", 38, 40)
        # Show the updated display
        self.oled.show()
        
    def writeText0(self,message):
        self.oled.fill(0)
        self.oled.text(message,5,5)
        self.oled.show()
    def writeText1(self,message):
        self.oled.fill(0)
        self.oled.text(message,5,15)
        self.oled.show()
    def writeText2(self,message):
        self.oled.fill(0)
        self.oled.text(message,5,25)
        self.oled.show()
    def writeText3(self,message):
        self.oled.fill(0)
        self.oled.text(message,5,35)
        self.oled.show()
    def writeText4(self,message):
        self.oled.fill(0)
        self.oled.text(message,5,45)
        self.oled.show()
    def writeText5(self,message):
        self.oled.fill(0)
        self.oled.text(message,5,55)
        self.oled.show()
    
    def addLine0(self,message):
        self.oled.text(message, 5, 5)
        self.oled.show()
    def addLine1(self,message):
        self.oled.text(message, 5, 15)
        self.oled.show()
    def addLine2(self,message):
        self.oled.text(message, 5, 25)
        self.oled.show()
    def addLine3(self,message):
        self.oled.text(message, 5, 35)
        self.oled.show()
    def addLine4(self,message):
        self.oled.text(message, 5, 45)
        self.oled.show()
    def addLine5(self,message):
        self.oled.text(message, 5, 55)
        self.oled.show()
        

"""
display=Display(8,9)
if True:
    display.showText0("Line 1 test")
    display.addLine1("Line 2 test")
    display.addLine2("Line 3 test")
    display.addLine3("Line 4 test")
    display.addLine4("Line 5 test")
    display.addLine5("Line 6 test")
"""