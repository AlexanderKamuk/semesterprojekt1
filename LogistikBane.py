from LDR_Turn_ReactionClassV3 import TrackDriving
from MagnetClass import Electromagnet 

Drive = TrackDriving()
#Drive.runrobot() to continously run (meant to Trackdriving)
#Drive.singlecheck meant to run until stopped
magnet = Electromagnet()
#magnet.start()
#magnet.stop()

#States
def nut1():
    global count
    Drive.singlecheck()
    if Drive.voltageR >= 1: #1 er bare for at have en værdi, værdien skal reelt være når læser sort, så når den er mindre en værdien hvid
        return # exit function early 
    #turn to spot
    Drive.rightturnrobot
    magnet.start()
    #turn front to start
    Drive.rightturnrobot
    count += 1
        
def home1(): #return home
    global count
    Drive.singlecheck()
    if Drive.voltageR < 1: return
    if Drive.voltageM < 1: return
    if Drive.voltageL < 1: return
    magnet.stop()
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

#def nut3()


count = 1

"""if voltageM or voltageL <?:
    count +=1"""

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
    while count == 5"""

