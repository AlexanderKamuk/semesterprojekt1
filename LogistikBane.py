from LDR_Turn_ReactionClassV3 import TrackDriving
from MagnetClass import Electromagnet 

Drive = TrackDriving()
#Drive.runrobot()

magnet = Electromagnet()
#magnet.start()
#magnet.stop()

#States
def nut1():
    global count
    Drive.singlecheck()
    if voltageR >= ?:
        return # exit function early 
    #turn to spot
    Drive.rightturnrobot
    magnet.start()
    #turn front to start
    Drive.rightturnrobot
    count += 1
        
def home1() 2: ? #return home
    global count
    Drive.singlecheck()
    if voltageR < ?: return
    if voltageM < ?: return
    if voltageL < ?: return
    magnet.stop()
    Drive.rightturnrobot
    Drive.rightturnrobot
    count += 1
    

def nut2():
    global count
    Drive.singlecheck()
    if voltageL >= ? return
    Drive.leftturnrobot
    magnet.start
    Drive.leftturnrobot
    count +=1

def home2():
    global count
    Drive.singlecheck()
    if voltageR < ?: return
    if voltageM < ?: return
    if voltageL < ?: return
    magnet.stop()
    Drive.leftturnrobot
    Drive.leftturnrobot

#def nut3()


count = 1

if voltageM or voltageL <?:
    count +=1

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
    
    
"""
    #state 5
    while count == 5

    #state 6
    while count == 5

