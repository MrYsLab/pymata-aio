#!/usr/bin/python
"""
  Exp5_Bumpers -- RedBot Experiment 5

  Now let's experiment with the whisker bumpers. These super-simple switches
  let you detect a collision before it really happens- the whisker will
  bump something before your robot crashes into it.

  This sketch was written by SparkFun Electronics, with lots of help from
  the Arduino community.
  This code is completely free for any use.
  Visit https://learn.sparkfun.com/tutorials/redbot-inventors-kit-guide
  for SIK information.

  8 Oct 2013 M. Hord
  Revised 30 Oct 2014 B. Huang
"""

from pymata_aio.pymata3 import PyMata3
from examples.sparkfun_redbot.sparkfun_experiments.library.redbot import RedBotMotors, RedBotBumper
from pymata_aio.constants import Constants
# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()
# Instantiate the motor control object. This only needs to be done once.
motors = RedBotMotors(board)

left_bumper = RedBotBumper(board, 3)  # initializes bumper object on pin 3
right_bumper = RedBotBumper(board, 11)  # initializes bumper object on pin 11

BUTTON_PIN = 12


def setup():
    # nothing here
    pass


def loop():
    motors.drive(255)

    left_bumper_state = left_bumper.read()
    # board.sleep(0.1)  # When using XBee a small sleep is necessary
    right_bumper_state = right_bumper.read()
    # board.sleep(0.1)  # When using XBee a small sleep is necessary
    if left_bumper_state == 0: # left bumper is bumped
        reverse()
        turnRight()

    if right_bumper_state == 0: # left bumper is bumped
        reverse()
        turnLeft()

def reverse():
    """backs up at full power"""
    motors.drive(-255)
    board.sleep(0.5)
    motors.brake()
    board.sleep(0.1)


def turnRight():
    """turns RedBot to the Right"""
    motors.leftMotor(-150)  # spin CCW
    motors.rightMotor(-150)  # spin CCW
    board.sleep(0.5)
    motors.brake();
    board.sleep(0.1)  # short delay to let robot fully stop


def turnLeft():
    """turns RedBot to the Left"""
    motors.leftMotor(150)  # spin CCW
    motors.rightMotor(150)  # spin CCW
    board.sleep(0.5)
    motors.brake();
    board.sleep(0.1)  # short delay to let robot fully stop


if __name__ == "__main__":
    setup()
    while True:
        loop()
# import the API class





