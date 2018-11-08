from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import asyncio

"""
Use a potentiometer connected to pin A0 to control
the brightness of an LED connected to pin 11
while reading the current temperature of a DSD18B20
one wire temperature sensor on pin 10.

Pin6 is a PWM pin.
"""


class DsPymata3Test:
    def __init__(self):

        self.DS18B20 = 10  # pin
        self.LED = 11  # pin 11
        self.POT = 0  # pin A0

        self.board = PyMata3()

        # set the pin modes the LED and POT
        self.board.set_pin_mode(self.LED, Constants.PWM)
        self.board.set_pin_mode(self.POT, Constants.ANALOG)
        self.board.set_sampling_interval(10)

        while True:
            try:
                # allows asyncio some time to process other tasks
                self.board.sleep(.01)

                # read the pot value and scale to control the PWM LED
                pot_value = self.board.analog_read(self.POT) // 4
                # print(pot_value)
                self.board.analog_write(self.LED, pot_value)

                # get the next temperature reading
                self.board.get_ds_temperature(10, self.the_call_back)
                self.board.sleep(.1)

            except KeyboardInterrupt:
                self.board.shutdown()

    def the_call_back(self, data):
        """
        Callback routine for temperature data.
        :param data: the data is in the form of a dictionary.
                     for example:  {'pin': 10, 'index': 0, 'celsius': 21.25}

        :return:
        """
        print(data)


# instantiate and go
DsPymata3Test()
