"""
  Exp8_1_AccelerometerRead -- RedBot Experiment 8.1

  Measuring speed, velocity, and acceleration are all key
  components to robotics. This first experiment will introduce
  you to using the Accelerometer sensor on the RedBot.

  Hardware setup:
  You'll need to attach the RedBot Accelerometer board to hader on the upper
  right side of the mainboard. See the manual for details on how to do this.

  This sketch was written by SparkFun Electronics, with lots of help from
  the Arduino community. This code is completely free for any use.

  8 Oct 2013 M. Hord
  Revised, 31 Oct 2014 B. Huang

  8 Oct 2013 M. Hord

  This experiment was inspired by Paul Kassebaum at Mathworks, who made
  one of the very first non-SparkFun demo projects and brought it to the
  2013 Open Hardware Summit in Boston. Thanks Paul!
 """

from pymata_aio.pymata3 import PyMata3
from library.redbot import RedBotMotors
from library.accelerometer import RedBotAccel

WIFLY_IP_ADDRESS = None            # Leave set as None if not using WiFly
WIFLY_IP_ADDRESS = "10.0.1.18"  # If using a WiFly on the RedBot, set the ip address here.
if WIFLY_IP_ADDRESS:
    board = PyMata3(ip_address=WIFLY_IP_ADDRESS)
else:
    # Use a USB cable to RedBot or an XBee connection instead of WiFly.
    COM_PORT = None # Use None for automatic com port detection, or set if needed i.e. "COM7"
    board = PyMata3(com_port=COM_PORT)

motors = RedBotMotors(board)
accelerometer = RedBotAccel(board)


def setup():
    pass


def loop():
    if accelerometer.available():
        accelerometer.read()
        """Display out the X, Y, and Z - axis "acceleration" measurements and also
        the relative angle between the X-Z, Y-Z, and X-Y vectors. (These give us
        the orientation of the RedBot in 3D space."""
        print("({}, {}, {}) -- [{:4.2f}, {:4.2f}, {:4.2f}]".format(accelerometer.x, accelerometer.y, accelerometer.z,
                                                               accelerometer.angleXZ, accelerometer.angleYZ,
                                                               accelerometer.angleXY))

        board.sleep(0.2)  # short delay in between readings


if __name__ == "__main__":
    setup()
    while True:
        loop()
