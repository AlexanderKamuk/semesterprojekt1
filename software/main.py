from LDRx5_turn_reactionV1 import TrackDriving
from MagnetClass import Electromagnet 
import time
from machine import ADC, Pin
#Initializations
Drive = TrackDriving()
#Drive.runrobot() to continously run (meant to Trackdriving)
#Drive.singlecheck meant to run until stopped
magnet = Electromagnet()
#magnet.start()
#magnet.stop()

#States
def straightline():
    global count 
    Drive.runrobot() #start moving forward
    if Drive.voltageR2 <0.2: #Value for detecting Black
        time.sleep(0.05) #small debounce
        if Drive.voltageR2 < 0.2: #Value for detecting Black
            magnet.start()
            Drive.rightturnrobot() # 90 degree turn to the right
            #needs the actuator to start here, so the nut can be picked up
    #        Pin.toggle(pin_navn)
    #        time.sleep(0.01)
    #        Pin.toggle(pin_navn)
            # wait time

            #needs the actuator to come back here after picking up the nut
    #        Pin.toggle(pin_navn)
    #        time.sleep(0.01)
    #        Pin.toggle(pin_navn)
            magnet.stop()
            Drive.leftturnrobot() # 90 degree turn to the left to face the line again

    elif Drive.voltageL2 < 0.2: #Value for detecting Black
        time.sleep(0.05) #small debounce
        elif Drive.voltageL2 < 0.2: #Value for detecting Black
            Drive.leftturnrobot() # 90 degree turn to the left
            magnet.start()
            #needs the actuator to start here, so the nut can be picked up
            #needs the actuator to come back here after picking up the nut
            magnet.stop()
            Drive.rightturnrobot() # 90 degree turn to the right to face the line again
            count += 1

def straightline2(): #state to ignore left and right readings
    Drive.runrobot() # keep moving forward
    if Drive.voltageR2 < 0.2 and Drive.voltageL2 < 0.2:
        count +=1 # move to next state

def home1(): #return home
    global count
    Drive.rightturnrobot()
    Drive.rightturnrobot()
    Drive.runrobot() #move forward
    if Drive.voltageR1 < 0.2 and Drive.voltageM < 0.2 and Drive.voltageL1 < 0.2:
        time.sleep(2) #give time to fully reach home position
        Drive.rightturnrobot()
        Drive.rightturnrobot()
        count += 1

count = 1
while True:
    #state 1
    if count == 1:
        straightline()
        

    #state 2
    if count == 2:
        straightline2() 

    #state 3
    if count == 3:
        straightline()

    #state 4
    if count == 4:
        home1()     
