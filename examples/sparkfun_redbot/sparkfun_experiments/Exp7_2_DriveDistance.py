"""
  Exp7_2_DriveDistance -- RedBot Experiment 7.2

  In an earlier experiment, we used a combination of speed and time to
  drive a certain distance. Using the encoders, we can me much more accurate.
  In this example, we will show you how to setup your robot to drive a certain
  distance regardless of the motorPower.

  This sketch was written by SparkFun Electronics, with lots of help from
  the Arduino community. This code is completely free for any use.

  8 Oct 2013 M. Hord
  Revised, 31 Oct 2014 B. Huang
"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from library.redbot import RedBotMotors,RedBotEncoder
import math
# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.


board = PyMata3()
encoders = RedBotEncoder(board)
motors = RedBotMotors(board)
encoder_pin_left = 16
encoder_pin_right = 10

button_pin = 12

counts_per_rev = 192    # 4 pairs of N-S x 48:1 gearbox = 192 ticks per wheel rev

wheel_diam = 2.56 # diam = 65mm / 25.4 mm/in
wheel_circ = math.pi * wheel_diam

# variables used to store the left and right encoder counts.
left_count = 0
right_count = 0


def setup():
    board.set_pin_mode(button_pin, Constants.INPUT)
    board.digital_write(button_pin, 1)  # writing pin high sets the pull-up resistor



def loop():
    # wait for a button press to start driving.
    if board.digital_read(button_pin) == 0:
        board.sleep(0.05)
        if board.digital_read(button_pin) == 0:
            driveDistance(12, 150)  # drive 12 inches at motor_power = 150


def driveDistance(distance, motor_power):
    global left_count
    global right_count
    left_count= 0
    right_count = 0
    numRev = float(distance/wheel_circ)

    # debug
    print("drive_distance() {} inches at {} power".format(distance,motor_power))


    print(numRev)
    encoders.clear_enc()  # clear the encoder count
    motors.drive(motor_power)
    # TODO: Find the 'proper' way to access these variables
    iteration = 0
    while right_count< numRev*counts_per_rev:

        left_count = encoders.get_ticks(encoder_pin_left)
        right_count = encoders.get_ticks(encoder_pin_right)
        print("{}       {}".format(left_count,right_count))  # stores the encoder count to a variable
        # print(numRev*counts_per_rev)
        board.sleep(0.01)
    #  if either left or right motor are more than 5 revolutions, stop
    motors.brake()

if __name__ == "__main__":
    setup()
    while True:
        loop()
        board.sleep(.01)
        #  print("Encoder Read: {}".format(board.encoder_read(encoder_pin_right)))
