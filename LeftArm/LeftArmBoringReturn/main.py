from LDR5V2 import TrackDriving
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
actuatorpin=Pin(12, Pin.OUT)
actuatorpin.value(0)

#Thresholds
thresholdL2= 0.1
thresholdL1= 0.1
thresholdM = 0.1
thresholdR1= 0.15
thresholdR2= 0.05
#States
def straightline():
    global count
    Drive.runrobot() #start moving forward
    if Drive.voltageR2 <thresholdR2 or Drive.voltageR1 < thresholdR1: #Value for detecting Black
        time.sleep(0.5) #small debounce
        if Drive.voltageR2 < thresholdR2 or Drive.voltageR1 <thresholdR1: #Value for detecting Black
            Drive.reverse5cm()
            Drive.leftturnrobot() # 90 degree turn to the left
            magnet.start()
            
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
            time.sleep(8)
            
            magnet.stop()
            time.sleep(2)# wait time for the nut to fall into the box
            Drive.rightturnrobot() # 90 degree turn to the right to face the line again
            Drive.straight(15)
            count += 1
            print(count)
def ignore():
    global count
    Drive.runrobot()
    if Drive.voltageR1 < thresholdR1 or Drive.voltageR2 < thresholdR2:
        Drive.straight(10)
        count += 1
        print(count)
def fullturn():
    global count
    Drive.runrobot()
    if Drive.voltageL2 < thresholdL2 and Drive.voltageL1 < thresholdL1 and Drive.voltageM < thresholdM:
        Drive.turn(200)
        count += 1
        print(count)
    
    
    
 
time.sleep(3)
count = 1
while True:
    #first part of first line
    if count == 1:
        ignore()
    if count == 2:
        ignore()
    if count == 3:
        Drive.turn(70,"left")
        Drive.straight(15)
        count += 1
    if count == 4:
        straightline()
    if count == 5:
        Drive.turn(15,"left")
        count += 1
    if count == 6:
        straightline()
    if count == 7:
        Drive.turn(160,"left")
        count += 1
    if count == 8:
        ignore()
    if count == 9:
        Drive.turn(90)
        count += 1
    if count == 10:
        ignore()
    if count == 11:
        Drive.runrobot()



