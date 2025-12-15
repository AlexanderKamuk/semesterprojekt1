from machine import Pin, PWM
import time
step=0
class StepperMotor:
    def __init__(self, pins, step_mode="MICRO", pwm_pct=15, frequency=18_000, micro_steps=1, steps_per_rev=200,curve=False):
        """
        Initialize the stepper motor with given pins, PWM frequency, step mode, and steps per revolution.
        
        :param pins: List of GPIO pin numbers connected to the motor driver.
        :param step_mode: The stepping mode for the motor ("FULL", "HALF", or "MICRO").
        :param pwm_pct: PWM percentage for each motor coil (0 to 100).
        :param frequency: Frequency for the PWM signals in Hz.
        :param micro_steps: Number of micro-steps per full step (used in micro-stepping mode).
        :param [TODO: Implement RPM] steps_per_rev: Number of steps required for one full revolution (default is 200).
        """

        # Initialize PWM for each pin
        self.pins = [PWM(Pin(pin)) for pin in pins]
        
        # Curve parameter
        self.curve=curve

        # Set the PWM frequency for all pins
        self.set_frequency(frequency)
 
        # Calculate the PWM value from percentage (65535 is max for 16-bit)
        self.pwm_max = 65535
        self.pwm_val = int(self.pwm_max * pwm_pct / 100)
        self.micro_steps = micro_steps
        self.step_mode = step_mode.upper() # Ensure that is it uppercase letters
        
        # Initialize step counter to track the total number of step sequences
        self.step_counter = 0

        # Choose the step sequence based on the mode (FULL, HALF, or MICRO)
        if self.step_mode == "FULL":
            # Full-step sequence
            self.step_sequence = [
                [self.pwm_val, self.pwm_val, 0, 0],
                [0, self.pwm_val, self.pwm_val, 0],
                [0, 0, self.pwm_val, self.pwm_val],
                [self.pwm_val, 0, 0, self.pwm_val]
            ]
        elif self.step_mode == "HALF":
            # Half-step sequence
            self.step_sequence = [
                [self.pwm_val, 0, 0, 0],
                [self.pwm_val, self.pwm_val, 0, 0],
                [0, self.pwm_val, 0, 0],
                [0, self.pwm_val, self.pwm_val, 0],
                [0, 0, self.pwm_val, 0],
                [0, 0, self.pwm_val, self.pwm_val],
                [0, 0, 0, self.pwm_val],
                [self.pwm_val, 0, 0, self.pwm_val]
            ]
        elif self.step_mode == "MICRO":
            # Generate micro-stepping sequence
            self.step_sequence = self.generate_micro_step_sequence(self.pwm_val, self.micro_steps)
        else:
            # Invalid step mode handling
            self.stop_sequence = [0, 0, 0, 0, 0, 0, 0, 0]
            raise ValueError("Invalid step mode! Use 'FULL', 'HALF', or 'MICRO'.")
                
        # Sequence to stop the motor (no current in coils)
        self.stop_sequence = [0, 0, 0, 0, 0, 0, 0, 0]
        self._running = False

    def generate_micro_step_sequence(self, pwm_val, micro_steps):
        """
        Generates a step sequence for micro-stepping where PWM values increase and decrease alternately.
        
        :param pwm_val: Maximum PWM value for 16-bit resolution (65535).
        :param micro_steps: Number of micro-steps per full step.
        
        :return: A list of lists representing the step sequence for micro-stepping.
        """
        micro_step_size = pwm_val // micro_steps  # Define the micro step size
        step_sequence = []

        # Generate the step sequence for each phase
        # Phase 1: PWM on first pin, decreasing; PWM on second pin, increasing
        if self.curve==True: # skip a few steps on one wheel
            for i in range(micro_steps//2):
                pwm_1 = pwm_val - i * micro_step_size
                pwm_2 = i * micro_step_size
                pwm_12 = pwm_val - (i+1) * micro_step_size
                pwm_22 = (i+1) * micro_step_size
                step_sequence.append([pwm_1, pwm_2, 0, 0, 0, 0, 0, 0])
                step_sequence.append([pwm_12, pwm_22, 0, 0, pwm_1, pwm_2, 0, 0])
            
            # Phase 2: PWM on second pin, decreasing; PWM on third pin, increasing
            for i in range(micro_steps//2):
                pwm_2 = pwm_val - i * micro_step_size
                pwm_3 = i * micro_step_size
                pwm_22 = pwm_val - (i+1) * micro_step_size
                pwm_32 = (i+1) * micro_step_size
                step_sequence.append([0, pwm_2, pwm_3, 0, 0, 0, 0, 0])
                step_sequence.append([0, pwm_22, pwm_32, 0, 0, pwm_2, pwm_3, 0])

            # Phase 3: PWM on third pin, decreasing; PWM on fourth pin, increasing
            for i in range(micro_steps//2):
                pwm_3 = pwm_val - i * micro_step_size
                pwm_4 = i * micro_step_size
                pwm_32 = pwm_val - (i+1) * micro_step_size
                pwm_42 = (i+1) * micro_step_size
                step_sequence.append([0, 0, pwm_3, pwm_4, 0, 0, 0, 0])
                step_sequence.append([0, 0, pwm_32, pwm_42, 0, 0, pwm_3, pwm_4])

            # Phase 4: PWM on fourth pin, decreasing; PWM on first pin, increasing
            for i in range(micro_steps//2):
                pwm_4 = pwm_val - i * micro_step_size
                pwm_1 = i * micro_step_size
                pwm_42 = pwm_val - (i+1) * micro_step_size
                pwm_12 = (i+1) * micro_step_size
                step_sequence.append([pwm_1, 0, 0, pwm_4, 0, 0, 0, 0])
                step_sequence.append([pwm_12, 0, 0, pwm_42, pwm_1, 0, 0, pwm_4])
        
        else: #Defaults to non-curve driving
            for i in range(micro_steps):
                pwm_1 = pwm_val - i * micro_step_size
                pwm_2 = i * micro_step_size
                step_sequence.append([pwm_1, pwm_2, 0, 0, pwm_1, pwm_2, 0, 0])

            # Phase 2: PWM on second pin, decreasing; PWM on third pin, increasing
            for i in range(micro_steps):
                pwm_2 = pwm_val - i * micro_step_size
                pwm_3 = i * micro_step_size
                step_sequence.append([0, pwm_2, pwm_3, 0, 0, pwm_2, pwm_3, 0])

            # Phase 3: PWM on third pin, decreasing; PWM on fourth pin, increasing
            for i in range(micro_steps):
                pwm_3 = pwm_val - i * micro_step_size
                pwm_4 = i * micro_step_size
                step_sequence.append([0, 0, pwm_3, pwm_4, 0, 0, pwm_3, pwm_4])

            # Phase 4: PWM on fourth pin, decreasing; PWM on first pin, increasing
            for i in range(micro_steps):
                pwm_4 = pwm_val - i * micro_step_size
                pwm_1 = i * micro_step_size
                step_sequence.append([pwm_1, 0, 0, pwm_4, pwm_1, 0, 0, pwm_4])

        return step_sequence

    def set_frequency(self, frequency):
        """
        Set the frequency for the PWM signals.

        :param frequency: The frequency of the PWM signal in Hz.
        """
        # Apply the given frequency to all pins
        for pin in self.pins:
            pin.freq(frequency)
    
    def move_stepper(self, steps, direction, delay_us=1000):
        """
        Move the stepper motor a specified number of steps.
 
        :param steps: Number of steps to move.
        :param direction: Direction to move. "forward" for forward, "backward" for backward.
        :param delay_us: Delay between steps in microseconds.
        """
        # Determine direction of movement
        if direction == "forward":
            direction_step = 1
        elif direction == "backward":
            direction_step = -1
        else:
            raise ValueError("Direction must be 'forward' or 'backward'")
    
        # Move the motor step by step
        steps = abs(steps)
        
        for _ in range(steps):
            global step
            step = step % len(self.step_sequence)
            self.set_step(self.step_sequence[step])
            time.sleep_us(delay_us)  # Use microsecond delay
            """for step in range(len(self.step_sequence))[::direction_step]:
                self.set_step(self.step_sequence[step])
                time.sleep_us(delay_us)  # Use microsecond delay"""
            step = step + direction_step
            
            self.step_counter += direction_step
        
        self.stop()  # Stop the motor after completing the steps

    def stop(self):
        """
        Set all PWM outputs to 0 to stop the motor.
        """
        self.set_step(self.stop_sequence)  # Apply stop sequence

    def set_step(self, step):
        """
        Set the stepper motor to a specific step.
 
        :param step: A list representing the step sequence.
        """
        # Apply the PWM values to each pin for the current step
        for pin in range(len(self.pins)):
            self.pins[pin].duty_u16(step[pin])