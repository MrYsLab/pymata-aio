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
from library.redbot import RedBotSensor

# If using a WiFly on the RedBot
WIFLY_IP_ADDRESS = '137.112.19.15'  # Set this your your WiFly's ip address
board = PyMata3(ip_address=WIFLY_IP_ADDRESS, ip_port=None)

# if using a serial cable or XBee on the RedBot
#COM_PORT = None # Use None for automatic com port detection, or set if needed i.e. "COM7"
#board = PyMata3(com_port=COM_PORT)

# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.
LEFT_LINE_FOLLOWER = 3  # pin number assignments for each IR sensor
CENTRE_LINE_FOLLOWER = 6
RIGHT_LINE_FOLLOWER = 7


IR_sensor_1 = RedBotSensor(board, LEFT_LINE_FOLLOWER)
IR_sensor_2 = RedBotSensor(board, CENTRE_LINE_FOLLOWER)
IR_sensor_3 = RedBotSensor(board, RIGHT_LINE_FOLLOWER)


def setup():
    print("Welcome to Experiment 6!")
    print("------------------------")


def loop():
    board.sleep(0.1)
    print("IR Sensor Readings: {},   {},    {}".format(IR_sensor_1.read(), IR_sensor_2.read(), IR_sensor_3.read()))


if __name__ == "__main__":
    setup()
    while True:
        loop()
