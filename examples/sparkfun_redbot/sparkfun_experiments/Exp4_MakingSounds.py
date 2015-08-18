#!/usr/bin/python3.4
"""/***********************************************************************
 * Exp4_MakingSounds -- RedBot Experiment 4
 *
 * Push the button (D12) to make some noise and start running!
 *
 * Hardware setup:
 * Plug the included RedBot Buzzer board into the Servo header labeled 9.
 *
 * This sketch was written by SparkFun Electronics,with lots of help from
 * the Arduino community. This code is completely free for any use.
 *
 * 23 Sept 2013 N. Seidle/M. Hord
 * 29 Oct 2014 B. Huang
 ***********************************************************************/"""

from pymata_aio.pymata3 import PyMata3
from RedBot import RedBotMotors
from pymata_aio.constants import Constants
# This line "includes" the RedBot library into your sketch.
# Provides special objects, methods, and functions for the RedBot.

board = PyMata3()

motors = RedBotMotors(board)

BUZZER_PIN = 9
BUTTON_PIN = 12

# Instantiate the motor control object. This only needs to be done once.


def setup():
    board.set_pin_mode(BUZZER_PIN, Constants.OUTPUT)  # configures the buzzerPin as an OUTPUT
    board.set_pin_mode(BUTTON_PIN, Constants.INPUT_PULLUP)  # configures the button as an INPUT



def loop():
    board.sleep(2)
    print(board.analog_read(17))



    if board.digital_read(BUTTON_PIN) == 0:
        board.play_tone(BUZZER_PIN, Constants.TONE_TONE, 2000, 1500)
        board.sleep(.125)
        # Turn off tone here
        # Turn on Tone again, at 2khz
        motors.drive(255) # Drive forward for a while
        board.sleep(2)
        board.play_tone(BUZZER_PIN, Constants.TONE_NO_TONE, 2000, 500)
        motors.drive(0) # Brake or stop the motors
        board.sleep(2)
        print(board.digital_read(BUTTON_PIN))

if __name__ == "__main__":
    setup()
    while True:
        loop()
# import the API class





