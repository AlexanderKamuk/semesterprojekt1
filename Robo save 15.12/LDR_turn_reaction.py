from StepperMotorDiff import StepperMotorDiff
from asyncDifferentialDrive import DifferentialDrive
import time
from machine import ADC, Pin, Timer
import time
import uasyncio as asyncio

adcM = ADC(Pin(26))
adcL = ADC(Pin(27))
#adc til nummer to er på pin 27
#@micropython.native
def ReadVoltage(timer):
    global voltageM
    global voltageL
    raw_valueM = adcM.read_u16()
    raw_valueL = adcL.read_u16()
    voltageM = raw_valueM * 3.3/65535
    voltageL = raw_valueL * 3.3/65535
    print(voltageM)

left=[0,1,2,3]
right=[4,5,6,7]

turn="r"
stepmode="MICRO"
microsteps_per_step=10
pwm_pct=20
turnmode="diff"
frequency=20_000

dist_turn=5
dist_straight=1
direction="forward"
delay_us=0
move_unit="dist"

turncallR=DifferentialDrive(left, right, stepmode, microsteps_per_step, pwm_pct, turn, turnmode, frequency)
turncallL=DifferentialDrive(left, right, stepmode, microsteps_per_step, pwm_pct,"l", turnmode, frequency)
straightcall=DifferentialDrive(left, right, stepmode, microsteps_per_step, pwm_pct, "N/A", turnmode, frequency)

reading_timer = Timer()
reading_timer.init(period=250, mode=Timer.PERIODIC, callback=ReadVoltage)

time.sleep(1)

global voltageM
global voltageL
#@micropython.viper
while True:
    if voltageM > 1.2 and voltageL > 0.7:
        turncallR.move(dist_turn, direction, delay_us, move_unit)
    elif voltageM < 1.5 and voltageL < 0.7:
        turncallL.move(dist_turn, direction, delay_us, move_unit)
    else:
        straightcall.move(dist_straight, "backward", delay_us, move_unit)
start = time.tick_ms()
reading_timer.deinit()
end = time.tick_ms()
print(time.ticks_diff(end, start))