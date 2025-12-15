from StepperMotorDiff import StepperMotorDiff
from DifferentialDrive import DifferentialDrive
from machine import ADC, Pin, Timer
import time
import uasyncio as asyncio
import micropython   # was commented out before?
#has new fuzzylogicdriver like things in it (The robot now automatically changes its movement speed depending on how “wrong” the LDR readings are, instead of using a fixed speed.)

class TrackDriving:
    def __init__(self):
        # LDR inputs
        self.adcM = ADC(Pin(26))
        self.adcL = ADC(Pin(27))
        # adc til nummer to er på pin 27

        # Motor pins
        self.left = [0, 1, 2, 3]
        self.right = [4, 5, 6, 7]

        # General driving parameters
        self.stepmode = "MICRO"
        self.microsteps_per_step = 4
        self.pwm_pct = 20
        self.turnmode = "diff"
        self.frequency = 40_000

        # Movement specific parameters 
        self.dist_turn = 5
        self.dist_straight = 1
        self.direction = "forward"
        self.delay_us = 0          # Delay will be regulated through fuzzy logic
        self.move_unit = "dist"


        # Max absolute voltage difference between M and L that we care about
        # (used for normalizing into a 0–1 "error" value)
        self.fuzzy_diff_max = 1.5

        # Delay range in microseconds. Big error => small delay (fast),
        # small error => larger delay (slower / more precise)
        self.min_delay_us = 0       # faster
        self.max_delay_us = 1000    # slower

        # Setup of call from DifferentialDrive class
        # Right turn
        self.turncallR = DifferentialDrive(
            self.left,
            self.right,
            self.stepmode,
            self.microsteps_per_step,
            self.pwm_pct,
            "r",
            self.turnmode,
            self.frequency,
        )
        # Left turn
        self.turncallL = DifferentialDrive(
            self.left,
            self.right,
            self.stepmode,
            self.microsteps_per_step,
            self.pwm_pct,
            "l",
            self.turnmode,
            self.frequency,
        )
        # Drive straight
        self.straightcall = DifferentialDrive(
            self.left,
            self.right,
            self.stepmode,
            self.microsteps_per_step,
            self.pwm_pct,
            "N/A",
            self.turnmode,
            self.frequency,
        )

        # Sensor voltage storage
        self.voltageM = 0.0
        self.voltageL = 0.0


    def ReadVoltage(self):
        """
        Read raw values and convert them to voltages for middle (M) and left (L) LDR sensors.
        """
        raw_valueM = self.adcM.read_u16()
        raw_valueL = self.adcL.read_u16()
        self.voltageM = raw_valueM * 3.3 / 65535
        self.voltageL = raw_valueL * 3.3 / 65535
        #print("L:", self.voltageL, "                     ", "M:", self.voltageM) # print used during debugging
    
    def rightturnrobot(self): #90 degrees right turn
        self.turncallR.move(
            90, self.direction, self.delay_us, self.move_unit
        )
    def leftturnrobot(self): #90 degrees left turn
        self.turncallL.move(
            90, self.direction, self.delay_us, self.move_unit
        )
    def straightrobot(self): #move straight
        self.straightcall.move(
            self.dist_straight, "backward", self.delay_us, self.move_unit
        )
    
    @micropython.native
    def chooseAction(self):
        """
        Decide which action the robot should take AND update delay_us using a simple rule.

        Returns:
            1: Turn right
            2: Turn left
            3: Drive straight 
        """

         
        """
        1) SPEED PART
        Use the difference between the two LDRs as an "error":
        If the sensors see very different brightness -> big error -> want to react fast
        If they are almost equal -> small error -> can move slower
        """
        abs_diff = abs(self.voltageM - self.voltageL)  # sign is not important for speed, only magnitude


        # Limit and normalize to [0, 1]
        max_d = self.fuzzy_diff_max
        if abs_diff >= max_d:
            norm_err = 1.0
        else:
            norm_err = abs_diff / max_d

        """
        Map normalized error to a delay between min_delay_us and max_delay_us.
        Big error-> norm_err ~ 1 -> delay close to min_delay_us  (fast)
        Small error-> norm_err ~ 0 -> delay close to max_delay_us  (slow)
        """
        span = self.max_delay_us - self.min_delay_us
        self.delay_us = int(self.max_delay_us - norm_err * span)

        # Safety: in case someone configured max < min by mistake
        if self.delay_us < self.min_delay_us:
            self.delay_us = self.min_delay_us
        elif self.delay_us > self.max_delay_us:
            self.delay_us = self.max_delay_us
    

         
        """
        2) BOOLIAN LOGIC
        Determine general action
        """
        # Decide action (right, left, straight) based on LDR reading
        if self.voltageM > 1.2 and self.voltageL > 0.7:
            return 1  # Turn right
        elif self.voltageM < 1.5 and self.voltageL < 0.7:
            return 2  # Turn left
        else:
            return 3  # Drive straight

    def runrobot(self):
        """
        Main control loop: read sensors, compute fuzzy speed + action, and move the robot.
        """
        while True:
            self.ReadVoltage() # Read LDR sensors
            #start = time.ticks_ms() # Timer used for debugging and comparison

            # chooseAction() now:
            # - updates self.delay_us ( speed)
            # - returns which manoeuvre to perform (1/2/3)
            action = self.chooseAction()

            # Act out the earlier determined action
            if action == 1: # Turn right
                self.turncallR.move(
                    self.dist_turn, self.direction, self.delay_us, self.move_unit
                )
            elif action == 2: # Turn left
                self.turncallL.move(
                    self.dist_turn, self.direction, self.delay_us, self.move_unit
                )
            elif action == 3: # Go straight (backwards)
                self.straightcall.move(
                    self.dist_straight, "backward", self.delay_us, self.move_unit
                )
            # End of timer and print used for debugging
            #end = time.ticks_ms()
            #print("loop time", time.ticks_diff(end, start))


Drive = TrackDriving()
Drive.runrobot()
