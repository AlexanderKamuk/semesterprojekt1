# file name: differential_drive_pcb
from StepperClass import StepperMotor
import math


class DifferentialDrive:
    def __init__(self, left, right, step_mode="MICRO", micro_steps=1, pwm_pct=20, turn="N/A", turn_mode="diff", frequency=14_000):
        """
        Initialize the navigation system with two stepper motors.

        :param left: Instance of StepperMotor class for the left motor.
        :param right: Instance of StepperMotor class for the right motor.
        :param step_mode: Step sequence to be used
        :param micro_steps: Micro steps per full step
        :param pwm_pct: % of max pwm
        :param turn: Whether to turn left ("l"), turn right ("r"), or drive straight ("N/A")
        :param turn_mode: Whether to turn using both ("diff") or one ("single") wheel
        :param frequency: Frequency for PWM signal in Hz
        """
        
        self.micro_steps=micro_steps
        self.turn=turn
        self.turn_mode=turn_mode
        
        # Generate pin list
        if turn_mode=="single":
            if turn=="l":
                pins=[16,17,18,19]+right    # Uses LEDs instead of motor pins in single wheel turn
            else:
                pins=left+[20,21,22,26]
        else:
            if turn=="l":
                pins=list(reversed(left))+right # Reverses order of pins for one motor driver
            elif turn=="r":
                pins=left+list(reversed(right))
            else:
                pins=left+right # Defaults to driving straight

        # Set up call in for from stepper motor class
        self.stepping = StepperMotor(pins, step_mode, pwm_pct=pwm_pct, frequency=frequency, micro_steps=micro_steps)

        # Ensure that all motors are turned off at
        self.stop()

    # Define function Stop motor
    def stop(self):
        self.stepping.stop()
    
    # Define function for moving stepper motors
    def move(self, dist, direction="forward", delay_us=1000000, move_unit="steps"):
        """
        :param dist: Distance to travel.
        :param direction: Direction to move. "forward" for forward, "backward" for backward.
        :param delay_us: Delay between steps in microseconds.
        :param move_unit: Units to move. "steps" for steps, "dist" for distance in cm or degrees
        """

        # Diameter of wheel in cm (regulated after testing results)
        d = 8.5*(1+0.0145)*(1+0.002)
        
        # Diameter between wheels in cm (regulated after testing results)
        dw = 24.5
        
        # Calculate necessary steps in distance
        if self.turn=="l" or self.turn=="r":
            if move_unit=="dist":
                distance_per_step=math.pi*d/(360/(1.8/self.micro_steps))
                turning_O=math.pi*dw*2
                steps_full_turn=turning_O/distance_per_step
                steps=dist/360*steps_full_turn
                if self.turn_mode=="single":
                    steps=steps
                else:
                    steps=steps/2
            else:
                if self.turn_mode=="single":
                    steps=steps
                else:
                    steps=steps/2
        else:
            if move_unit == "dist":
                steps=dist/(d*math.pi/(200*self.micro_steps))
            else:
                steps=dist

        # Prepare delay move_stepper function
        delay=delay_us
        
        # Call in moving function from stepper motor class
        self.stepping.move_stepper(steps, direction, delay)