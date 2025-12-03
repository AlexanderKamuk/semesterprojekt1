from machine import Pin, PWM
import time

class ServoMotor:
    def __init__(self):
        #initializes GPIO16 as the pico pin for the servo motor, and sets the frequency to 50 hz
        self.servo_pin=Pin(16)
        self.servo=PWM(self.servo_pin) #initialize PWM on pin 16
        self.servo.freq(50)


    def DegreeServo(self):
            #calculates the positions for the servo.(regulated through testing)
        self.duty=65535 #max duty cycle for 16 bit
        self.deg_0	= int(0.5 / 20 * self.duty) #0 degrees
        self.deg_90	= int(1.55 / 20 * self.duty) #90 degrees
        self.deg_180	= int(2.5 / 20 * self.duty) #180 degrees

    #Moves the servo to the given positions
    def servo0deg(self):
        self.servo.duty_u16(self.deg_0) #0 degrees
    def servo90deg(self):
        self.servo.duty_u16(self.deg_90) #90 degrees
    def servo180deg(self):
        self.servo.duty_u16(self.deg_180) #180 degrees