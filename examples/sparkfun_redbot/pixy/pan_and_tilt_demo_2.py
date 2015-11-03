#!/usr/bin/env python3
"""
Demo of using the pan and tilt servo kit.

 This demo assumes you have purchased the Pixy pan and tilt kit.  You can connect the servos in two places:
   1. Just plug the servos into servo ports on the Arduino 3, 9, or 10 (NOT 11!).  This demo uses 3 and 10.
   2. Plug the servos in on the Pixy board as recommended here http://cmucam.org/projects/cmucam5/wiki/Assembling_pantilt_Mechanism

 This version of the code assumes you have connected the servo to the Pixy board directly.
 Warning! The tilt servo can sometimes act sporadic so we recommend option #1 or *only using the pan servo*.

 In addition to the pan and tilt demo you also need all of the setup that was necessar for the pixy_hello_world.py program....
   In order to run this example you of course you need a Pixy and a RedBot with an ICSP header.
   The cable goes such that the red wire of the ribbon cable is on bottom.
   Also make sure you have nothing plugged into pin 11 which is just above that header.
   The Pixy uses pins 11 and 12, but the button does not seem to interfere with Pixy as long as
   it doesn't get pressed (just don't try to use the button and Pixy at the same time).
   You also need to make sure the Pixy has been trained to track a color
     (http://cmucam.org/projects/cmucam5/wiki/Teach_Pixy_an_object).
"""
import asyncio
import math

from pymata_aio.pymata3 import PyMata3
from pymata_aio.pymata3 import Constants


# board = PyMata3(ip_address="r01.wlan.rose-hulman.edu")
board = PyMata3()

# Pixy x-y position values
PIXY_MIN_X = 0
PIXY_MAX_X = 319
PIXY_MIN_Y = 0
PIXY_MAX_Y = 199
X_CENTER = ((PIXY_MAX_X - PIXY_MIN_X) / 2)
Y_CENTER = ((PIXY_MAX_Y - PIXY_MIN_Y) / 2)

# Servo values
PIXY_RCS_MIN_POS = 0
PIXY_RCS_MAX_POS = 1000
PIXY_RCS_CENTER_POS = ((PIXY_RCS_MAX_POS - PIXY_RCS_MIN_POS) / 2)


class ServoLoop:

    def __init__(self, proportional_gain, derivator_gain):
        self.position = PIXY_RCS_CENTER_POS
        self.proportional_gain = proportional_gain
        self.derivator_gain = derivator_gain
        self.previous_error = 0x80000000

    def update(self, error):
        if self.previous_error != 0x80000000:
            velocity = (error * self.proportional_gain + (error - self.previous_error) * self.derivator_gain) / math.pow(2, 10)
            self.position += velocity
            if self.position > PIXY_RCS_MAX_POS:
                self.position = PIXY_RCS_MAX_POS
            if self.position < PIXY_RCS_MIN_POS:
                self.position = PIXY_RCS_MIN_POS
        self.previous_error = error

pan_loop = ServoLoop(100.0, 300.0)  # Reduced the default values
tilt_loop = ServoLoop(100.0, 300.0) # Reduced the default values

def pixy_value_update(blocks):
    """ Prints the Pixy blocks data."""
    if len(blocks) > 0:
        pan_error = X_CENTER - blocks[0]["x"]
        titl_error = blocks[0]["y"] - Y_CENTER
        pan_loop.update(pan_error)
        tilt_loop.update(titl_error)

        loop = asyncio.get_event_loop()
        if loop.is_running():
            # This is the version that will be used since we are in a callback, but I wanted to show how to
            # properly protect against calls to board.something when you don't know if you are in the non-async
            # land vs when you are currently executing code from within async land.
            asyncio.ensure_future(board.core.pixy_set_servos(int(pan_loop.position), int(tilt_loop.position)))
        else:
            board.pixy_set_servos(int(pan_loop.position), int(tilt_loop.position))


def print_pixy_blocks(blocks):
    """ Prints the Pixy blocks data."""
    print("Detected " + str(len(blocks)) + " Pixy blocks:")
    for block_index in range(len(blocks)):
        block = blocks[block_index]
        print("  block {}: sig: {}  x: {} y: {} width: {} height: {}".format(
                block_index, block["signature"], block["x"], block["y"], block["width"], block["height"]))


def main():
    board.pixy_init(cb=pixy_value_update, cb_type=Constants.CB_TYPE_DIRECT)
    board.keep_alive(period=2)
    while True:
        board.sleep(1.0)
        print_pixy_blocks(board.pixy_get_blocks())

main()
