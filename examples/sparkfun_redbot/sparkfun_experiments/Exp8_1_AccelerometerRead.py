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
from pymata_aio.constants import Constants
from library.redbot import RedBotMotors
from library.accelerometer import RedBotAccel

#COM_PORT = None # Use automatic com port detection (the default)
COM_PORT = "COM10" # Manually specify the com port (optional)


board = PyMata3(com_port=COM_PORT)
motors = RedBotMotors(board)
accelerometer = RedBotAccel(board)


def setup():
    pass


def loop():
    if accelerometer.available():
        data = accelerometer.read()
        data = list(data)
        print(data) # wait for a button press to start driving.
        board.sleep(0.1)

if __name__ == "__main__":
    setup()
    while True:
        loop()
