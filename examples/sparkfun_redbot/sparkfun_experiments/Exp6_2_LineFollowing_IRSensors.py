"""/***********************************************************************
 * Exp6_2_LineFollowing_IRSensors -- RedBot Experiment 6
 *
 * This code reads the three line following sensors on A3, A6, and A7
 * and prints them out to the Serial Monitor. Upload this example to your
 * RedBot and open up the Serial Monitor by clicking the magnifying glass
 * in the upper-right hand corner.
 *
 * This is a real simple example of a line following algorithm. It has
 * a lot of room for improvement, but works fairly well for a curved track.
 * It does not handle right angles reliably -- maybe you can come up with a
 * better solution?
 *
 * This sketch was written by SparkFun Electronics,with lots of help from
 * the Arduino community. This code is completely free for any use.
 *
 * 18 Feb 2015 B. Huang
 ***********************************************************************/"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from library.redbot import RedBotMotors, RedBotSensor

# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()

left = RedBotSensor(board, 3)  # pin number assignments for each IR sensor
centre = RedBotSensor(board, 4)
right = RedBotSensor(board, 7)

# constants that are used in the code. LINETHRESHOLD is the level to detect
# if the sensor is on the line or not. If the sensor value is greater than this
# the sensor is above a DARK line.
#
# SPEED sets the nominal speed

LINE_THRESHOLD = 800
SPEED = 60  # sets the nominal speed. Set to any number 0-255

motors = RedBotMotors(board)


def setup():
    print("Welcome to Experiment 6.2 - Line Following")
    print("------------------------------------------")
    board.sleep(2)
    print("IR Sensor Readings:")
    board.sleep(0.5)


def loop():
    left_ir_reading = left.read()
    centre_ir_reading = centre.read()
    right_ir_reading = right.read()

    print("IR Sensor Readings: {},   {},    {}".format(left_ir_reading, centre_ir_reading, right_ir_reading))

    if centre_ir_reading > LINE_THRESHOLD:
        left_speed = -SPEED
        right_speed = SPEED
    elif right_ir_reading > LINE_THRESHOLD:
        left_speed = -(SPEED + 50)
        right_speed = SPEED - 50
    elif left_ir_reading > LINE_THRESHOLD:
        left_speed = -(SPEED - 50)
        right_speed = SPEED + 50
    else:
        left_speed = 50  # If all sensors are seeing black, then set speed to slow until a sensor picks up
        # white again
        right_speed = 50
    if (left_ir_reading > LINE_THRESHOLD) & (centre_ir_reading > LINE_THRESHOLD) & (right_ir_reading > LINE_THRESHOLD):
        motors.brake()
    else:
        motors.leftMotor(left_speed)
        motors.rightMotor(right_speed)
    board.sleep(0.1)  # add a delay to decrease sensitivity


if __name__ == "__main__":
    setup()
    while True:
        loop()
