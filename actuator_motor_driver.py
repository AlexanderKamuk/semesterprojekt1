from StepperClass import StepperMotor
from machine import Pin
import time
import math

# Motor pins
pins=[0,1,2,3]

# Step mode
stepmode="MICRO"

# Percent of max pwm
pwm_pct=80 # Practice PCB is used, so a higher pwm_pct is required

# Frequency
freq=18_000

# Microsteps per full step
microsteps=20

# Distance to move
dist=1600

# Unit of dist ("steps", "cm" or "degree")
unit="steps"

if unit == "degree": # Convert from degrees to steps
    dist=dist/1.8*microsteps
elif unit == "cm": # Convert from cm to steps
    diameter=8.6*(1+0.0145)*(1+0.002) # Measured in cm, regulated through earlier testing in DifferentialDrive
    circumference=math.pi*diameter
    dist=circumference/360*dist*microsteps

# Direction of movement
directionPos="forward"
directionNeg="backward"

# Delay in us
delay_us=1000

# Initiate generel movement class
motor=StepperMotor(pins, stepmode, pwm_pct, freq, microsteps)

# Define signal pin
signal=Pin("GP11", Pin.IN, Pin.PULL_DOWN)

directionModes=[directionPos,directionNeg]
mode_idx=0

# Main loop
while True:
    if signal.value() == 1: # Activate if signal pin is triggered
        motor.move_stepper(dist,directionModes[mode_idx],delay_us) # Move actuator in given direction
        print("moving "+directionModes[mode_idx]) # Print movement direction
        mode_idx=(mode_idx+1)%len(directionModes) # Switch movement direction
    else:
        pass

print("ERROR: MAIN LOOP ENDED")