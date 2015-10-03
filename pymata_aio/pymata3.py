"""
Copyright (c) 2015 Alan Yorinks All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import asyncio
import sys
import logging

from .pymata_core import PymataCore


class PyMata3:
    """
    This class exposes and implements a proxy API for the pymata_core asyncio
    API,  If your application does not use asyncio directly, this is
    the API that you should use..
    """

    def __init__(self, arduino_wait=2, log_output=False, com_port=None,
                 ip_address=None, ip_port=2000, ip_handshake='*HELLO*'):
        """
        Constructor for the PyMata3 API
        If log_output is set to True, a log file called 'pymata_log'
        will be created in the current directory and all pymata_aio output
        will be redirected to the log with no output appearing on the console.

        :param arduino_wait: Amount of time to allow Arduino to finish its
                             reset (2 seconds for Uno, Leonardo can be 0)
        :param log_output: If True, pymata_aio.log is created and all
                            console output is redirected to this file.
        :param com_port: If specified, auto port detection will not be
                         performed and this com port will be used.
        :param ip_address: If using a WiFly module, set its address here
        :param ip_port: Port to used with ip_address
        :param ip_handshake: Connectivity handshake string sent by IP device

        :returns: None
        """
        self.log_out = log_output
        self.sleep_tune = .001
        self.core = PymataCore(arduino_wait, self.sleep_tune, log_output,
                               com_port, ip_address, ip_port, ip_handshake)
        self.core.start()
        self.sleep(1)

    def analog_read(self, pin):
        """
        Retrieve the last data update for the specified analog pin.
        It is intended for a polling application.

        :param pin: Analog pin number (ex. A2 is specified as 2)
        :returns: Last value reported for the analog pin
        """
        loop = asyncio.get_event_loop()
        value = loop.run_until_complete(self.core.analog_read(pin))
        return value

    def analog_write(self, pin, value):
        """
        Set the selected PWM pin to the specified value.

        :param pin: PWM pin number
        :param value:  Set the selected pin to the specified
                       value. 0-0x4000 (14 bits)
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.analog_write(pin, value))

    def digital_read(self, pin):
        """
        Retrieve the last data update for the specified digital pin.
        It is intended for a polling application.

        :param pin: Digital pin number
        :returns: Last value reported for the digital pin
        """
        loop = asyncio.get_event_loop()
        value = loop.run_until_complete(self.core.digital_read(pin))
        return value

    def digital_write(self, pin, value=0):
        """
        Set the specified digital input pin to the provided value

        :param pin: Digital pin to be set
        :param value: 0 or 1
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.digital_write(pin, value))

    def disable_analog_reporting(self, pin):
        """
        Disables analog reporting for a single analog pin.

        :param pin: Analog pin number. For example for A0, the number is 0.
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.disable_analog_reporting(pin))

    def disable_digital_reporting(self, pin):
        """
        Disables digital reporting. By turning reporting off for this pin,
        reporting is disabled for all 8 bits in the "port"

        :param pin: Pin and all pins for this port
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.disable_digital_reporting(pin))

    def encoder_config(self, pin_a, pin_b, cb=None, cb_type=None,
                       hall_encoder=False):
        """
        This command enables the rotary encoder (2 pin + ground) and will
        enable encoder reporting.

        This is a FirmataPlus feature.

        Encoder data is retrieved by performing a digital_read from
        pin a (encoder pin 1)

        :param pin_a: Encoder pin 1.
        :param pin_b: Encoder pin 2.
        :param cb: callback function to report encoder changes
        :param cb_type: Constants.CB_TYPE_DIRECT = direct call
                        or Constants.CB_TYPE_ASYNCIO = asyncio coroutine
        :param hall_encoder: wheel hall_encoder - set to True to select
                             hall encoder support support.
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.encoder_config(pin_a, pin_b,
                                                         cb, cb_type,
                                                         hall_encoder))

    def encoder_read(self, pin):
        """
        This method retrieves the latest encoder data value.
        It is a FirmataPlus feature.

        :param pin: Encoder Pin
        :returns: encoder data value
        """
        loop = asyncio.get_event_loop()
        try:
            value = loop.run_until_complete(self.core.encoder_read(pin))
            return value
        except RuntimeError:
            self.shutdown()

    def enable_analog_reporting(self, pin):
        """
        Enables analog reporting for a single analog pin,

        :param pin: Analog pin number. For example for A0, the number is 0.
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.enable_analog_reporting(pin))

    def enable_digital_reporting(self, pin):
        """
        Enables digital reporting. By turning reporting on for all
        8 bits in the "port".
        This is part of Firmata's protocol specification.

        :param pin: Pin and all pins for this port
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.enable_digital_reporting(pin))

    def extended_analog(self, pin, data):
        """
        This method will send an extended-data analog write command
        to the selected pin..

        :param pin: 0 - 127
        :param data: 0 - 0-0x4000 (14 bits)
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.extended_analog(pin, data))

    def get_analog_latch_data(self, pin):
        """
        A list is returned containing the latch state for the pin, the
        latched value, and the time stamp
        [pin_num, latch_state, latched_value, time_stamp]
        If the the latch state is LATCH_LATCHED, the table is reset
        (data and timestamp set to zero)
        It is intended to be used for a polling application.

        :param pin: Pin number.
        :returns:  [latched_state, threshold_type, threshold_value,
                    latched_data, time_stamp]
        """
        loop = asyncio.get_event_loop()
        l_data = loop.run_until_complete(self.core.get_analog_latch_data(pin))
        return l_data

    def get_analog_map(self, cb=None):
        """
        This method requests and returns an analog map.

        :param cb: Optional callback reference
        :returns: An analog map response or None if a timeout occurs
        """
        loop = asyncio.get_event_loop()
        report = loop.run_until_complete(self.core.get_analog_map())
        if cb:
            cb(report)
        else:
            return report

    def get_capability_report(self, raw=True, cb=None):
        """
        This method retrieves the Firmata capability report

        :param raw: If True, it either stores or provides the callback
                      with a report as list.
                    If False, prints a formatted report to the console
        :param cb: Optional callback reference to receive a raw report
        :returns: capability report
        """
        loop = asyncio.get_event_loop()

        report = loop.run_until_complete(self.core.get_capability_report())
        if raw:
            if cb:
                cb(report)
            else:
                return report
        else:
            # noinspection PyProtectedMember
            self.core._format_capability_report(report)

    def get_digital_latch_data(self, pin):
        """
        A list is returned containing the latch state for the pin, the
        latched value, and the time stamp

        [pin_num, latch_state, latched_value, time_stamp]

        If the the latch state is LATCH_LATCHED, the table is reset
        (data and timestamp set to zero).
        It is intended for use by a polling application.

        :param pin: Pin number.
        :returns:  [latched_state, threshold_type, threshold_value,
                    latched_data, time_stamp]
        """
        loop = asyncio.get_event_loop()
        l_data = loop.run_until_complete(self.core.get_digital_latch_data(pin))
        return l_data

    def get_firmware_version(self, cb=None):
        """
        This method retrieves the Firmata firmware version

        :param cb: Reference to a callback function
        :returns:If no callback is specified, the firmware version
        """
        loop = asyncio.get_event_loop()

        version = loop.run_until_complete(
            self.core.get_firmware_version())
        if cb:
            cb(version)
        else:
            return version

    def get_protocol_version(self, cb=None):
        """
        This method retrieves the Firmata protocol version

        :param cb: Optional callback reference.
        :returns:If no callback is specified, the firmware version
        """
        loop = asyncio.get_event_loop()
        version = loop.run_until_complete(self.core.get_protocol_version())

        if cb:
            cb(version)
        else:
            return version

    def get_pin_state(self, pin, cb=None):
        """
        This method retrieves a pin state report for the specified pin

        :param pin: Pin of interest
        :param cb: optional callback reference
        :returns: pin state report
        """
        loop = asyncio.get_event_loop()
        report = loop.run_until_complete(self.core.get_pin_state(pin))
        if cb:
            cb(report)
        else:
            return report

    def get_pymata_version(self):
        """
        This method retrieves the PyMata version number

        :returns: PyMata version number.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.get_pymata_version())

    def i2c_config(self, read_delay_time=0):
        """
        This method configures Arduino i2c with an optional read delay time.

        :param read_delay_time: firmata i2c delay time
        :returns: No return value
        """
        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.core.i2c_config(read_delay_time))

    def i2c_read_data(self, address):
        """
        Retrieve result of last data read from i2c device.
        i2c_read_request should be called before trying to retrieve data.
        It is intended for use by a polling application.

        :param address: i2c
        :returns: last data read or None if no data is present.
        """
        loop = asyncio.get_event_loop()

        value = loop.run_until_complete(self.core.i2c_read_data(address))
        return value

    def i2c_read_request(self, address, register, number_of_bytes, read_type,
                         cb=None, cb_type=None):
        """
        This method issues an i2c read request for a single read,continuous
        read or a stop, specified by the read_type.
        Because different i2c devices return data at different rates,
        if a callback is not specified, the user must first call this method
        and then call i2c_read_data  after waiting for sufficient time for the
        i2c device to respond.
        Some devices require that transmission be restarted
        (e.g. MMA8452Q accelerometer).
        Use I2C_READ | I2C_RESTART_TX for those cases.

        :param address: i2c device
        :param register: i2c register number
        :param number_of_bytes: number of bytes to be returned
        :param read_type:  Constants.I2C_READ, Constants.I2C_READ_CONTINUOUSLY
                           or Constants.I2C_STOP_READING.
        Constants.I2C_RESTART_TX may be OR'ed when required
        :param cb: optional callback reference
        :param cb_type: Constants.CB_TYPE_DIRECT = direct call or
                        Constants.CB_TYPE_ASYNCIO = asyncio coroutine
        :returns: No return value        """

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.i2c_read_request(address, register,
                                                           number_of_bytes,
                                                           read_type,
                                                           cb,
                                                           cb_type))

    def i2c_write_request(self, address, args):
        """
        Write data to an i2c device.

        :param address: i2c device address
        :param args: A variable number of bytes to be sent to the device
                     passed in as a list.
        :returns: No return value
        """
        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.core.i2c_write_request(address, args))

    def play_tone(self, pin, tone_command, frequency, duration=None):
        """
        This method will call the Tone library for the selected pin.
        It requires FirmataPlus to be loaded onto the arduino
        If the tone command is set to TONE_TONE, then the specified tone
           will be played.
        Else, if the tone command is TONE_NO_TONE, then any currently
           playing tone will be disabled.
        It is intended for a future release of Arduino Firmata

        :param pin: Pin number
        :param tone_command: Either TONE_TONE, or TONE_NO_TONE
        :param frequency: Frequency of tone
        :param duration: Duration of tone in milliseconds
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.play_tone(pin, tone_command,
                                                    frequency, duration))

    def send_reset(self):
        """
        Send a Firmata reset command

        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.send_reset())

    def servo_config(self, pin, min_pulse=544, max_pulse=2400):
        """
        This method configures the Arduino for servo operation.

        :param pin: Servo control pin
        :param min_pulse: Minimum pulse width
        :param max_pulse: Maximum pulse width
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.servo_config(pin, min_pulse,
                                                       max_pulse))

    def set_analog_latch(self, pin, threshold_type, threshold_value,
                         cb=None, cb_type=None):
        """
        This method "arms" an analog pin for its data to be latched and
        saved in the latching table.
        If a callback method is provided, when latching criteria is achieved,
        the callback function is called with latching data notification.

        :param pin: Analog pin number (value following an 'A' designator,
                    i.e. A5 = 5
        :param threshold_type: Constants.LATCH_GT | Constants.LATCH_LT  |
                               Constants.LATCH_GTE | Constants.LATCH_LTE
        :param threshold_value: numerical value - between 0 and 1023
        :param cb: callback method
        :param cb_type: Constants.CB_TYPE_DIRECT = direct call or
                        Constants.CB_TYPE_ASYNCIO = asyncio coroutine
        :returns: True if successful, False if parameter data is invalid
        """
        loop = asyncio.get_event_loop()

        result = loop.run_until_complete(self.core.set_analog_latch(
            pin, threshold_type, threshold_value, cb, cb_type))
        return result

    def set_digital_latch(self, pin, threshold_value, cb=None, cb_type=None):
        """
        This method "arms" a digital pin for its data to be latched and saved
        in the latching table.
        If a callback method is provided, when latching criteria is achieved,
        the callback function is called
        with latching data notification.

        :param pin: Digital pin number
        :param threshold_value: 0 or 1
        :param cb: callback function
        :param cb_type: Constants.CB_TYPE_DIRECT = direct call or
                        Constants.CB_TYPE_ASYNCIO = asyncio coroutine
        :returns: True if successful, False if parameter data is invalid
        """
        loop = asyncio.get_event_loop()

        result = loop.run_until_complete(self.core.set_digital_latch(
            pin, threshold_value, cb, cb_type))
        return result

    def set_pin_mode(self, pin_number, pin_state, callback=None, cb_type=None):
        """
        This method sets the  pin mode for the specified pin.

        :param pin_number: Arduino Pin Number
        :param pin_state: INPUT/OUTPUT/ANALOG/PWM - for SERVO use
                          servo_config()
        :param callback: Optional: A reference to a call back function to be
                         called when pin data value changes
        :param cb_type: Constants.CB_TYPE_DIRECT = direct call or
                        Constants.CB_TYPE_ASYNCIO = asyncio coroutine
        :returns: No return value
        """
        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.core.set_pin_mode(
            pin_number, pin_state, callback, cb_type))

    def set_sampling_interval(self, interval):
        """
        This method sets the sampling interval for the Firmata loop method

        :param interval: time in milliseconds
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.set_sampling_interval(interval))

    def sleep(self, time):
        """
        Perform an asyncio sleep for the time specified in seconds. T
        his method should be used in place of time.sleep()

        :param time: time in seconds
        :returns: No return value
        """
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.core.sleep(time))
        except asyncio.CancelledError:
            pass
        except RuntimeError:
            pass

    def shutdown(self):
        """
        Shutdown the application and exit

        :returns: No return value
        """
        if not self.log_out:
            print('Shutting down ...')
        try:
            loop = asyncio.get_event_loop()
            self.send_reset()
            for t in asyncio.Task.all_tasks(loop):
                t.cancel()
            loop.run_until_complete(asyncio.sleep(0.1))
            loop.close()
            # keeps pytest happy
            sys.exit(1)
        except TypeError:
            # ignore the error
            pass
        except RuntimeError:
            # ignore
            pass
        except Exception as ex:
            if self.log_out:
                logging.exception(ex)
            else:
                print(ex)

    def sonar_data_retrieve(self, trigger_pin):
        """
        Retrieve Ping (HC-SR04 type) data. The data is presented as a
        dictionary.
        The 'key' is the trigger pin specified in sonar_config() and the
        'data' is the current measured distance (in centimeters)
        for that pin. If there is no data, the value is set to None.
        This is a FirmataPlus feature.

        :returns: active_sonar_map
        """
        loop = asyncio.get_event_loop()
        sonar_data = \
            loop.run_until_complete(self.core.sonar_data_retrieve(trigger_pin))
        return sonar_data

    # noinspection PyUnusedLocal
    def sonar_config(self, trigger_pin, echo_pin, cb=None, ping_interval=50,
                     max_distance=200, cb_type=None):
        """
        Configure the pins,ping interval and maximum distance for an HC-SR04
        type device.
        Single pin configuration may be used. To do so, set both the trigger
        and echo pins to the same value.
        Up to a maximum of 6 SONAR devices is supported
        If the maximum is exceeded a message is sent to the console and the
        request is ignored.
        NOTE: data is measured in centimeters

        This is FirmataPlus feature.

        :param trigger_pin: The pin number of for the trigger (transmitter).
        :param echo_pin: The pin number for the received echo.
        :param cb: optional callback function to report sonar data changes
        :param ping_interval: Minimum interval between pings. Lowest number
                              to use is 33 ms.Max is 127
        :param max_distance: Maximum distance in cm. Max is 200.
        :param cb_type: direct call or asyncio yield from
        :returns: No return value
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.sonar_config(trigger_pin,
                                                       echo_pin, cb,
                                                       ping_interval,
                                                       max_distance, cb_type))

    def stepper_config(self, steps_per_revolution, stepper_pins):
        """
        Configure stepper motor prior to operation.
        This is a FirmataPlus feature.

        :param steps_per_revolution: number of steps per motor revolution
        :param stepper_pins: a list of control pin numbers - either 4 or 2
        :returns: No return value

        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.sonar_config(steps_per_revolution,
                                                       stepper_pins))

    def stepper_step(self, motor_speed, number_of_steps):
        """
        Move a stepper motor for the number of steps at the specified speed
        This is a FirmataPlus feature.

        :param motor_speed: 21 bits of data to set motor speed
        :param number_of_steps: 14 bits for number of steps & direction
                                positive is forward, negative is reverse
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.core.stepper_step(motor_speed,
                                                       number_of_steps))
