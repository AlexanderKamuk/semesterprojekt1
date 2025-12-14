from LDR_Turn_ReactionClassV3 import TrackDriving
from MagnetClass import Electromagnet 
from ServoMotor import ServoMotor
import time

#Initializations
Drive = TrackDriving()
#Drive.runrobot() to continously run (meant to Trackdriving)
#Drive.singlecheck meant to run until stopped
magnet = Electromagnet()
#magnet.start()
#magnet.stop()
Actuator = ServoMotor()
#Actuator.degservo0()
#Actuator.degservo90()
#Actuator.degservo180()



#States

"""
def nut1():
    global count
    Drive.singlecheck()
    if Drive.voltageR >= 1: #1 er bare for at have en værdi, værdien skal reelt være når læser sort, så når den er mindre en værdien hvid
        return # exit function early 
    #turn to spot
    Drive.rightturnrobot
    magnet.start()
    Actuator.degservo180()
    time.sleep(1)
    Actuator.degservo0()
    magnet.stop()
    #turn front to start
    Drive.rightturnrobot 
    count += 1

def home1(): #return home
    global count
    Drive.singlecheck()
    if Drive.voltageR < 1: return
    if Drive.voltageM < 1: return
    if Drive.voltageL < 1: return
    Drive.rightturnrobot
    Drive.rightturnrobot
    count += 1
    

def nut2():
    global count
    Drive.singlecheck()
    if Drive.voltageL >= 1: return
    Drive.leftturnrobot
    magnet.start
    Drive.leftturnrobot
    count +=1

def home2():
    global count
    Drive.singlecheck()
    if Drive.voltageR < 1: return
    if Drive.voltageM < 1: return
    if Drive.voltageL < 1: return
    magnet.stop()
    Drive.leftturnrobot
    Drive.leftturnrobot

def leftside():
    global count
    Drive.singlecheck()
    if Drive.voltageL < 1: return
    if Drive.voltageM < 1: return
    if Drive.voltageR < 1: return
    Drive.leftturnrobot
    count += 1

def nut3():    
    Drive.singlecheck()
    if Drive.voltageR >= 1: return
    magnet.start()
    Drive.rightturnrobot

    Drive.leftturnrobot

    count += 1

"""




#New states

#Straight Line
def StraigtLine():
    global count
    Drive.straightrobot()
    if Drive.voltageR2 < ?:
        Drive.rightturnrobot()
        magnet.start()
        #needs the actuator to start here, so the nut can be picked up
        Pin.toggle(pin_navn)
        time.sleep(0.01)
        Pin.toggle(pin_navn)
        # wait time

        #needs the actuator to come back here after picking up the nut
        Pin.toggle(pin_navn)
        time.sleep(0.01)
        Pin.toggle(pin_navn)
        magnet.stop()
        Drive.leftturnrobot() # now the robot is turned towards the line again
        #need to add some logic so it can ignore differences in the readings from the LDRs
        Drive.straightrobot() #this functions needs to make sure the robot keeps moving.
    if Drive.voltageL2 < ?:
        Drive.leftturnrobot()
        magnet.start()
        #needs the actuator to start here, so the nut can be picked up
        #needs the actuator to come back here after picking up the nut
        magnet.stop()
        Drive.rightturnrobot() # now the robot is turned towards the line again
        #need to add some logic so it can ignore differences in the readings from the LDRs
        #need to add count +1 here to move to next part of the logic in this state
        count += 1
def straightline2(): 
    Drive.straightrobot()
    if Drive.voltageL2 < ? and Drive.voltageR2 < ?: return
    Drive.straightrobot()  
def straightline3():
    Drive.straightrobot()
    if Drive.voltageR2 < ?:
        Drive.rightturnrobot()
        magnet.start()
        #needs the actuator to start here, so the nut can be picked up
        #needs the actuator to come back here after picking up the nut
        magnet.stop()
        Drive.leftturnrobot() # now the robot is turned towards the line again
        #need to add some logic so it can ignore differences in the readings from the LDRs
        Drive.straightrobot() #this functions needs to make sure the robot keeps moving.
    

    


count = 1

while True:    #state 1
    while count == 1:
        nut1()

    #state 2
    while count == 2:
        home1()

    #state 3
    while count == 3:
        nut2()

    #state 4
    while count == 4:
        home2()
    
    

    #state 5
    while count == 5:
        leftside()

    #state 6
    while count == 5:
        nut3()
    
    #state 7
    while count == 7:
        home1()
    
    #state 8
    while count == 8:
        leftside()
    
    #state 9
    leftsidenut = 0
    while count == 9:   
        nut4()
