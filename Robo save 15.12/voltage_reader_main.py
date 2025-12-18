from differential_drive_stepper import DifferentialDrive
import time
from machine import ADC, Pin, Timer

adc = ADC(Pin(26))

log_filename = "data_log3.csv"


def ReadVoltage(timer):
    raw_value = adc.read_u16()
    voltage = raw_value * 3.3/65535
    print("{},{}".format(time.time()-time0,voltage))
    log_file.write("{},{}\n".format(time.time()-time0,voltage))

left=[0,1,2,3]
right=[4,5,6,7]

with open(log_filename, 'w') as log_file:
    # Startup delay
    time.sleep(1)
    
    # Data list setup
    time0=time.time()
    log_file.write("time,voltage\n")
    
    # LDR reading as a timer
    reading_timer = Timer()
    reading_timer.init(period=250, mode=Timer.PERIODIC, callback=ReadVoltage)
    
    # turn 180
    turn="r"
    diff=DifferentialDrive(left, right, "MICRO", 10, 20, turn)
    diff.move(180, "forward", 1000, "dist")

    # wait
    time.sleep(2)

    # turn 180
    turn="l"
    diff=DifferentialDrive(left, right, "MICRO", 10, 20, turn)
    diff.move(180, "forward", 1000, "dist")
    
    # stop timer
    reading_timer.deinit()