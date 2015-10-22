#!/usr/bin/env python3
"""
Basic demo of reporting Pixy data.

 This sketch is a good place to start if you're just getting started with
 Pixy and pymata-aio.  This program simply prints the detected object blocks.
"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.pymata3 import Constants


board = PyMata3()
got_blocks_counter = 0

def got_blocks(blocks):
    global got_blocks_counter
    got_blocks_counter += 1
    if got_blocks_counter % 40 == 0:
        print("Detected " + str(len(blocks)) + " blocks:")
        print(blocks)
        if len(blocks) > 0 and blocks[0] == 11:
            print("Wrong kind of block :)  Accidentally reported it as a digital again.  Oops.")
            return
        for block_index in range(len(blocks)):
            block = blocks[block_index]
            print("block {}: sig: {}  x: {} y: {} width: {} height: {}".format(
                    block_index, block["signature"], block["x"], block["y"], block["width"], block["height"]))

def got_pushbutton_press(current_value):
    print("Pushbutton " + str(current_value))
    #print(board.pixy_get_blocks())  # TODO: Implement this function.


def main():
    # Use a callback to display the readings in real time.
    board.pixy_init(cb=got_blocks, cb_type=Constants.CB_TYPE_DIRECT)

    # Only get the Pixy blocks when the pushbutton is pressed.
    #board.pixy_init()

    board.keep_alive(period=2)

    # Do nothing.  Just kill time to allow callback to keep running
    board.set_pin_mode(13, Constants.OUTPUT)
    board.set_pin_mode(12, Constants.INPUT, callback=got_pushbutton_press, cb_type=Constants.CB_TYPE_DIRECT)
    board.digital_write(12, 1)
    while True:
        print(".")
        board.digital_write(13, 1)
        board.sleep(1.0)
        board.digital_write(13, 0)
        board.sleep(1.0)

main()
