#!/usr/bin/python
"""
  Exp2_DriveForward -- RedBot Experiment 2

  Drive forward and stop.

  Hardware setup:
  The Power switch must be on, the motors must be connected, and the board must be receiving power
  from the battery. The motor switch must also be switched to RUN.
"""

from pymata_aio.pymata3 import PyMata3
from library.redbot import RedBotMotors
# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

WIFLY_IP_ADDRESS = None            # Leave set as None if not using WiFly
WIFLY_IP_ADDRESS = "137.112.217.88"  # If using a WiFly on the RedBot, set the ip address here.
if WIFLY_IP_ADDRESS:
    board = PyMata3(ip_address=WIFLY_IP_ADDRESS)
else:
    # Use a USB cable to RedBot or an XBee connection instead of WiFly.
    COM_PORT = None # Use None for automatic com port detection, or set if needed i.e. "COM7"
    board = PyMata3(com_port=COM_PORT)

motors = RedBotMotors(board)
# Instantiate the motor control object. This only needs to be done once.


def setup():
    print("Left and right motors at full speed forward")
    motors.drive(255)   # Turn on Left and right motors at full speed forward.
    board.sleep(2.0)    # Waits for 2 seconds
    print("Stop both motors")
    motors.stop()       # Stops both motors
    board.shutdown()


def loop():
    # Nothing here. We'll get to this in the next experiment.
    pass


if __name__ == "__main__":
    setup()

