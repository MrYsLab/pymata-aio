#!/usr/bin/env python3
"""
Demo of using the pan and tilt servo kit.

 This demo assumes you have purchased the Pixy pan and tilt kit.  You can connect the servos in two places:
   1. Just plug the servos into servo ports on the Arduino 3, 9, or 10 (NOT 11!).  This demo uses 3 and 10.
   2. Plug the servos in on the Pixy board as recommended here http://cmucam.org/projects/cmucam5/wiki/Assembling_pantilt_Mechanism

 This code assumes you have connected the servos connected to the Pixy board directly.
 Due to power limitations we only use the pan servo in this demo.
"""

from pymata_aio.pymata3 import PyMata3

# board = PyMata3(arduino_wait=0, sleep_tune=0.0001, ip_address="r01.wlan.rose-hulman.edu")
board = PyMata3(sleep_tune=0.0001) # Since the Pixy can transmit a lot of data reduce the asyncio sleep time to reduce the possibility of lagging behind messages.


# Servo values
PIXY_RCS_MIN_POS = 0
PIXY_RCS_MAX_POS = 1000
PIXY_RCS_CENTER_POS = 500

def main():
    board.keep_alive(period=2)
    board.pixy_init()
    while True:
        for s0 in range(PIXY_RCS_CENTER_POS, PIXY_RCS_MAX_POS, 10):
            board.pixy_set_servos(s0, PIXY_RCS_CENTER_POS)
            board.sleep(0.05)
        for s0 in range(PIXY_RCS_MAX_POS, PIXY_RCS_MIN_POS, -10):
            board.pixy_set_servos(s0, PIXY_RCS_CENTER_POS)
            board.sleep(0.05)
        for s0 in range(PIXY_RCS_MIN_POS, PIXY_RCS_CENTER_POS, 10):
            board.pixy_set_servos(s0, PIXY_RCS_CENTER_POS)
            board.sleep(0.05)
        print("Sweep complete")
        board.sleep(1.0)

main()
