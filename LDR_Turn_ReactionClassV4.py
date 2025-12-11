from DifferentialDrive import DifferentialDrive
from machine import ADC, Pin
import micropython


class TrackDriving:
    def __init__(self, test: bool = False):
        # Define threshold LDR values depending on situation
        if test is True:  # For testing and debugging
            self.thresholdM = 0.9
            self.thresholdL = 1.0
            self.thresholdR = 0.9
        else:  # For use on track
            self.thresholdM = 0.4
            self.thresholdL = 0.8
            self.thresholdR = 0.3

        # LDR inputs
        self.adcM = ADC(Pin(26))
        self.adcL = ADC(Pin(27))
        self.adcR = ADC(Pin(28))
        # adc til nummer to er på pin 27 og 28

        # Motor pins
        self.left = [0, 1, 2, 3]
        self.right = [4, 5, 6, 7]

        # General driving parameters
        self.stepmode = "MICRO"
        self.microsteps_per_step = 4
        self.pwm_pct = 20
        self.turnmode = "diff"   # can be set to "curve" if you want forward+turn
        self.frequency = 40_000

        # Movement specific parameters
        self.dist_turn = 5
        self.dist_straight = 1
        self.direction = "forward"
        # Simple constant speed (delay between steps in microseconds)
        # smaller = faster, larger = slower
        self.delay_us = 1500
        self.move_unit = "dist"

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

    def ReadVoltage(self):
        """Read raw values and convert them to voltages for M, L and R LDR sensors."""
        raw_valueM = self.adcM.read_u16()
        raw_valueL = self.adcL.read_u16()
        raw_valueR = self.adcR.read_u16()
        self.voltageM = raw_valueM * 3.3 / 65535
        self.voltageL = raw_valueL * 3.3 / 65535
        self.voltageR = raw_valueR * 3.3 / 65535
        # print("L:", self.voltageL, " M:", self.voltageM, " R:", self.voltageR)

    @micropython.native
    def chooseAction(self):
        """Decide which action the robot should take.

        Returns:
            1: Turn right
            2: Turn left
            3: Drive straight
        """

        # Decide action (right, left, straight) based on LDR readings and thresholds
        if (
            self.voltageL > self.thresholdL
            and self.voltageM > self.thresholdM
            and self.voltageR < self.thresholdR
        ):
            return 1  # Turn right
        elif (
            self.voltageL < self.thresholdL
            and self.voltageM > self.thresholdM
            and self.voltageR > self.thresholdR
        ):
            return 2  # Turn left
        else:
            return 3  # Drive straight

    def runrobot(self):
        """Main control loop: read sensors, compute action, and move the robot."""
        while True:
            self.ReadVoltage()  # Read LDR sensors

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


# Create and run
Drive = TrackDriving()
Drive.runrobot()
