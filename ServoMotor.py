from machine import Pin, PWM
import time

class ServoMotor:
    def __init__(self):
        #initializes GPIO16 as the pico pin for the servo motor, and sets the frequency to 50 hz
        self.servo_pin=Pin(16)
        self.servo=PWM(self.servo_pin)
        self.servo.freq(50)


    def DegreeServo(self):
            #calculates the positions for the servo.(regulated through testing)
        self.duty=65535
        self.deg_0	= int(0.5 / 20 * self.duty)
        self.deg_90	= int(1.55 / 20 * self.duty)
        self.deg_180	= int(2.5 / 20 * self.duty)

    #Moves the servo to the given positions
    def servo0deg(self):
        self.servo.duty_u16(self.deg_0)
    def servo90deg(self):
        self.servo.duty_u16(self.deg_90)
    def servo180deg(self):
        self.servo.duty_u16(self.deg_180)