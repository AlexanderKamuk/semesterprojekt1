from DifferentialDrive import DifferentialDrive
from machine import ADC, Pin
import time


class TrackDriving:
    def __init__(self, test=False):
        # Thresholds
        if test:
            self.thresholdM = 0.8
            self.thresholdL = 1.0
            self.thresholdR = 0.8
        else:
            self.thresholdM = 0.4
            self.thresholdL = 0.5
            self.thresholdR = 0.25

        # LDR ADCs
        self.adcL = ADC(Pin(26))
        self.adcM = ADC(Pin(27))
        self.adcR = ADC(Pin(28))

        # Motor pins
        self.left = [0, 1, 2, 3]
        self.right = [4, 5, 6, 7]

        # Drive settings (FASTER + HALF stepping + curve-only)
        self.stepmode = "HALF"          # HALF stepping
        self.microsteps_per_step = 1    # unused in HALF mode, kept for API
        self.pwm_pct = 40
        self.frequency = 20_000

        # distances in cm (tune these after testing(testing not completed))
        self.dist_turn = 1
        self.dist_straight = 2

        # speed (smaller delay_us = faster)
        self.delay_us = 800
        self.final_delay_us = 400
        self.ramp_steps = 20

        # curve intensity (0=almost straight, 1=strong turn)
        self.curve_intensity = 0.80

        # Curve-only drive objects
        self.turncallR = DifferentialDrive(
            self.left, self.right,
            step_mode=self.stepmode,
            micro_steps=self.microsteps_per_step,
            pwm_pct=self.pwm_pct,
            turn="r",
            frequency=self.frequency,
            curve_intensity=self.curve_intensity,
        )
        self.turncallL = DifferentialDrive(
            self.left, self.right,
            step_mode=self.stepmode,
            micro_steps=self.microsteps_per_step,
            pwm_pct=self.pwm_pct,
            turn="l",
            frequency=self.frequency,
            curve_intensity=self.curve_intensity,
        )
        self.straightcall = DifferentialDrive(
            self.left, self.right,
            step_mode=self.stepmode,
            micro_steps=self.microsteps_per_step,
            pwm_pct=self.pwm_pct,
            turn="N/A",
            frequency=self.frequency,
            curve_intensity=0.0,
        )

        self.voltageM = 0.0
        self.voltageL = 0.0
        self.voltageR = 0.0

        time.sleep(0.5)

    def ReadVoltage(self):
        raw_valueM = self.adcM.read_u16()
        raw_valueL = self.adcL.read_u16()
        raw_valueR = self.adcR.read_u16()

        self.voltageM = raw_valueM * 3.3 / 65535
        self.voltageL = raw_valueL * 3.3 / 65535
        self.voltageR = raw_valueR * 3.3 / 65535

    def chooseAction(self):
        # 1 = right, 2 = left, 3 = back, 4 = forward
        if self.voltageL > self.thresholdL and self.voltageM > self.thresholdM and self.voltageR < self.thresholdR:
            return 1
        elif self.voltageL < self.thresholdL and self.voltageM > self.thresholdM and self.voltageR > self.thresholdR:
            return 2
        elif self.voltageL > self.thresholdL and self.voltageM > self.thresholdM and self.voltageR > self.thresholdR:
            return 3
        else:
            return 4

    def runrobot(self):
        while True:
            self.ReadVoltage()
            action = self.chooseAction()

            if action == 1:  # right curve
                self.turncallR.move(
                    self.dist_turn, "forward",
                    delay_us=self.delay_us,
                    move_unit="dist",
                    ramp=True,
                    final_delay_us=self.final_delay_us,
                    ramp_steps=self.ramp_steps,
                )
            elif action == 2:  # left curve
                self.turncallL.move(
                    self.dist_turn, "forward",
                    delay_us=self.delay_us,
                    move_unit="dist",
                    ramp=True,
                    final_delay_us=self.final_delay_us,
                    ramp_steps=self.ramp_steps,
                )
            elif action == 3:  # back
                self.straightcall.move(
                    self.dist_straight, "backward",
                    delay_us=self.delay_us,
                    move_unit="dist",
                    ramp=True,
                    final_delay_us=self.final_delay_us,
                    ramp_steps=self.ramp_steps,
                )
            else:  # forward
                self.straightcall.move(
                    self.dist_straight, "forward",
                    delay_us=self.delay_us,
                    move_unit="dist",
                    ramp=True,
                    final_delay_us=self.final_delay_us,
                    ramp_steps=self.ramp_steps,
                )


if __name__ == "__main__":
    robot = TrackDriving(test=False)
    robot.runrobot()
