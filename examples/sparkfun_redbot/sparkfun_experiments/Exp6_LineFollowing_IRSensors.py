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
 * Revices, 2 Oct 2015 L Mathews
 ***********************************************************************/"""

import sys
import signal

from pymata_aio.pymata3 import PyMata3
from library.redbot import RedBotSensor

WIFLY_IP_ADDRESS = None            # Leave set as None if not using WiFly
WIFLY_IP_ADDRESS = "10.0.1.18"  # If using a WiFly on the RedBot, set the ip address here.
if WIFLY_IP_ADDRESS:
    board = PyMata3(ip_address=WIFLY_IP_ADDRESS)
else:
    # Use a USB cable to RedBot or an XBee connection instead of WiFly.
    COM_PORT = None # Use None for automatic com port detection, or set if needed i.e. "COM7"
    board = PyMata3(com_port=COM_PORT)

LEFT_LINE_FOLLOWER = 3  # pin number assignments for each IR sensor
CENTRE_LINE_FOLLOWER = 6
RIGHT_LINE_FOLLOWER = 7

IR_sensor_1 = RedBotSensor(board, LEFT_LINE_FOLLOWER)
IR_sensor_2 = RedBotSensor(board, CENTRE_LINE_FOLLOWER)
IR_sensor_3 = RedBotSensor(board, RIGHT_LINE_FOLLOWER)


def signal_handler(sig, frame):
    """Helper method to shutdown the RedBot if Ctrl-c is pressed"""
    print('\nYou pressed Ctrl+C')
    if board is not None:
        board.send_reset()
        board.shutdown()
    sys.exit(0)


def setup():
    signal.signal(signal.SIGINT, signal_handler)
    print("Welcome to Experiment 6!")
    print("------------------------")


def loop():
    board.sleep(0.1)
    print("IR Sensor Readings: {},   {},    {}".format(IR_sensor_1.read(), IR_sensor_2.read(), IR_sensor_3.read()))


if __name__ == "__main__":
    setup()
    while True:
        loop()
