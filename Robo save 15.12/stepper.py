class StepperMotor:
    def __init__(self, pins, pwm_pct = 0.15, frequency=18_000):
        """
        Initialize a StepperMotor object.

        :param pins: List of GPIO pin numbers connected to the motor driver.
        :param pwm_pct: Percentage of the maximum PWM duty cycle.
        :param frequency: Frequency for the PWM signals.
        """

        
        self.pwm_pct = pwm_pct
        self.frequency = frequency
#taken from earlier code, this inializes the pins
        def initialize_pins(pins):
            return [PWM(Pin(pin)) for pin in pins]
        self.pins = initialize_pins(pins)
    
    # this defines any frequency for each pin
        def set_frequency(pins, frequency):
            for pin in pins:
                pin.freq(frequency)

        set_frequency(self.pins, frequency)

    
    def set_step(pins, step):
        for pin in range(len(pins)):
            pins[pin].duty_u16(step[pin])
    

        
    def stop(pins):
        stop_sequence = [0, 0, 0, 0]
        print("Stop --> {}".format(stop_sequence))
        StepperMotor.set_step(pins, stop_sequence)

    
    
            
    # defines how to move the stepper motor with any given number of steps
    def move_stepper(self,steps, direction, delay=0.001, which=1):

    
        pwm_max = 65535
        pct=self.pwm_pct
        pwm_val = int(pwm_max * pct)
        
        step_sequence = None
        

        self.which=which
        if which == 1:
                      #full step
            step_sequence = [
                [pwm_val, pwm_val, 0, 0],
                [0, pwm_val, pwm_val, 0],
                [0, 0, pwm_val, pwm_val],
                [pwm_val, 0, 0, pwm_val],
                ]
        
        elif which==2:           
        # How many steps for each sequence? half step
            step_sequence = [
                    [pwm_val, pwm_val, 0, 0],
                    [0, pwm_val, 0, 0],
                    [0, pwm_val, pwm_val, 0],
                    [0, 0, pwm_val, 0],
                    [0, 0, pwm_val, pwm_val],
                    [0, 0, 0, pwm_val],
                    [pwm_val, 0, 0, pwm_val],
                    [pwm_val, 0, 0, 0]
            
                    ]
        elif which==3:            
            #micro step	
            step_sequence = [
                [pwm_val, 0, 0, 0],    
                [pwm_val, pwm_val//2, 0, 0], 
                [pwm_val, pwm_val, 0, 0],  
                [pwm_val//2,pwm_val,0,0],
                [0, pwm_val, 0, 0],
                [0, pwm_val, pwm_val//2, 0],
                [0, pwm_val, pwm_val, 0],
                [0, pwm_val//2, pwm_val, 0],
                [0 ,0 , pwm_val, 0],
                [0, 0, pwm_val, pwm_val//2],
                [0, 0, pwm_val, pwm_val],
                [0, 0, pwm_val//2, pwm_val],
                [0, 0, 0, pwm_val],
                [pwm_val//2, 0, 0, pwm_val],
                [pwm_val, 0, 0, pwm_val],
                [pwm_val, 0, 0, pwm_val//2],         # Microstep 8
        ]
            
    
        elif step_sequence == None:
            print("step sequence can only be 1, 2 or 3")
    
    
    
    
        if delay < 0.0001:
            delay = 0.0001
            print("! Delay limit !")
            
        steps = abs(steps)
        
        if direction == 1:
        
            for cnt in range(steps):
                print(cnt)
                for step in range(len(step_sequence)):
                    StepperMotor.set_step(self.pins, step_sequence[step])
                    print("{} --> {}".format(step,step_sequence[step]))
                    time.sleep(delay)
                    
        elif direction == -1:
            
            for cnt in range(steps):
                    print(steps-cnt)
                    for step in range(len(step_sequence)-1, -1, -1):
                        StepperMotor.set_step(self.pins, step_sequence[step])
                        print("{} --> {}".format(step,step_sequence[step]))
                        time.sleep(delay)
            
        # IMPORTANT #
        StepperMotor.stop(self.pins)
        
    def keep_rotating(self, direction, delay):
       if steps == 1:
        while True:
           self.move_stepper(steps, direction, delay)