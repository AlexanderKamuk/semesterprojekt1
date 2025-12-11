# file name: differential_drive_pcb
from StepperClassNewTest import StepperMotor
import math


class DifferentialDrive:
    def __init__(self, left, right, step_mode="MICRO", micro_steps=1,
                 pwm_pct=20, turn="N/A", turn_mode="diff",
                 frequency=14_000, curve_intensity=1.0):
        """
        Initialize the navigation system with two stepper motors.

        :param left: List of GPIO pins for left motor driver.
        :param right: List of GPIO pins for right motor driver.
        :param step_mode: Step sequence to be used ("FULL", "HALF", "MICRO")
        :param micro_steps: Micro steps per full step
        :param pwm_pct: % of max pwm
        :param turn: "l", "r", or "N/A"
        :param turn_mode:
            "diff"   - differential turn (on the spot, one wheel fwd, other back)
            "single" - only one wheel turns (pivot)
            "curve"  - both wheels forward, inner wheel slower (forward + turn)
        :param frequency: PWM frequency in Hz
        :param curve_intensity: For turn_mode="curve":
            0.0 = no curve (straight), 1.0 = max curve
        """
        self.micro_steps = micro_steps
        self.turn = turn
        self.turn_mode = turn_mode
        self.curve_intensity = curve_intensity

        # Generate pin list
        if turn_mode == "single":
            # Original single-wheel behaviour
            if turn == "l":
                pins = [16, 17, 18, 19] + right  # LEDs + right wheel
            else:
                pins = left + [20, 21, 22, 26]

        elif turn_mode == "curve":
            # Forward + turn:
            # StepperMotor treats first 4 pins as "motor A" (fast/outer),
            # last 4 pins as "motor B" (slow/inner) when curve=True.

            if turn == "l":
                # Turning left -> right wheel should be outer/faster
                pins = right + left
            elif turn == "r":
                # Turning right -> left wheel should be outer/faster
                pins = left + right
            else:
                # No specific turn, behave like straight
                pins = left + right

        else:
            # Default "diff" behaviour (spin in place) 
            if turn == "l":
                pins = list(reversed(left)) + right
            elif turn == "r":
                pins = left + list(reversed(right))
            else:
                pins = left + right  # Straight

        # Enable StepperMotor curve mode ONLY when we are in curve turning
        curve_flag = (turn_mode == "curve" and turn in ("l", "r"))

        # Set up call in for from stepper motor class
        self.stepping = StepperMotor(
            pins,
            step_mode,
            pwm_pct=pwm_pct,
            frequency=frequency,
            micro_steps=micro_steps,
            curve=curve_flag,
            curve_intensity=self.curve_intensity,
        )

        # Ensure that all motors are turned off at start
        self.stop()

    # Define function Stop motor
    def stop(self):
        self.stepping.stop()
    
    # Define function for moving stepper motors
    def move(self, dist, direction="forward", delay_us=1000000, move_unit="steps"):
        """
        :param dist: Distance to travel.
        :param direction: Direction to move. "forward" or "backward".
        :param delay_us: Delay between steps in microseconds.
        :param move_unit: "steps" for raw steps, "dist" for cm or degrees.
        """

        # Diameter of wheel in cm (regulated after testing results)
        d = 8.5 * (1 + 0.0145) * (1 + 0.002)
        
        # Distance between wheels in cm (regulated after testing results)
        dw = 24.5

        # Calculate necessary steps in distance 
        if self.turn in ("l", "r") and self.turn_mode != "curve":
            # original/old turning math (for diff / single)
            if move_unit == "dist":
                distance_per_step = math.pi * d / (360 / (1.8 / self.micro_steps))
                turning_O = math.pi * dw * 2
                steps_full_turn = turning_O / distance_per_step
                steps = dist / 360 * steps_full_turn
                if self.turn_mode == "single":
                    steps = steps
                else:
                    steps = steps / 2
            else:
                # dist is already "turn steps"
                steps = dist
                if self.turn_mode != "single":
                    steps = steps / 2
        else:
            # Straight driving OR curve driving:
            # we use the same linear-distance formula,
            # curve pattern in the motor decides the actual trajectory.
            if move_unit == "dist":
                steps = dist / (d * math.pi / (200 * self.micro_steps))
            else:
                steps = dist

        # Prepare delay for move_stepper
        delay = delay_us
        
        # Call moving function from stepper motor class
        self.stepping.move_stepper(steps, direction, delay)
