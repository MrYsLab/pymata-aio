#!/usr/bin/env python3
"""
Basic demo of reporting Pixy data.

 This sketch is a good place to start if you're just getting started with
 Pixy and pymata-aio.  This program simply prints the detected object blocks.
"""

from pymata_aio.pymata3 import PyMata3


def got_blocks(blocks):
    print("Detected " + str(len(blocks)) + "blocks:")
    for block_index in range(len(blocks)):
        block = blocks[block_index]
        print("block {1:3d}: sig: {1:3d}  x: {1:3d} y: {1:3d} width: {1:3d} height: {1:3d}".format(
                block_index, block.signature, block.x, block.y, block.width, block.height))

def main():
    board = PyMata3(ip_address="r05.wlan.rose-hulman.edu")
    board.pixy_init(got_blocks)
    while True:
        board.sleep(0.025) # Do nothing.  Allow callback to keep running

main()
