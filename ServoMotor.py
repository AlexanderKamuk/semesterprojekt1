from machine import Pin, PWM
import time

#initializes GPIO16 as the pico pin for the servo motor, and sets the frequency to 50 hz
servo_pin=("GP16")
servo=PWM(servo_pin)
servo.freq(50)



#calculates the positions for the servo.(regulated through testing)
duty=65535
deg_0	= int(0.5 / 20 * duty)
deg_90	= int(1.55 / 20 * duty)
deg_180	= int(2.5 / 20 * duty)

#Moves the servo to the given positions
servo.duty_u16(deg_0)
time.sleep(2)
servo.duty_u16(deg_90)
time.sleep(2)
servo.duty_u16(deg_180)
time.sleep(2)