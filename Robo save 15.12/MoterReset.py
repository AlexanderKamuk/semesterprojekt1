from StepperClass import StepperMotor

right=[0,1,2,3]
left=[4,5,6,7]
pins=left+right

stepping = StepperMotor(pins, "MICRO", 20, 20_000, 4)
stepping.stop()