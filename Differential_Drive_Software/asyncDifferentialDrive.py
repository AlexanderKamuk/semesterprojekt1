# file name: differential_drive_pcb
from StepperMotorDiff import StepperMotorDiff
import math
import uasyncio as asyncio


class DifferentialDrive:
    def __init__(
        self,
        left,
        right,
        step_mode="MICRO",
        micro_steps=1,
        pwm_pct=20,
        turn="N/A",
        turn_mode="diff",
        frequency=14_000,
    ):
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
        
        # Set up call for left and right motor from stepper motor class
        self.steppingL = StepperMotorDiff(left, step_mode, pwm_pct, frequency, micro_steps)
        self.steppingR = StepperMotorDiff(right, step_mode, pwm_pct, frequency, micro_steps)

        # Ensure that all motors are turned off at
        self.stop()

    # Define function Stop motor
    def stop(self):
        self.steppingL.stop()
        self.steppingR.stop()
    
    # Define function for moving stepper motors
    def move(self, dist, direction="forward", delay_us=1000000, move_unit="steps"):
        """
        Move the robot straight or perform a turn.

        Interpretation of arguments:
        - If turn == "N/A"  -> drive straight.
        - If turn == "l"/"r"-> perform a turn.

        :param dist:
            If move_unit == "steps":
                - Number of motor steps (raw step count).
            If move_unit == "dist":
                - When turning (self.turn == "l"/"r"): dist is an angle in degrees.
                - When driving straight (self.turn == "N/A"): dist is a distance in cm.
        :param direction: "forward" or "backward".
        :param delay_us: Delay between steps in microseconds.
        :param move_unit: "steps" or "dist".
        """

        # Diameter of wheel in cm (regulated after testing results)
        wheel_diameter = 8.5*(1+0.0145)*(1+0.002)
        
        # Diameter between wheels in cm (regulated after testing results)
        diameter_between_wheels = 24
        
        # Calculate necessary steps in distance
        if self.turn in ["r","l"]:
            if move_unit=="dist":
                # dist is interpreted as an angle in degrees (0–360), the robot has to turn
                distance_per_step = math.pi * wheel_diameter / (360 / (1.8 / self.micro_steps)) # Calculate distance per step
                turning_circumference = math.pi * diameter_between_wheels * 2 # Calculate turning circumference
                steps_full_turn = turning_circumference / distance_per_step # Calculate steps per full turn
                # Steps needed for the requested angle
                steps = dist / 360 * steps_full_turn # calculate steps required to move a given number of degrees
                if self.turn_mode=="single": # All steps on one wheel for single wheel drive
                    if self.turn=="l":
                        stepsR=steps
                        stepsL=0
                    else: # Right turn, single wheel
                        stepsL=steps
                        stepsR=0
                else: # Divide the steps equally and change direction of one wheel for differential drive
                    if self.turn=="l":
                        stepsR=steps/2
                        stepsL=-steps/2
                    else: # Right turn, differential drive
                        stepsL=steps/2
                        stepsR=-steps/2
            else: # Asumes move_unit to be steps
                # move_unit=="steps": dist is already a step count
                if self.turn_mode=="single": # All steps on one wheel for single wheel drive
                    if self.turn=="l":
                        stepsR=dist
                        stepsL=0
                    else: # Right turn, single wheel
                        stepsL=dist
                        stepsR=0
                else: # Divide the steps equally and change direction of one wheel for differential drive
                    if self.turn=="l":
                        stepsR=dist/2
                        stepsL=-dist/2
                    else: # Right turn, differential drive
                        stepsL=dist/2
                        stepsR=-dist/2
        # Drive straight (no turning)
        else: # Defaults to driving straight, if turn is neither "l" nor "r"
            if move_unit == "dist": # Calculate necessary steps to move a given distance
                # Convert linear distance (cm) to steps
                cm_per_step = wheel_diameter*math.pi/(200*self.micro_steps) # Calculate cm moved per microstep
                stepsL=dist / cm_per_step # Calculate necessary steps to move a given distance
                stepsR=stepsL
            else: # Assumes move_unit to be "steps"
                stepsL=dist
                stepsR=dist

        # Prepare delay for move_stepper function
        delay=delay_us
        
        # Define async task for each wheel by calling in an async function from the stepper class
        async def stepper_move_call():
            #Run both motors concurrently and return when both are finished.
            task_left = asyncio.create_task(
                self.steppingL.move_stepper(stepsL, direction, delay)
            )
            task_right = asyncio.create_task(
                self.steppingR.move_stepper(stepsR, direction, delay)
            )
            # Wait for both tasks to complete
            await task_left
            await task_right
        
        # Run the async tasks
        asyncio.run(stepper_move_call())