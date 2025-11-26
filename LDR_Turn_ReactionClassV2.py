from StepperMotorDiff import StepperMotorDiff
from asyncDifferentialDrive import DifferentialDrive
import time
from machine import ADC, Pin, Timer
import time
import uasyncio as asyncio
class TrackDriving:
    def __init__(self,):
        self.adcM = ADC(Pin(26))
        self.adcL = ADC(Pin(27))
        #adc til nummer to er på pin 27
        self.left=[0,1,2,3]
        self.right=[4,5,6,7]

        self.stepmode="MICRO"
        self.microsteps_per_step=4
        self.pwm_pct=20
        self.turnmode="diff"
        self.frequency=40_000

        self.dist_turn=5
        self.dist_straight=1
        self.direction="forward"
        self.delay_us=0
        self.move_unit="dist"

        self.turncallR=DifferentialDrive(self.left, self.right, self.stepmode, self.microsteps_per_step, self.pwm_pct, "r", self.turnmode, self.frequency)
        self.turncallL=DifferentialDrive(self.left, self.right, self.stepmode, self.microsteps_per_step, self.pwm_pct,"l", self.turnmode, self.frequency)
        self.straightcall=DifferentialDrive(self.left, self.right, self.stepmode, self.microsteps_per_step, self.pwm_pct, "N/A", self.turnmode, self.frequency)

        #reading_timer = Timer()
        #reading_timer.init(period=250, mode=Timer.PERIODIC, callback=ReadVoltage)

        time.sleep(1)

    @micropython.native
    def ReadVoltage(self):
#        global voltageM
#        global voltageL
        raw_valueM = self.adcM.read_u16()
        raw_valueL = self.adcL.read_u16()
        self.voltageM = raw_valueM * 3.3/65535
        self.voltageL = raw_valueL * 3.3/65535
        print("L:",self.voltageL,"                     ","M:", self.voltageM)

    
    #global voltageM
    #global voltageL
    @micropython.native
    def chooseAction(self):
        if self.voltageM > 1.2 and self.voltageL > 0.7:
            return 1
        elif self.voltageM < 1.5 and self.voltageL < 0.7:
            return 2
        else:
            return 3
        
    def runrobot(self):   
        while True:
        # for i in range(100):
            self.ReadVoltage()
            start = time.ticks_ms()
            action = self.chooseAction()
            if action == 1:
                self.turncallR.move(self.dist_turn, self.direction, self.delay_us, self.move_unit)
            elif action == 2:
                self.turncallL.move(self.dist_turn, self.direction, self.delay_us, self.move_unit)
            elif action == 3:
                self.straightcall.move(self.dist_straight, "backward", self.delay_us, self.move_unit)
            end = time.ticks_ms()
            
        print("loop time", time.ticks_diff(end,start))


    #start = time.tick_ms()
    #reading_timer.deinit()
    #end = time.ticks_ms()
    #print(time.ticks_diff(end, start))

#start = TrackDriving()


