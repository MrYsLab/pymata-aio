#!/usr/bin/env python3
"""
Basic demo of reporting Pixy data.

 This sketch is a good place to start if you're just getting started with
 Pixy and pymata-aio.  This program simply prints the detected object blocks.
"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.pymata3 import Constants


# board = PyMata3(ip_address="r01.wlan.rose-hulman.edu")
board = PyMata3()

use_pixy_callback = False

def print_pixy_blocks(blocks):
    """ Prints the Pixy blocks data."""
    print("Detected " + str(len(blocks)) + " blocks:")
    if len(blocks) > 0 and not "signature" in blocks[0]:
        print("Something went wrong.  This does not appear to be a printable block.")
        board.shutdown()
        return
    for block_index in range(len(blocks)):
        block = blocks[block_index]
        print("  block {}: sig: {}  x: {} y: {} width: {} height: {}".format(
                block_index, block["signature"], block["x"], block["y"], block["width"], block["height"]))


def main():
    if use_pixy_callback:
        # Use a callback to display the Pixy readings.
        board.pixy_init(cb=print_pixy_blocks, cb_type=Constants.CB_TYPE_DIRECT)
    else:
        # Use the pixy_block property to display the readings.
        board.pixy_init()

    board.keep_alive(period=2)
    # Flash the LED while killing time.
    board.set_pin_mode(13, Constants.OUTPUT)
    while True:
        print(".")
        board.digital_write(13, 1)
        board.sleep(1.0)
        board.digital_write(13, 0)
        board.sleep(1.0)
        if not use_pixy_callback:
            print_pixy_blocks(board.pixy_get_blocks())

main()
