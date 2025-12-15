#5LDR's start code
from machine import ADC, Pin
import time

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
    set_pins(sequence[0])
    raw_valueL2 = adc.read_u16()
    voltageL2 = raw_valueL2 * 3.3/65535
    
    set_pins(sequence[1])
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
    print(voltageL2, voltageL1,"         ",voltageR1, voltageR2)
    #print([voltageL2,voltageL1,voltageM,voltageR1,voltageR2])

while True:
    ReadVoltage()
    time.sleep(0.1)
