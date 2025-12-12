from StepperClass import StepperMotor
import math

# Motor pins
pins=[0,1,2,3]

# Step mode
stepmode="MICRO"

# Percent of max pwm
pwm_pct=70 # Practice PCB is used, so a higher pwm_pct is required

# Frequency
freq=18_000

# Microsteps per full step
microsteps=16

# Distance to move
dist=1600

# Unit of dist ("steps", "cm" or "degree")
unit="steps"

if unit == "degree": # Convert from degrees to steps
    dist=dist/1.8
elif unit == "cm": # Convert from cm to steps
    diameter=8.6*(1+0.0145)*(1+0.002) # Measured in cm, regulated through earlier testing in DifferentialDrive
    circumference=math.pi*diameter
    dist=circumference/360*dist

# Direction of movement
direction="forward"

# Delay in us
delay_us=1000

motor=StepperMotor(pins, stepmode, pwm_pct, freq, microsteps)
motor.move_stepper(dist,direction,delay_us)
print("done")