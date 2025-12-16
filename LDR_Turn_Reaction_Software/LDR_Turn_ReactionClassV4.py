from StepperMotorDiff import StepperMotorDiff
from DifferentialDrive import DifferentialDrive
from machine import ADC, Pin, Timer
import time
import uasyncio as asyncio
import micropython   
# has new speed  things in it (The robot now automatically changes its
# movement speed depending on how “wrong” the LDR readings are, instead of using a fixed speed.)
#can use curve

class TrackDriving:
    def __init__(self, test=False):
        # Define threshold LDR values depending on situation
        if test == True: # For testing and debugging
            self.thresholdM = 0.8
            self.thresholdL = 1
            self.thresholdR = 0.8
        else: # For use on track
            self.thresholdM = 0.4
            self.thresholdL = 0.8
            self.thresholdR = 0.3
        
        # LDR inputs
        self.adcM = ADC(Pin(26))
        self.adcL = ADC(Pin(27))
        self.adcR = ADC(Pin(28))
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
        self.delay_us = 1500          # Delay will be regulated through fuzzy logic
        self.move_unit = "dist"

        # fuzzy / speed control settings 
        # Max absolute voltage difference between M and L that we care about
        # (used for normalizing into a 0–1 "error" value)
        self.fuzzy_diff_max = 1.5

        # Delay range in microseconds.
        # Small error -> should be fast (delay near min_delay_us)
        # Big error   -> should be slower (delay near max_delay_us)
        self.min_delay_us = 1500       # fastest
        self.max_delay_us = 2250    # slowest

        # Toggle for fuzzy logic (True = use fuzzy, False = constant speed)
        self.use_fuzzy_speed = True
        self.constant_delay_us = 500    # used when fuzzy is disabled

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
        self.voltageR = 0.0

    def enable_fuzzy_speed(self):
        """Use fuzzy logic speed control."""
        self.use_fuzzy_speed = True

    def disable_fuzzy_speed(self, constant_delay_us=None):
        """
        Turn off fuzzy logic and use a constant delay_us instead.
        If constant_delay_us is given, update the stored constant speed.
        """
        self.use_fuzzy_speed = False
        if constant_delay_us is not None:
            self.constant_delay_us = constant_delay_us

    def ReadVoltage(self):
        """
        Read raw values and convert them to voltages for middle (M) and left (L) LDR sensors.
        """
        raw_valueM = self.adcM.read_u16()
        raw_valueL = self.adcL.read_u16()
        raw_valueR = self.adcR.read_u16()
        self.voltageM = raw_valueM * 3.3 / 65535
        self.voltageL = raw_valueL * 3.3 / 65535
        self.voltageR = raw_valueR * 3.3 / 65535
        # print("L:", self.voltageL, "                     ", "M:", self.voltageM)

    #@micropython.native
    def chooseAction(self):
        """
        Decide which action the robot should take AND update delay_us using a simple rule.

        Returns:
            1: Turn right
            2: Turn left
            3: Drive straight 
        """

        # 1) SPEED PART
        if self.use_fuzzy_speed:
            # Use the difference between the two LDRs as an "error":
            # If the sensors see very different brightness -> big error -> move slower
            # If they are almost equal -> small error -> move faster
            abs_diff = abs(self.voltageR - self.voltageL)

            # Limit and normalize to [0, 1]
            max_d = self.fuzzy_diff_max
            if abs_diff >= max_d:
                norm_err = 1.0
            else:
                norm_err = abs_diff / max_d

            # Small error (norm_err ~ 0) -> delay close to min_delay_us (fast)
            # Big   error (norm_err ~ 1) -> delay close to max_delay_us (slow)
            span = self.max_delay_us - self.min_delay_us
            self.delay_us = int(self.min_delay_us + norm_err * span)
        else:
            # Fuzzy disabled: use constant speed
            self.delay_us = self.constant_delay_us

        # Safety: in case someone configured max < min by mistake
        if self.delay_us < self.min_delay_us:
            self.delay_us = self.min_delay_us
        elif self.delay_us > self.max_delay_us:
            self.delay_us = self.max_delay_us

        # 2) BOOLEAN LOGIC – determine general action
        # Decide action (right, left, straight) based on LDR reading
        if self.voltageL > self.thresholdL and self.voltageM > self.thresholdM and self.voltageR < self.thresholdR:
            return 1  # Turn right
        elif self.voltageL < self.thresholdL and self.voltageM > self.thresholdM and self.voltageR > self.thresholdR:
            return 2  # Turn left
        else:
            return 3  # Drive straight

    def runrobot(self):
        """
        Main control loop: read sensors, compute speed + action, and move the robot.
        """
        while True:
            self.ReadVoltage()  # Read LDR sensors

            # chooseAction():
            # - updates self.delay_us (speed)
            # - returns which manoeuvre to perform (1/2/3)
            action = self.chooseAction()

            # Act out the earlier determined action
            if action == 1:  # Turn right
                self.turncallR.move(
                    self.dist_turn, self.direction, self.delay_us, self.move_unit
                )
            elif action == 2:  # Turn left
                self.turncallL.move(
                    self.dist_turn, self.direction, self.delay_us, self.move_unit
                )
            elif action == 3:  # Go straight (backwards)
                self.straightcall.move(
                    self.dist_straight, "backward", self.delay_us, self.move_unit
                )
test=True # Input this variable in TrackDriving() to enable debugging LDR-values
# Create and run
Drive = TrackDriving()
Drive.runrobot()
