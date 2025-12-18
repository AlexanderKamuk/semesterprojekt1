from StepperClass import StepperMotor
import math


class DifferentialDrive:
    """Curve-only differential drive.

    ONLY supports:
      - straight
      - curve left
      - curve right
    """

    def __init__(
        self,
        left_pins,
        right_pins,
        step_mode="HALF",
        micro_steps=1,
        pwm_pct=30,
        turn="N/A",                 # 'l', 'r', or 'N/A'
        frequency=20_000,
        curve_intensity=1.0,
        wheel_diameter_cm=8.5 * (1 + 0.0145) * (1 + 0.002),
    ):
        self.left_pins = list(left_pins)
        self.right_pins = list(right_pins)

        self.step_mode = str(step_mode).upper()
        self.micro_steps = max(1, int(micro_steps))

        self.turn = turn
        self.curve_intensity = float(curve_intensity)
        self.wheel_diameter_cm = float(wheel_diameter_cm)

        # pins order matters for curve mode:
        # first 4 pins = outer/faster wheel, last 4 pins = inner/slower wheel
        if self.turn == "l":
            pins = self.left_pins + self.right_pins
            curve = True
        elif self.turn == "r":
            pins = self.right_pins + self.left_pins
            curve = True
        else:
            pins = self.left_pins + self.right_pins
            curve = False

        self.stepping = StepperMotor(
            pins,
            step_mode=self.step_mode,
            pwm_pct=pwm_pct,
            frequency=frequency,
            micro_steps=self.micro_steps,
            curve=curve,
            curve_intensity=self.curve_intensity,
        )

        self.stop()

    def stop(self):
        self.stepping.stop()

    def _steps_per_rev_total(self):
        # Base is 200 full steps per rev for 1.8° motors
        base = 200
        if self.step_mode == "FULL":
            factor = 1
        elif self.step_mode == "HALF":
            factor = 2
        else:  # MICRO
            factor = self.micro_steps
        return base * factor

    def _cm_to_steps(self, dist_cm):
        steps_per_rev = self._steps_per_rev_total()
        circumference = math.pi * self.wheel_diameter_cm
        cm_per_step = circumference / steps_per_rev
        return int(dist_cm / cm_per_step)

    def move(
        self,
        dist,
        direction="forward",
        delay_us=900,
        move_unit="dist",   # 'dist' (cm) or 'steps'
        ramp=True,
        final_delay_us=450,
        ramp_steps=30,
    ):
        if move_unit == "dist":
            steps = self._cm_to_steps(dist)
        else:
            steps = int(dist)

        steps = abs(int(steps))
        if steps <= 0:
            return

        if ramp:
            self.stepping.move_stepper_with_ramp(
                steps,
                direction,
                initial_delay_us=int(delay_us),
                final_delay_us=int(final_delay_us),
                ramp_steps=int(ramp_steps),
            )
        else:
            self.stepping.move_stepper(steps, direction, int(delay_us))
