from machine import ADC, Pin
import time

adcL = ADC(Pin(26))
adcM = ADC(Pin(27))
adcR = ADC(Pin(28))

log_filename = "data_log3.csv"


def ReadVoltage():
    raw_valueL = adcL.read_u16()
    voltageL = raw_valueL * 3.3/65535
    raw_valueM = adcM.read_u16()
    voltageM = raw_valueM * 3.3/65535
    raw_valueR = adcR.read_u16()
    voltageR = raw_valueR * 3.3/65535
    print([voltageL,voltageM,voltageR])
    #print(voltageR)

"""with open(log_filename, 'a') as log_file:
    time0=time.time()
    log_file.write("time,voltage\n")
    while True:
        voltage = ReadVoltage()
        print("{},{}".format(time.time()-time0,voltage))
        log_file.write("{},{}\n".format(time.time()-time0,voltage))
        time.sleep(1)"""

while True:
    ReadVoltage()
    time.sleep(0.1)



