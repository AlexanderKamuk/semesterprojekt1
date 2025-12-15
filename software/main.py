from LDRx5_turn_reactionV1 import TrackDriving
from MagnetClass import Electromagnet 
import time
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
            #Actuator - roll out 
            Pin.toggle(pin_navn)
            time.sleep(0.01)
            Pin.toggle(pin_navn)
            
            #needs wait time
            #needs wiggle function
            
            #actuator roll in
            Pin.toggle(pin_navn)
            time.sleep(0.01)
            Pin.toggle(pin_navn)
            magnet.stop()
            Drive.leftturnrobot() # 90 degree turn to the left to face the line again
    elif Drive.voltageL2 < 0.2: #Value for detecting Black
        time.sleep(0.05) #small debounce
        if Drive.voltageL2 < 0.2: #Value for detecting Black
            magnet.start
            Drive.leftturnrobot() # 90 degree turn to the left
            #Actuator - roll out 
            Pin.toggle(pin_navn)
            time.sleep(0.01)
            Pin.toggle(pin_navn)
            
            #needs wait time
            #needs wiggle function
            
            #actuator roll in
            Pin.toggle(pin_navn)
            time.sleep(0.01)
            Pin.toggle(pin_navn)
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

def line2():
    Drive.runrobot()
    if Drive.voltageR2 < 0.2 and Drive.voltageL2 < 0.2:
        Drive.leftturnrobot()
        count += 1
def line2pickup():
    Drive.runrobot()
    if Drive.voltageR2 < 0.2:
        time.sleep(0.1)
        if Drive.voltageR2 < 0.2:
            magnet.start()
            Drive.rightturnrobot()
            #Actuator - roll out 
            Pin.toggle(pin_navn)
            time.sleep(0.01)
            Pin.toggle(pin_navn)
            
            #needs wait time
            #needs wiggle function
            
            #actuator roll in
            Pin.toggle(pin_navn)
            time.sleep(0.01)
            Pin.toggle(pin_navn)
            magnet.stop()
            Drive.leftturnrobot()
            count += 1 #2 right sides, so in needs to run count += 1, 2 times before switching to new state
            

count = 1
while True:
    #first part of first line
    if count == 1:
        straightline()
        

    #second part of first line
    if count == 2:
        straightline2() 

    #third part of first line
    if count == 3:
        straightline()

    #back to start
    if count == 4:
        home1()
    
    
