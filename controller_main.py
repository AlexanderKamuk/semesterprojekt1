from DifferentialDrive import DifferentialDrive
from machine import ADC, Pin, Timer
from DisplayControllor import Display

import time

# ADC pins
adcx = ADC(Pin(26))
adcy = ADC(Pin(27))

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

# Emergency stop parameters
emergencyStop = Pin(14, Pin.IN, Pin.PULL_DOWN)
emergency_stop = 0

#Display setup
sda_pin=8
scl_pin=9
display=Display(sda_pin,scl_pin)
display.clear() # Clear display

# Define emergency stop function
def button_check(pin):
    if emergencyStop.value() == 1:   # Activate if button is pressed
        global emergency_stop
        display.writeText0("Emergency stop initiated")
        display.addLine1("initialized")
        #print("Emergency stop initiated")
        time.sleep(0.3)   # Debounce
        speed_mode_vis.value(0) # Turn off speed-mode-visualisation-LED
        emergency_stop = 1 # Change value of main loop dependant variable to exit main loop

time.sleep(1)

# Call in emergency stop as an interrupt
emergencyStop.irq(button_check)   # Call in the emergency button check

# Main loop
while emergency_stop == 0:
    ReadVoltage() # Check button state
    #time.sleep(0.1)
    #print("active")
    # Speed mode change
    if voltagey == 3.3 and (1 < voltagex < 2): # React if joystick button is pressed
        time.sleep(0.2) # Debounce
        Pin.toggle(speed_mode_vis) # Toggle LED on/off
        #print(speed_mode_vis.value())
        if speed_mode_vis.value() == 0: # Activate slow mode
            delay_us = max_delay_us
            display.writeText2("Minimum speed")
            display.addLine3("achieved")
        else: # Activate normal mode
            delay_us = min_delay_us
            display.writeText2("Full speed")
            display.addLine3("ahead!")
    
    # Controller movement interpretation
    if voltagex < 1 and (1 < voltagey < 2): # Joystick is turned to the left
        turnLeft.move(dist_turn, direction, delay_us, move_unit)
    elif voltagex > 2 and (1 < voltagey < 2): # Joystick is turned to the Right
        turnRight.move(dist_turn, direction, delay_us, move_unit)
    elif (3.3 > voltagey > 2) and (1 < voltagex < 2): # Joystick is turned backward and joystick button is not pressed
        straight.move(dist_straight, "backward", delay_us, move_unit)
    elif voltagey < 1 and (1 < voltagex < 2): # Joystick is turned forward
        straight.move(dist_straight, "forward", delay_us, move_unit)
    else: # Joystick is untouched
        pass

# Stop all motors and confirm full stop
straight.stop()
display.addLine3("Succesfully")
display.addLine4("stopped")

#print("Succesfully stopped")