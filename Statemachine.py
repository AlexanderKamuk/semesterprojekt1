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


#5LDR's start code
"""
adc = ADC(Pin(26))

activationPins=[22,19,18]
signalPins=[Pin(pin,Pin.OUT) for pin in activationPins]

sequence=[
    [1,0,0],
    [0,1,0],
    [0,0,1],
    [0,0,0],
    [0,1,1]
    ]

def set_pins(combination):
    for pin, value in zip(signalPins, combination):
        pin.value(value)

def ReadVoltage():
    self.set_pins(sequence[0])
    raw_valueL2 = adc.read_u16()
    voltageL2 = raw_valueL2 * 3.3/65535
    
    self.set_pins(sequence[1])
    raw_valueL1 = adc.read_u16()
    voltageL1 = raw_valueL1 * 3.3/65535
    
    set_pins(sequence[2])
    raw_valueM = adc.read_u16()
    voltageM = raw_valueM * 3.3/65535
    
    set_pins(sequence[3])
    raw_valueR1 = adc.read_u16()
    voltageR1 = raw_valueR1 * 3.3/65535
    
    set_pins(sequence[4])
    raw_valueR2 = adc.read_u16()
    voltageR2 = raw_valueR2 * 3.3/65535
    print(voltageL2, "            ",voltageR2)
    #print([voltageL2,voltageL1,voltageM,voltageR1,voltageR2])


"""
"""
while True:
    ReadVoltage()
    time.sleep(0.1)"""
#5 ldr's end code

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

def straightline():
    Drive.runrobot()
    global count
    if Drive.voltageR2 <0.15:
        time.sleep(0.05) #small debounce
        if Drive.voltageR2 < 0.15:
            magnet.start()
            Drive.rightturnrobot()
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
            Drive.leftturnrobot() # now the robot is turned towards the line again
            #need to add some logic so it can ignore differences in the readings from the LDRs
    elif Drive.voltageL2 < 0.15:
        time.sleep(0.05) #small debounce
        elif Drive.voltageL2 < 0.15:
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
    Drive.runrobot()
    if Drive.voltageR2 < 0.15 and Drive.voltageL2 < 0.15:
        count +=1

"""
def straightline3():
    Drive.runrobot()
    if Drive.voltageR2 < 0.15:
        Drive.rightturnrobot()
        magnet.start()
        #needs the actuator to start here, so the nut can be picked up
        #needs the actuator to come back here after picking up the nut
        magnet.stop()
        Drive.leftturnrobot() # now the robot is turned towards the line again
        #need to add some logic so it can ignore differences in the readings from the LDRs
        Drive.runrobot() #this functions needs to make sure the robot keeps moving.
"""    

    


count = 1

while True:    #state 1
    if count == 1:
        straightline()
        

    #state 2
    if count == 2:
        straightline2()

    #state 3
    if count == 3:
        straightline()
"""
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
"""