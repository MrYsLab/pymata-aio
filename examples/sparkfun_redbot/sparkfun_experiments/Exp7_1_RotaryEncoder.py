"""
  Exp7_1_RotaryEncoder -- RedBot Experiment 7

  Knowing where your robot is can be very important. The RedBot supports
  the use of an encoder to track the number of revolutions each wheel has
  made, so you can tell not only how far each wheel has traveled but how
  fast the wheels are turning.

  This sketch was written by SparkFun Electronics, with lots of help from
  the Arduino community. This code is completely free for any use.

  8 Oct 2013 M. Hord
  Revised, 31 Oct 2014 B. Huang+
 """

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from library.redbot import RedBotMotors, RedBotEncoder

# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()
motors = RedBotMotors(board)
encoders = RedBotEncoder(board)

ENCODER_PIN_LEFT = 16
ENCODER_PIN_RIGHT = 10

BUTTON_PIN = 12

COUNTS_PER_REV = 192    # 4 pairs of N-S x 48:1 gearbox = 192 ticks per wheel rev


def setup():
    board.set_pin_mode(BUTTON_PIN, Constants.INPUT)
    board.digital_write(BUTTON_PIN, 1)  # writing pin high sets the pull-up resistor
    print("Left     Right")
    print("==============")


def loop():
    # wait for a button press to start driving.
    if board.digital_read(BUTTON_PIN) == 0:
        board.sleep(0.2)
        if  board.digital_read(BUTTON_PIN) == 0:
            encoders.clearEnc()  # Reset the counters
            motors.drive(150)  # Start driving forward

    left_count = encoders.getTicks(ENCODER_PIN_LEFT)
    right_count = encoders.getTicks(ENCODER_PIN_RIGHT)

    print("{}       {}".format(left_count, right_count))  # stores the encoder count to a variable

    #  if either left or right motor are more than 5 revolutions, stop
    if left_count >= 5 * COUNTS_PER_REV or right_count >= 5 * COUNTS_PER_REV:
        motors.brake()

if __name__ == "__main__":
    setup()
    while True:
        loop()
        #  print("Encoder Read: {}".format(board.encoder_read(encoder_pin_right)))
