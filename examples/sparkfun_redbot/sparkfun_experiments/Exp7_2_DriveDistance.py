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
from examples.sparkfun_redbot.sparkfun_experiments.library.redbot import RedBotMotors
import math
# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()
motors = RedBotMotors(board)
encoderPinLeft = 16
encoderPinRight = 10

buttonPin = 12

countsPerRev = 192    # 4 pairs of N-S x 48:1 gearbox = 192 ticks per wheel rev

wheelDiam = 2.56 # diam = 65mm / 25.4 mm/in
wheelCirc = math.pi * wheelDiam

# variables used to store the left and right encoder counts.
lCount = 0
rCount = 0


def setup():
    board.set_pin_mode(buttonPin, Constants.INPUT)
    board.digital_write(buttonPin, 1)  # writing pin high sets the pull-up resistor



def loop():
    # wait for a button press to start driving.
    if board.digital_read(buttonPin) == 0:
        driveDistance(12, 150)  # drive 12 inches at motor_power = 150


def driveDistance(distance, motorPower):
    global lCount
    global rCount
    lCount= 0
    rCount = 0
    numRev = float(distance/wheelCirc)

    # debug
    print("drive_distance() {} inches at {} power".format(distance,motorPower))


    print(numRev)
    motors.clearEnc()  # clear the encoder count
    motors.drive(motorPower)
    # TODO: Find the 'proper' way to access these variables
    iteration = 0
    while rCount< numRev*countsPerRev:

        lCount = motors.getTicks(encoderPinLeft)
        rCount = motors.getTicks(encoderPinRight)

        print("{}       {}".format(lCount,rCount))  # stores the encoder count to a variable
        print(numRev*countsPerRev)
        board.sleep(0.01)
    #  if either left or right motor are more than 5 revolutions, stop
    motors.brake()

if __name__ == "__main__":
    setup()
    while True:
        loop()
        board.sleep(.01)
        #  print("Encoder Read: {}".format(board.encoder_read(encoder_pin_right)))
