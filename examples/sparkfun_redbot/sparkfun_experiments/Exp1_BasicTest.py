#!/usr/bin/python
"""
  Exp1_BasicTest -- RedBot Experiment 1

  Time to make sure the electronics work! To test everything out, we're
  going to blink the LED on the board.
"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

board = PyMata3(ip_address="r05.wlan.rose-hulman.edu")


def setup():
    """setup() function runs once at the very beginning."""
    board.set_pin_mode(13, Constants.OUTPUT)
    # The RedBot has an LED connected to pin 13.
    # Pins are all generic, so we have to first configure it
    # as an OUTPUT using this command.


def loop():
    """loop() function repeats over and over... forever!"""
    print("Blink sequence")
    board.digital_write(13, 1)  # Turns LED ON -- HIGH puts 5V on pin 13.
    board.sleep(0.500)          # "pauses" the program for 500 milliseconds
    board.digital_write(13, 0)  # Turns LED OFF -- LOW puts 0V on pin 13.
    board.sleep(0.500)          # "pauses" the program for 500 milliseconds
    # The total delay period is 1000 ms, or 1 second.


if __name__ == "__main__":
    setup()
    while True:
        loop()


# **********************************************************************
#  In Arduino, an LED is often connected to pin 13 for "debug" purposes.
#  This LED is used as an indicator to make sure that we're able to upload
#  code to the board. It's also a good indicator that your program is running.
# **********************************************************************
