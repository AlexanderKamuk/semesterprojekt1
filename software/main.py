from LDRx5_turn_reactionV1 import TrackDriving
from MagnetClass import Electromagnet 
import time
from machine import Pin
#Initializations
Drive = TrackDriving()
#Drive.runrobot() to follow track

magnet = Electromagnet()
#magnet.start()
#magnet.stop()

#actuator Pin
actuatorpin=Pin(11, Pin.OUT)
actuatorpin.value(0)

#States
def straightline():
    global count 
    Drive.runrobot() #start moving forward
    if Drive.voltageR2 <0.22: #Value for detecting Black
        time.sleep(1) #small debounce
        if Drive.voltageR2 < 0.22: #Value for detecting Black
            magnet.start()
            Drive.leftturnrobot() # 90 degree turn to the left
            #Actuator - roll out 
            Pin.toggle(actuatorpin)
            time.sleep(0.01)
            Pin.toggle(actuatorpin)
            time.sleep(7) #wait time for roll out
            Drive.wiggle()
            #Actuator - roll in
            Pin.toggle(actuatorpin)
            time.sleep(0.01)
            Pin.toggle(actuatorpin)
            magnet.stop()
            Drive.rightturnrobot() # 90 degree turn to the right to face the line again
    elif Drive.voltageL2 < 0.2: #Value for detecting Black
        time.sleep(0.3) #small debounce
        if Drive.voltageL2 < 0.2: #Value for detecting Black
            magnet.start()
            Drive.rightturnrobot() # 90 degree turn to the right
            #Actuator - roll out 
            Pin.toggle(actuatorpin)
            time.sleep(0.01)
            Pin.toggle(actuatorpin)
            time.sleep(7)#wait time for roll out
            Drive.wiggle()
            #Actuator - roll in
            Pin.toggle(actuatorpin)
            time.sleep(0.01)
            Pin.toggle(actuatorpin)
            magnet.stop()
            Drive.leftturnrobot() # 90 degree turn to the right to face the line again
            count += 1
            print("first state done")
def straightline2(): #state to ignore left and right readings
    global count
    Drive.runrobot() # keep moving forward
    if Drive.voltageR2 < 0.3 and Drive.voltageL2 < 0.3:
        count +=1 # move to next state
        print("second state done")
    Drive.runrobot()
    
def home1line1(): #return home
    global count
    Drive.rightturnrobot()
    Drive.rightturnrobot()
    count += 1
def home2line1():
    Drive.runrobot() #move forward
    if Drive.voltageR1 < 0.2 and Drive.voltageM < 0.2 and Drive.voltageL1 < 0.2:
        time.sleep(2) #give time to fully reach home position
        Drive.rightturnrobot()
        Drive.rightturnrobot()
        count += 1

def line2():
    global count
    Drive.runrobot()
    if Drive.voltageR2 < 0.25 and Drive.voltageL2 < 0.2:
        Drive.leftturnrobot()
        count += 1
def line2pickup():
    global count
    Drive.runrobot()
    if Drive.voltageR2 < 0.25:
        time.sleep(0.1)
        if Drive.voltageR2 < 0.25:
            magnet.start()
            Drive.rightturnrobot()
            #Actuator - roll out 
#            Pin.toggle(pin_navn)
#            time.sleep(0.01)
#            Pin.toggle(pin_navn)
            
#            time.sleep(7) #wait time for roll out
            #needs wiggle function
            
            #Actuator - roll in
#            Pin.toggle(pin_navn)
#            time.sleep(0.01)
#            Pin.toggle(pin_navn)
            magnet.stop()
            Drive.leftturnrobot()
            count += 1 #2 right side pick ups, so this code needs to run twice in a row
            
def home2():
    global count
    if Drive.voltageR1 < 0.2 and Drive.voltageR2 < 0.25 and Drive.voltageL2 < 0.2 and Drive.voltageL1 < 0.2:
        Drive.leftturnrobot()
        Drive.leftturnrobot()
        Drive.runrobot()
        if (Drive.voltageR1 < 0.2 and Drive.voltageR2 < 0.25 and Drive.voltageL2 < 0.2 and Drive.voltageL1 < 0.2 or
        Drive.voltageR1 > 0.3 and Drive.voltageR2 > 0.3 and Drive.voltageL2 > 0.3 and Drive.voltageL1 > 0.3):
            Drive.rightturnrobot()
            Drive.runrobot()
            
#time.sleep(3)
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
        home1line1()
    
    #turn left to line 2
    if count == 5:
        home2line1()

    if count in (6, 7):
        line2()
    
    if count == 8:
        line2pickup()
        
    if count == 9:
        home2()
    time.sleep(0.01)#to prevent CPU overload
        
    
