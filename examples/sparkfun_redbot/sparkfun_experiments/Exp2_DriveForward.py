#!/usr/bin/python
"""
  Exp2_DriveForward -- RedBot Experiment 2

  Drive forward and stop.

  Hardware setup:
  The Power switch must be on, the motors must be connected, and the board must be receiving power
  from the battery. The motor switch must also be switched to RUN.
"""

from pymata_aio.pymata3 import PyMata3
from examples.sparkfun_redbot.sparkfun_experiments.library.redbot import RedBotMotors
# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()

motors = RedBotMotors(board)
# Instantiate the motor control object. This only needs to be done once.


def setup():
    print("Left and right motors at full speed forward")
    motors.drive(255)   # Turn on Left and right motors at full speed forward.
    board.sleep(2.0)    # Waits for 2 seconds
    print("Stop both motors")
    motors.stop()       # Stops both motors


def loop():
    # Nothing here. We'll get to this in the next experiment.
    pass


if __name__ == "__main__":
    setup()
    while True:
        loop()
