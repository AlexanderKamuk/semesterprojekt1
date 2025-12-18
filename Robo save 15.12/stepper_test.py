# Always include:
from stepper import StepperMotor
from differential_drive_stepper import DifferentialDrive
import time

time.sleep(3)
"""left=[16,17,18,19]
right=[20,21,22,26]"""
left=[0,1,2,3]
right=[4,5,6,7]

"""turn="N/A"
diff=DifferentialDrive(left, right, "MICRO", 3, 20, turn)
diff.move(100, "forward", 1000, "dist")"""

turn="r"
diff=DifferentialDrive(left, right, "MICRO", 6, 20, turn)
diff.move(180, "forward", 1000, "dist")

time.sleep(2)

turn="l"
diff=DifferentialDrive(left, right, "MICRO", 6, 20, turn)
diff.move(180, "forward", 1000, "dist")

"""for i in range(4):
    turn="N/A"
    diff=DifferentialDrive(left, right, "MICRO", 3, 20, turn)
    diff.move(100, "forward", 1000, "dist")
    time.sleep(0)
    turn="r"
    diff=DifferentialDrive(left, right, "MICRO", 3, 20, turn)
    diff.move(90, "forward", 1000, "steps")"""

print("process ended")