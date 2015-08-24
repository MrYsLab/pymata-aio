"""//***********************************************************************
 * Exp6_LineFollowing_IRSensors -- RedBot Experiment 6
 *
 * This code reads the three line following sensors on A3, A6, and A7
 * and prints them out to the Serial Monitor. Upload this example to your
 * RedBot and open up the Serial Monitor by clicking the magnifying glass
 * in the upper-right hand corner.
 *
 * This sketch was written by SparkFun Electronics,with lots of help from
 * the Arduino community. This code is completely free for any use.
 *
 * 8 Oct 2013 M. Hord
 * Revised, 31 Oct 2014 B. Huang
 ***********************************************************************/"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from examples.sparkfun_redbot.sparkfun_experiments.library.redbot import RedBotMotors

# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()
motors = RedBotMotors(board)
LEFT_LINE_FOLLOWER = 3  # pin number assignments for each IR sensor
CENTRE_LINE_FOLLOWER = 6
RIGHT_LINE_FOLLOWER = 7


def setup():
    board.set_pin_mode(LEFT_LINE_FOLLOWER, Constants.ANALOG)  # initialize a sensor object on A3
    board.set_pin_mode(CENTRE_LINE_FOLLOWER, Constants.ANALOG)  # initialize a sensor object on A6
    board.set_pin_mode(RIGHT_LINE_FOLLOWER, Constants.ANALOG)  # initialize a sensor object on A7


def loop():
    print("IR Sensor Readings: {},   {},    {}".format(board.analog_read(LEFT_LINE_FOLLOWER), board.analog_read(
        CENTRE_LINE_FOLLOWER), board.analog_read(RIGHT_LINE_FOLLOWER)))


if __name__ == "__main__":
    setup()
    while True:
        board.sleep(1)
        loop()
