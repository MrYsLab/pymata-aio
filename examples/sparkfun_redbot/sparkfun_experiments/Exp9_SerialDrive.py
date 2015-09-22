"""
Exp9_SerialDrive -- RedBot Experiment 9

  The first step to controlling the RedBot remotely is to first drive it
  from the Serial Monitor in a tethered setup.

  Hardware setup:
  After uploading this sketch, keep the RedBot tethered to your computer with
  the USB cable. Open up the Serial Monitor to send commands to the RedBot to
  drive.

  This sketch was written by SparkFun Electronics, with lots of help from
  the Arduino community. This code is completely free for any use.

  15 Dec 2014 B. Huang

  This experiment was inspired by Paul Kassebaum at Mathworks, who made
  one of the very first non-SparkFun demo projects and brought it to the
  2013 Open Hardware Summit in Boston. Thanks Paul!
 ***********************************************************************/
"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from library.redbot import RedBotMotors


board = PyMata3()
motors = RedBotMotors(board)


def setup():
    pass

def loop():
    speed = int(input())
    speed = throttle(speed)
    motors.drive(speed)


   # function for constraining the speed value between -255:255
def throttle(n, minn=-255, maxn=255):
    return max(min(maxn, n), minn)

if __name__ == "__main__":
    setup()
    while True:
        board.sleep(.1)
        loop()


