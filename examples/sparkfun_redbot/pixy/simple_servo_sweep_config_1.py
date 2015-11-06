#!/usr/bin/env python3
"""
Demo of using the pan and tilt servo kit.

 This demo assumes you have purchased the Pixy pan and tilt kit.  You can connect the servos in two places:
   1. Just plug the servos into servo ports on the Arduino 3, 9, or 10 (NOT 11!).  This demo uses 3 and 10.
   2. Plug the servos in on the Pixy board as recommended here http://cmucam.org/projects/cmucam5/wiki/Assembling_pantilt_Mechanism

 This code assumes you have connected the servos connected to the RedBot board NOT to the Pixy board.

"""

from pymata_aio.pymata3 import PyMata3

# board = PyMata3(arduino_wait=0, sleep_tune=0.0001, ip_address="r01.wlan.rose-hulman.edu")
board = PyMata3(sleep_tune=0.0001) # Since the Pixy can transmit a lot of data reduce the asyncio sleep time to reduce the possibility of lagging behind messages.

# Servo connection locations on the RedBot board.
PIN_PAN_SERVO = 3
PIN_TILT_SERVO = 10


def print_pixy_blocks(blocks):
    """ Prints the Pixy blocks data."""
    print("Detected " + str(len(blocks)) + " Pixy blocks:")
    for block_index in range(len(blocks)):
        block = blocks[block_index]
        print("  block {}: sig: {}  x: {} y: {} width: {} height: {}".format(
                block_index, block["signature"], block["x"], block["y"], block["width"], block["height"]))


def main():
    board.keep_alive(period=2)
    board.pixy_init()
    board.servo_config(PIN_PAN_SERVO)
    board.servo_config(PIN_TILT_SERVO)
    while True:
        for pan_deg in range(90, 170, 2):
            board.analog_write(PIN_PAN_SERVO, pan_deg)
            board.sleep(0.05)
        print_pixy_blocks(board.pixy_get_blocks())
        for pan_deg in range(170, 90, -2):
            board.analog_write(PIN_PAN_SERVO, pan_deg)
            board.sleep(0.05)
        print_pixy_blocks(board.pixy_get_blocks())

        # Test the tilt servo.
        for tilt_deg in range(90, 150, 2):
            board.analog_write(PIN_TILT_SERVO, tilt_deg)
            board.sleep(0.05)
        print_pixy_blocks(board.pixy_get_blocks())
        for tilt_deg in range(150, 30, -2):
            board.analog_write(PIN_TILT_SERVO, tilt_deg)
            board.sleep(0.05)
        print_pixy_blocks(board.pixy_get_blocks())
        for tilt_deg in range(30, 90, 2):
            board.analog_write(PIN_TILT_SERVO, tilt_deg)
            board.sleep(0.05)
        print_pixy_blocks(board.pixy_get_blocks())

        for pan_deg in range(90, 10, -2):
            board.analog_write(PIN_PAN_SERVO, pan_deg)
            board.sleep(0.05)
        print_pixy_blocks(board.pixy_get_blocks())
        for pan_deg in range(10, 90, 2):
            board.analog_write(PIN_PAN_SERVO, pan_deg)
            board.sleep(0.05)
        print_pixy_blocks(board.pixy_get_blocks())

main()
