from DifferentialDrive import DifferentialDrive
from machine import ADC, Pin, Timer
import time
import micropython

class TrackDriving:
    def __init__(self):
        # LDR inputs
        self.adc = ADC(Pin(27))
        
        activationPins=reversed([22,18,14])
        self.signalPins=[Pin(pin,Pin.OUT) for pin in activationPins]
        
        self.sequence=[
            [0,1,0],
            [0,0,1],
            [0,0,0],
            [0,1,1],
            [1,0,0]
            ]

        # Motor pins
        self.left = [0, 1, 2, 3]

self.right = [4, 5, 6, 7]

        # General driving parameters
        self.stepmode = "MICRO"
        self.microsteps_per_step = 8
        self.pwm_pct = 25
        self.turnmode = "diff"
        self.frequency = 18_000

        # Movement specific parameters 
        self.dist_turn = 1
        
        # Thresholds
        self.thresholdL = 0.1
        self.thresholdM = 0.08
        self.thresholdR = 0.08
        
        self.dist_straight = 0.5
        self.direction = "forward"
        self.delay_us = 1200
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
        self.voltageL2 = 0.0
        self.voltageL1 = 0.0
        self.voltageR1 = 0.0
        self.voltageR2 = 0.0

    def set_pins(self, combination):
        for pin, value in zip(self.signalPins, combination):
            pin.value(value)


    def ReadVoltage(self):
        """
        Read raw values and convert them to voltages for middle (M) and left (L) LDR sensors.
        """
        self.set_pins(self.sequence[0])
        self.voltageL2 = self.adc.read_u16() * 3.3 / 65535

        self.set_pins(self.sequence[1])
        self.voltageL1 = self.adc.read_u16() * 3.3 / 65535

        self.set_pins(self.sequence[2])
        self.voltageM = self.adc.read_u16() * 3.3 / 65535

        self.set_pins(self.sequence[3])
        self.voltageR1 = self.adc.read_u16() * 3.3 / 65535

        self.set_pins(self.sequence[4])
        self.voltageR2 = self.adc.read_u16() * 3.3 / 65535
    
    def rightturnrobot(self): #90 degrees right turn
        self.turncallR.move(
            155, self.direction, self.delay_us, self.move_unit
        )
    def leftturnrobot(self): #90 degrees left turn
        self.turncallL.move(
            155, self.direction, self.delay_us, self.move_unit
            
        )
        
    def turn(self,angle, direction="right"):
        if direction=="left":
            self.turncallL.move(
                angle, self.direction, self.delay_us, self.move_unit
            )
        else:
            self.turncallR.move(
                angle, self.direction, self.delay_us, self.move_unit
            )
        
    def _200(self):
        self.turncallR.move(
            200, self.direction, self.delay_us, self.move_unit
        )
        
    def _70(self):
        self.turncallR.move(
            45, self.direction, self.delay_us, self.move_unit
        )
    
    def straight(self,length):
        self.straightcall.move(
                length, "backward", self.delay_us, self.move_unit
            )
        
    def straight5cm(self):
        self.straightcall.move(
                5, "backward", self.delay_us, self.move_unit
            )
    def straight10cm(self):
        self.straightcall.move(
                10, "backward", self.delay_us, self.move_unit
                )
        
    def reverse5cm(self):
        self.straightcall.move(
                5, "forward", self.delay_us, self.move_unit
            )
        
    def reverse(self,length):
        self.straightcall.move(
                length, "forward", self.delay_us, self.move_unit
            )
    
        
    def wiggle(self):
        self.turn(10)
        self.turn(20,"left")
        self.turn(10)
        
        self.reverse(2)
        
        self.turn(15)
        self.turn(30,"left")
        self.turn(15)
        
        self.straight(2)
         
        self.turn(20)
        self.turn(40,"left")
        self.turn(20)
        
        self.reverse(2)
        
        self.turn(45)
        self.turn(90,"left")
        self.turn(45)
        
        self.straight(2)
        
    


        
    
        
    @micropython.native
    def chooseAction(self):
        """
        Returns:
            1: Turn right
            2: Turn left
            3: Drive straight
        """
        
        """
        BOOLIAN LOGIC
        Determine general action
        """
        # Decide action (right, left, straight) based on LDR reading
        if  self.voltageL2 > self.thresholdL and self.voltageM < self.thresholdR: 
            return 1  # Turn right
        elif self.voltageL2 < self.thresholdL and self.voltageM > self.thresholdR:
            return 2  # Turn left
        else:
            return 3  # Drive straight

    def runrobot(self):
        """Main control loop: read sensors, decide action, move robot."""
        self.ReadVoltage()
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

#Drive = TrackDriving()

#while True:
#    Drive.runrobot()


