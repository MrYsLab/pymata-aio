#!/usr/bin/python
"""
  Exp3_Turning -- RedBot Experiment 3

  Explore turning with the RedBot by controlling the Right and Left motors
  separately.

  Hardware setup:
  This code requires only the most basic setup: the motors must be
  connected, and the board must be receiving power from the battery pack.
 """

from pymata_aio.pymata3 import PyMata3
from examples.sparkfun_redbot.sparkfun_experiments.library.redbot import RedBotMotors
# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()

motors = RedBotMotors(board)
# Instantiate the motor control object. This only needs to be done once.


def setup():
    print("Driving forward")
    # drive forward -- instead of using motors.drive(); Here is another way.
    motors.rightMotor(150)  # Turn on right motor clockwise medium power (motorPower = 150)
    motors.leftMotor(150)  # Turn on left motor counter clockwise medium power (motorPower = 150)
    board.sleep(1.0)  # Waits for 1000 ms.
    motors.brake();

    print("Pivot-- turn to right")
    # pivot -- spinning both motors CCW causes the RedBot to turn to the right
    motors.rightMotor(-100)  # Turn on right motor clockwise medium power (motorPower = 150)
    motors.leftMotor(-100)  # Turn on left motor counter clockwise medium power (motorPower = 150)
    board.sleep(0.500)
    motors.brake()
    board.sleep(0.500)

    print("Driving Straight to Finish")
    # drive forward -- instead of using motors.drive(); Here is another way.
    motors.rightMotor(150)  # Turn on right motor clockwise medium power (motorPower = 150)
    motors.leftMotor(-150)  # Turn on left motor counter clockwise medium power (motorPower = 150)
    motors.drive(255)
    board.sleep(1.0)
    motors.brake()  # brake() motors


def loop():
    # Figure 8 pattern -- Turn Right, Turn Left, Repeat
    print("Veering Right")
    motors.leftMotor(-200)  # Left motor CCW at 200
    motors.rightMotor(80)   # Right motor CW at 80
    board.sleep(2.0)
    print("Veering Left")
    motors.leftMotor(-80)   # Left motor CCW at 80
    motors.rightMotor(200)  # Right motor CW at 200
    board.sleep(2.0)
    pass


if __name__ == "__main__":
    setup()
    while True:
        loop()
