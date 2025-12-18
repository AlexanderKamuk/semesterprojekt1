from DifferentialDriveOrigin import DifferentialDrive
from machine import ADC, Pin, Timer

import time

# ADC pins
adcx = ADC(Pin(27))
adcy = ADC(Pin(26))

# Controller communication function
def ReadVoltage():
    global voltagex
    global voltagey
    raw_valuey = adcy.read_u16()
    voltagey = raw_valuey * 3.3/65535
    raw_valuex = adcx.read_u16()
    voltagex = raw_valuex * 3.3/65535
    #print(voltagey)
    #print(voltagex)

# Motor pins
left=[0,1,2,3]
right=[4,5,6,7]

# Generel driving parameters
turn="r"
stepmode="MICRO"
microsteps_per_step=10
pwm_pct=20
turnmode="diff"
frequency=20_000

# Movement specific parameters
dist_turn=5
dist_straight=1
direction="forward"
max_delay_us=1000
min_delay_us=500
move_unit="dist"

#turnmode="curve" # experimental variable

# Generel driving class calls
turnLeft=DifferentialDrive(left, right, stepmode, microsteps_per_step, pwm_pct, "l", turnmode, frequency)
turnRight=DifferentialDrive(left, right, stepmode, microsteps_per_step, pwm_pct, "r", turnmode, frequency)
straight=DifferentialDrive(right, left, stepmode, microsteps_per_step, pwm_pct, "N/A", turnmode, frequency)

# Speed mode parameters
delay_us=max_delay_us # Start in slow mode
speed_mode_vis = Pin(13, Pin.OUT)
speed_mode_vis.value(0)

time.sleep(1)

delay_us=500
# Main loop
while True:
    ReadVoltage() # Check button state
    #time.sleep(0.5)
    #print("active")
    # Speed mode change
    """if voltagey == 3.3 and (1 < voltagex < 2): # React if joystick button is pressed
        time.sleep(0.2) # Debounce
        Pin.toggle(speed_mode_vis) # Toggle LED on/off
        #print(speed_mode_vis.value())
        if speed_mode_vis.value() == 0: # Activate slow mode
            delay_us = max_delay_us
        else: # Activate normal mode
            delay_us = min_delay_us"""
    
    # Controller movement interpretation
    if voltagex < 2 and (1 < voltagey < 3): # Joystick is turned to the left
        turnLeft.move(dist_turn, direction, delay_us, move_unit)
    elif voltagex > 3 and (1 < voltagey < 3): # Joystick is turned to the Right
        turnRight.move(dist_turn, direction, delay_us, move_unit)
    elif (3.4 > voltagey > 2.6) and (2 < voltagex < 3): # Joystick is turned backward and joystick button is not pressed
        straight.move(dist_straight, "forward", delay_us, move_unit)
    elif voltagey < 2 and (2 < voltagex < 3): # Joystick is turned forward
        straight.move(dist_straight, "backward", delay_us, move_unit)
    else: # Joystick is untouched
        pass

# Stop all motors and confirm full stop
straight.stop()
print("Succesfully stopped")