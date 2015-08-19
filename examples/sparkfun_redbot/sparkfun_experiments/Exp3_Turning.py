#!/usr/bin/python3.4
"""***********************************************************************
 * Exp3_Turning -- RedBot Experiment 3
 *
 * Explore turning with the RedBot by controlling the Right and Left motors
 * separately.
 *
 * Hardware setup:
 * This code requires only the most basic setup: the motors must be
 * connected, and the board must be receiving power from the battery pack.
 *
 * 23 Sept 2013 N. Seidle/M. Hord
 * 04 Oct 2014 B. Huang
 ***********************************************************************"""

from pymata_aio.pymata3 import PyMata3
from RedBot import RedBotMotors
# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()

motors = RedBotMotors(board)


# Instantiate the motor control object. This only needs to be done once.


def setup():
    print("Driving Straight")

    motors.drive(255)  # Turn on Left and right motors at full speed forward.
    board.sleep(2.0)  # Waits for 2 seconds
    motors.pivot(255)
    print("Pivot-- turn to right")
    board.sleep(2.0)
    print("Driving Straight to Finish")
    motors.drive(255)
    board.sleep(2.0)
    motors.stop()  # Stops both motors


def loop():
    # Figure 8 pattern -- Turn Right, Turn Left, Repeat
    print("Veering Right")
    motors.leftFwd(200),
    motors.rightFwd(80)
    board.sleep(2.0)
    print("Veering Left")
    motors.leftFwd(80)
    motors.rightFwd(200)
    board.sleep(2.0)
    pass


if __name__ == "__main__":
    setup()
    while True:
        loop()
