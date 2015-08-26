"""
  Exp7_1_RotaryEncoder -- RedBot Experiment 7

  Knowing where your robot is can be very important. The RedBot supports
  the use of an encoder to track the number of revolutions each wheel has
  made, so you can tell not only how far each wheel has traveled but how
  fast the wheels are turning.

  This sketch was written by SparkFun Electronics, with lots of help from
  the Arduino community. This code is completely free for any use.

  8 Oct 2013 M. Hord
  Revised, 31 Oct 2014 B. Huang
 """

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from examples.sparkfun_redbot.sparkfun_experiments.library.redbot import RedBotMotors

# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()
motors = RedBotMotors(board)

encoder_pin_left = 16
encoder_pin_right = 10
left_encoder_count = 0
right_encoder_count = 0


# Configure



def left_encoder_callback(event=None):
    global left_encoder_count
    left_encoder_count += 1
    print("Left: {}".format(left_encoder_count))

def right_encoder_callback(event=None):
    global right_encoder_count
    right_encoder_count += 1
    print("Right: {}".format(right_encoder_count))

def setup():
    board.set_pin_mode(encoder_pin_left, Constants.INPUT, Constants.ENCODER)
    board.set_pin_mode(encoder_pin_right, Constants.INPUT, Constants.ENCODER)
    # board.encoder_config(encoder_pin_left, encoder_pin_right, left_encoder_callback)
    board.encoder_config(encoder_pin_left, encoder_pin_left, left_encoder_callback)
    board.encoder_config(encoder_pin_right, encoder_pin_right, right_encoder_callback)
def loop():
    # print(board.digital_read(10))
    pass

if __name__ == "__main__":
    setup()
    while True:
        board.sleep(.1)
        loop()


