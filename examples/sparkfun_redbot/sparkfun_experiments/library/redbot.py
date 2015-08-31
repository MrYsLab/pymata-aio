#!/usr/bin/python
"""
  This class is a port from the https://github.com/sparkfun/RedBot Arduino library into Pymata-aio
  It is NOT a complete port. It just shows some of the main basic features.  Feel free to port more.
"""
import asyncio
from pymata_aio.constants import Constants
from pymata_aio.pymata_core import PymataCore


# RedBot motor pins from RedBot.h
L_CTRL_1 = 2
L_CTRL_2 = 4
PWM_L = 5

R_CTRL_1 = 7
R_CTRL_2 = 8
PWM_R = 6

ENCODER_PIN_LEFT = 16
ENCODER_PIN_RIGHT = 10


class RedBotEncoder:
    def __init__(self, board=None):

        self.board = board

        self.left_encoder_count = 0
        self.right_encoder_count = 0

        if self.board != None:
            # board.set_pin_mode(ENCODER_PIN_LEFT, Constants.INPUT)
            # board.sleep(0.1)
            # board.set_pin_mode(ENCODER_PIN_RIGHT, Constants.INPUT)
            # board.sleep(0.1)
            board.encoder_config(ENCODER_PIN_LEFT, ENCODER_PIN_RIGHT, self.encoder_callback,
                                 Constants.CB_TYPE_DIRECT, True)

    def encoder_callback(self, data):
        self.left_encoder_count += data[0]
        self.right_encoder_count += data[1]

    def clear_enc(self, flag=None):

        if flag == None:
            self.left_encoder_count = 0
            self.right_encoder_count = 0
        elif flag == ENCODER_PIN_RIGHT:
            self.right_encoder_count = 0
        elif flag == ENCODER_PIN_LEFT:
            self.left_encoder_count = 0

    def get_ticks(self, encoder):
        if encoder == ENCODER_PIN_LEFT:
            return self.left_encoder_count
        elif encoder == ENCODER_PIN_RIGHT:
            return self.right_encoder_count


encoderObject = RedBotEncoder()


class RedBotMotors:
    """Controls the motors on the RedBot"""

    def __init__(self, board):
        """Constructor for pin setup"""

        self.board = board
        self.total_left_ticks = 0
        self.total_right_ticks = 0
        # The interface to the motor driver is kind of ugly. It's three pins per
        # channel: two that define role (forward, reverse, stop, brake) and one
        # PWM input for speed.
        board.set_pin_mode(L_CTRL_1, Constants.OUTPUT)
        board.set_pin_mode(L_CTRL_2, Constants.OUTPUT)
        board.set_pin_mode(PWM_L, Constants.PWM)  # Not done in RedBot motors but I just went ahead and added it.
        board.set_pin_mode(R_CTRL_1, Constants.OUTPUT)
        board.set_pin_mode(R_CTRL_2, Constants.OUTPUT)
        board.set_pin_mode(PWM_R, Constants.PWM)  # Not done in RedBot motors but I just went ahead and added it.

    def brake(self):
        """effectively shorts the two leads of the motor together, which causes the motor to resist being turned. It stops quite quickly."""
        self.left_brake()
        self.right_brake()

    def drive(self, speed, durationS=-1.0):
        """
            Starts both motors. It figures out whether the motors should go
            forward or revers, then calls the appropriate individual functions. Note
            the use of a 16-bit integer for the speed input an 8-bit integer doesn't
            have the range to reach full speed. The calls to the actual drive functions
            are only 8-bit, since we only have 8-bit PWM.
        """
        if speed > 0:
            self.left_fwd(min(abs(speed), 255))
            self.right_fwd(min(abs(speed), 255))
        else:
            self.left_rev(min(abs(speed), 255))
            self.right_rev(min(abs(speed), 255))
        if durationS > 0:
            self.board.sleep(durationS)
            self.left_stop()
            self.right_stop()

    def left_motor(self, speed, durationS=-1.0):
        """Basically the same as drive(), but omitting the right motor."""
        if speed > 0:
            self.left_rev(min(abs(speed), 255))
        else:
            self.left_fwd(min(abs(speed), 255))
        if durationS > 0:
            self.board.sleep(durationS)
            self.left_stop()

    def right_motor(self, speed, durationS=-1.0):
        """Basically the same as drive(), but omitting the left motor."""
        if speed > 0:
            self.right_fwd(min(abs(speed), 255))
        else:
            self.right_rev(min(abs(speed), 255))
        if durationS > 0:
            self.board.sleep(durationS)
            self.left_stop()

    def stop(self):
        """
            stop() allows the motors to coast to a stop, rather than trying to stop them
            quickly. As will be the case with functions affecting both motors, the
            global stop just calls the individual stop functions for each wheel.
        """
        self.left_stop()
        self.right_stop()

    def left_brake(self):
        """allows left motor to coast to a stop"""
        self.board.digital_write(L_CTRL_1, 1)
        self.board.digital_write(L_CTRL_2, 1)
        self.board.analog_write(PWM_L, 0)

    def right_brake(self):
        """allows left motor to coast to a stop"""
        self.board.digital_write(R_CTRL_1, 1)
        self.board.digital_write(R_CTRL_2, 1)
        self.board.analog_write(PWM_R, 0)

    def left_stop(self):
        """allows left motor to coast to a stop"""
        self.board.digital_write(L_CTRL_1, 0)
        self.board.digital_write(L_CTRL_2, 0)
        self.board.analog_write(PWM_L, 0)

    def right_stop(self):
        """allows left motor to coast to a stop"""
        self.board.digital_write(R_CTRL_1, 0)
        self.board.digital_write(R_CTRL_2, 0)
        self.board.analog_write(PWM_R, 0)

    def pivot(self, speed, durationS=-1.0):
        """
            pivot() controls the pivot speed of the RedBot. The values of the pivot function inputs
            range from -255:255, with -255 indicating a full speed counter-clockwise rotation.
            255 indicates a full speed clockwise rotation
        """
        if speed < 0:
            self.left_fwd(min(abs(speed), 255))
            self.right_rev(min(abs(speed), 255))
        else:
            self.left_rev(min(abs(speed), 255))
            self.right_fwd(min(abs(speed), 255))
        if durationS > 0:
            self.board.sleep(durationS)
            self.left_stop()
            self.right_stop()

    # ******************************************************************************
    #  Private functions for RedBotMotor
    # ******************************************************************************/
    # These are the motor-driver level abstractions for turning a given motor the
    #  right direction. Users never see them, and *should* never see them, so we
    #  make them private.

    def left_fwd(self, spd):
        self.board.digital_write(L_CTRL_1, 1)
        self.board.digital_write(L_CTRL_2, 0)
        self.board.analog_write(PWM_L, spd)
        # If we have an encoder in the system, we want to make sure that it counts
        # in the right direction when ticks occur.
        if encoderObject:
            encoderObject.lDir = 1

    def left_rev(self, spd):
        self.board.digital_write(L_CTRL_1, 0)
        self.board.digital_write(L_CTRL_2, 1)
        self.board.analog_write(PWM_L, spd)
        # If we have an encoder in the system, we want to make sure that it counts
        # in the right direction when ticks occur.
        if encoderObject:
            encoderObject.lDir = -1

    def right_fwd(self, spd):
        self.board.digital_write(R_CTRL_1, 1)
        self.board.digital_write(R_CTRL_2, 0)
        self.board.analog_write(PWM_R, spd)
        # If we have an encoder in the system, we want to make sure that it counts
        # in the right direction when ticks occur.
        if encoderObject:
            encoderObject.rDir = 1

    def right_rev(self, spd):
        self.board.digital_write(R_CTRL_1, 0)
        self.board.digital_write(R_CTRL_2, 1)
        self.board.analog_write(PWM_R, spd)
        # If we have an encoder in the system, we want to make sure that it counts
        # in the right direction when ticks occur.
        if encoderObject:
            encoderObject.rDir = -1


class RedBotSensor:
    pin_number = 0

    def __init__(self, board, pin_number):
        self.board = board
        self.pin_number = pin_number
        board.set_pin_mode(pin_number, Constants.ANALOG)

    def read(self):
        return self.board.analog_read(self.pin_number)


class RedBotBumper:
    pin_number = 0

    def __init__(self, board, pin_number):
        self.pin_number = pin_number
        self.board = board
        self.board.set_pin_mode(pin_number, Constants.INPUT)
        self.board.digital_write(pin_number, 1)  # sets pin pull-up resistor. INPUT_PULLUP is not an option with Pymata
        pass

    def read(self):
        return self.board.digital_read(self.pin_number)


class RedBotAccel:
    """
    This library is a direct port of: https://github.com/sparkfun/SparkFun_MMA8452Q_Arduino_Library/tree/V_1.1.0
    Special Note: All reads have the Constants.I2C_END_TX_MASK bit sit. Most devices do not need to do this, but it
    is required for this chip.
    """
    MMA8452Q_Register = {
        'STATUS': 0x00,
        'OUT_X_MSB': 0x01,
        'OUT_Y_MSB': 0x03,
        'OUT_Y_LSB': 0x04,
        'OUT_Z_MSB': 0x05,
        'OUT_Z_LSB': 0x06,
        'SYSMOD': 0x0B,
        'INT_SOURCE': 0x0C,
        'WHO_AM_I': 0x0D,
        'XYZ_DATA_CFG': 0x0E,
        'HP_FILTER_CUTOFF': 0x0F,
        'PL_STATUS': 0x10,
        'PL_CFG': 0x11,
        'PL_COUNT': 0x12,
        'PL_BF_ZCOMP': 0x13,
        'P_L_THS_REG': 0x14,
        'FF_MT_CFG': 0x15,
        'FF_MT_SRC': 0x16,
        'FF_MT_THS': 0x17,
        'FF_MT_COUNT': 0x18,
        'TRANSIENT_CFG': 0x1D,
        'TRANSIENT_SRC': 0x1E,
        'TRANSIENT_THS': 0x1F,
        'TRANSIENT_COUNT': 0x20,
        'PULSE_CFG': 0x21,
        'PULSE_SRC': 0x22,
        'PULSE_THSX': 0x23,
        'PULSE_THSY': 0x24,
        'PULSE_THSZ': 0x25,
        'PULSE_TMLT': 0x26,
        'PULSE_LTCY': 0x27,
        'PULSE_WIND': 0x28,
        'ASLP_COUNT': 0x29,
        'CTRL_REG1': 0x2A,
        'CTRL_REG2': 0x2B,
        'CTRL_REG3': 0x2C,
        'CTRL_REG4': 0x2D,
        'CTRL_REG5': 0x2E,
        'OFF_X': 0x2F,
        'OFF_Y': 0x30,
        'OFF_Z': 0x31
    }

    def __init__(self, board, address=0x1d, scale=2, output_data_rate=0):
        """
RedBotAccel(self.board, , 2, 0)
        @param address: Address of the device
        @param scale: scale factor
        @param output_data_rate: output data rate
        @return: no return value
        """

        # portrait landscape status values
        self.PORTRAIT_U = 0
        self.PORTRAIT_D = 1
        self.LANDSCAPE_R = 2
        self.LANDSCAPE_L = 3
        self.LOCKOUT = 0x40

        # device id
        self.device_id = 42

        # device address
        self.address = address

        # scale factor (fsr)
        self.scale = scale

        # output data rate (odr)
        self.output_data_rate = output_data_rate

        # call backs for axis, portrait/landscape and tap results
        self.axis = None
        self.p_l = None
        self.tap = None

        # When a read is performed,, data is returned through a call back to this structure.
        # It should be cleared after data is consumed
        self.callback_data = []

        # beginning of data returned is located at position 4
        # 0 is the device address
        self.data_start = 2

        self.board = board

        # reset accel
        register = self.MMA8452Q_Register['CTRL_REG2']
        self.board.i2c_write_request(self.address, [register, 0x40])
        self.start()

    @asyncio.coroutine
    def start(self):
        # configure firmata for i2c
        yield from self.board.i2c_config()

        # reset the device
        register = self.MMA8452Q_Register['CTRL_REG2']
        yield from self.board.i2c_write_request(self.address, [register, 0x40])

        # verify the device by sending a WHO AM I command and checking the results
        id_board = yield from self.check_who_am_i()
        if not id_board:
            print("Who am I fails")
            yield from self.board.shutdown()
        else:
            # Correct device, continue with init
            # Must be in standby to change registers
            yield from self.standby()

            # set up the scale register
            yield from self.set_scale(self.scale)

            # set the output data rate
            yield from self.set_output_data_rate(self.output_data_rate)

            # Set up portrait/landscape detection
            yield from self.setup_portrait_landscape()

            # Disable x, y, set z to 0.5g
            yield from self.setup_tap(0x80, 0x80, 0x08)

            # set device to active state
            # self.board.sleep(.3)
            yield from self.set_active()

    @asyncio.coroutine
    def data_val(self, data):
        """
        This is the callback method used to save read results
        @param data: Data returned from the device
        @return: No return value
        """
        self.callback_data = data

    @asyncio.coroutine
    def check_who_am_i(self):
        """
        This method checks verifies the device ID.
        @return: True if valid, False if not
        """
        register = self.MMA8452Q_Register['WHO_AM_I']

        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)
        # yield from asyncio.sleep(1)
        reply = yield from self.wait_for_read_result()
        # yield from asyncio.sleep(1)

        if reply[self.data_start] == self.device_id:
            rval = True
        else:
            rval = False
        return rval

    @asyncio.coroutine
    def standby(self):
        """
        Put the device into standby mode so that the registers can be set.
        @return: No return value
        """
        register = self.MMA8452Q_Register['CTRL_REG1']
        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        ctrl1 = yield from self.wait_for_read_result()

        ctrl1 = (ctrl1[self.data_start]) & ~0x01
        self.callback_data = []

        yield from self.board.i2c_write_request(self.address, [register, ctrl1])

    @asyncio.coroutine
    def set_scale(self, scale):
        """
        Set the device scale register.
        Device must be in standby before calling this function
        @param scale: scale factor
        @return: No return value
        """
        register = self.MMA8452Q_Register['XYZ_DATA_CFG']
        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        config_reg = yield from self.wait_for_read_result()
        config_reg = config_reg[self.data_start]
        config_reg &= 0xFC  # Mask out scale bits
        config_reg |= (scale >> 2)
        yield from self.board.i2c_write_request(self.address, [register, config_reg])

    @asyncio.coroutine
    def set_output_data_rate(self, output_data_rate):
        """
        Set the device output data rate.
        Device must be in standby before calling this function
        @param output_data_rate: Desired data rate
        @return: No return value.
        """
        # self.standby()
        register = self.MMA8452Q_Register['CTRL_REG1']
        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        control_reg = yield from self.wait_for_read_result()
        control_reg = control_reg[self.data_start]

        control_reg &= 0xC7  # Mask out data rate bits
        control_reg |= (output_data_rate << 3)
        yield from self.board.i2c_write_request(self.address, [register, control_reg])

    @asyncio.coroutine
    def setup_portrait_landscape(self):
        """
        Setup the portrait/landscape registers
        Device must be in standby before calling this function
        @return: No return value
        """
        register = self.MMA8452Q_Register['PL_CFG']

        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        control_reg = yield from self.wait_for_read_result()
        control_reg = control_reg[self.data_start] | 0x40

        #  1. Enable P/L
        yield from self.board.i2c_write_request(self.address, [register, control_reg])

        register = self.MMA8452Q_Register['PL_COUNT']

        # 2. Set the de-bounce rate
        yield from self.board.i2c_write_request(self.address, [register, 0x50])

    @asyncio.coroutine
    def read_portrait_landscape(self, callback=None):
        """
        This function reads the portrait/landscape status register of the MMA8452Q.
        It will return either PORTRAIT_U, PORTRAIT_D, LANDSCAPE_R, LANDSCAPE_L,
        or LOCKOUT. LOCKOUT indicates that the sensor is in neither p or ls.
        @return: See above.
        """
        register = self.MMA8452Q_Register['PL_STATUS']
        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        pl_status = yield from self.wait_for_read_result()
        pl_status = pl_status[self.data_start]
        if pl_status & 0x40:  # Z-tilt lockout
            pl_status = self.LOCKOUT
        else:  # Otherwise return LAPO status
            pl_status = (pl_status & 0x6) >> 1

        if callback:
            yield from callback(pl_status)
        yield from asyncio.sleep(.001)

        return pl_status

    @asyncio.coroutine
    def setup_tap(self, x_ths, y_ths, z_ths):
        """
        This method sets the tap thresholds.
        Device must be in standby before calling this function.
        Set up single and double tap - 5 steps:
        for more info check out this app note:
        http://cache.freescale.com/files/sensors/doc/app_note/AN4072.pdf
        Set the threshold - minimum required acceleration to cause a tap.
        @param x_ths: x tap threshold
        @param y_ths: y tap threshold
        @param z_ths: z tap threshold
        @return: No return value.
        """
        temp = 0

        if not (x_ths & 0x80):  # If top bit ISN'T set
            temp |= 0x3  # Enable taps on x
            register = self.MMA8452Q_Register["PULSE_THSX"]
            yield from self.board.i2c_write_request(self.address, [register, x_ths])

        if not (y_ths & 0x80):  # If top bit ISN'T set
            temp |= 0x0C  # Enable taps on y
            register = self.MMA8452Q_Register["PULSE_THSY"]
            yield from self.board.i2c_write_request(self.address, [register, y_ths])

        if not (z_ths & 0x80):  # If top bit Izx
            temp |= 0x30  # Enable taps on z
            register = self.MMA8452Q_Register["PULSE_THSZ"]
            yield from self.board.i2c_write_request(self.address, [register, z_ths])

        # self.board.sleep(2)
        # Set up single and/or double tap detection on each axis individually.
        register = self.MMA8452Q_Register['PULSE_CFG']
        yield from self.board.i2c_write_request(self.address, [register, temp | 0x40])

        #  Set the time limit - the maximum time that a tap can be above the thresh
        register = self.MMA8452Q_Register['PULSE_TMLT']
        #  30ms time limit at 800Hz odr
        yield from self.board.i2c_write_request(self.address, [register, 0x30])

        #  Set the pulse latency - the minimum required time between pulses
        register = self.MMA8452Q_Register['PULSE_LTCY']
        yield from self.board.i2c_write_request(self.address, [register, 0xA0])

        #  Set the second pulse window - maximum allowed time between end of
        #  latency and start of second pulse
        register = self.MMA8452Q_Register['PULSE_WIND']
        yield from self.board.i2c_write_request(self.address, [register, 0xFF])  # 5. 318ms (max value) between taps max

    @asyncio.coroutine
    def read_tap(self, callback=None):
        """
        This function returns any taps read by the MMA8452Q. If the function
        returns 0, no new taps were detected. Otherwise the function will return the
        lower 7 bits of the PULSE_SRC register.
        @return: 0 or lower 7 bits of the PULSE_SRC register.
        """
        # self.board.sleep(1)
        register = self.MMA8452Q_Register['PULSE_SRC']
        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        tap_status = yield from self.wait_for_read_result()
        tap_status = tap_status[self.data_start]
        if tap_status & 0x80:
            tap_status &= 0x7f
        else:
            tap_status = 0

        if callback:
            yield from callback(tap_status)
        yield from asyncio.sleep(.001)

        return tap_status

    @asyncio.coroutine
    def set_active(self):
        """
        This method sets the device to the active state
        @return: No return value.
        """
        register = self.MMA8452Q_Register['CTRL_REG1']
        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        control_reg = yield from self.wait_for_read_result()

        control_reg = control_reg[self.data_start] | 0x01

        yield from self.board.i2c_write_request(self.address, [register, control_reg])

    @asyncio.coroutine
    def available(self):
        """
        This method checks to see if new xyz data is available
        @return: Returns 0 if not available. 1 if it is available
        """
        register = self.MMA8452Q_Register['STATUS']
        yield from self.board.i2c_read_request(self.address, register, 1,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        avail = yield from self.wait_for_read_result()
        avail = (avail[self.data_start] & 0x08) >> 3

        return avail

    @asyncio.coroutine
    def read(self, callback=None):
        """
        The device returns an MSB and LSB (in that order) for each axis.
        These are 12 bit values - that is only the upper 4 bits of the LSB are used.

        To make things more confusing, firmata returns each axis as 4 bytes, and reverses the order because
        it looks at the world as lsb, msb order.
        :return: callback data is set with x,y,z raw (integers) followed by x,y,z corrected ( floating point)
        Call available() first to make sure new data is really available.
        """
        register = self.MMA8452Q_Register['OUT_X_MSB']
        yield from self.board.i2c_read_request(self.address, register, 6,
                                               Constants.I2C_READ | Constants.I2C_END_TX_MASK,
                                               self.data_val, Constants.CB_TYPE_ASYNCIO)

        # get x y z data
        xyz = yield from self.wait_for_read_result()

        # string off address and register bytes
        xyz = xyz[2:]
        xmsb = xyz[0]
        xlsb = xyz[1]
        ymsb = xyz[2]
        ylsb = xyz[3]
        zmsb = xyz[4]
        zlsb = xyz[5]

        # OR the 2 pieces together, shift 4 places to get 12 bits
        xa = (xmsb << 8 | xlsb) >> 4

        ya = (ymsb << 8 | ylsb) >> 4

        za = (zmsb << 8 | zlsb) >> 4

        cx = float(xa) / float(2048) * float(self.scale)
        cy = float(ya) / float(2048) * float(self.scale)
        cz = float(za) / float(2048) * float(self.scale)

        if callback:
            yield from callback([xa, ya, za, cx, cy, cz])
        yield from asyncio.sleep(.001)

        return [xa, ya, za, cx, cy, cz]

    @asyncio.coroutine
    def wait_for_read_result(self):
        """
        This is a utility function to wait for return data call back
        @return: Returns resultant data from callback
        """
        while not self.callback_data:
            yield from asyncio.sleep(.001)
        rval = self.callback_data
        self.callback_data = []
        return rval


if __name__ == "__main__":
    my_board = PymataCore(2)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(my_board.start_aio())
    accel = RedBotAccel(my_board, 0x1d, 2, 0)
    loop.run_until_complete(accel.start())
    while True:
        availb = loop.run_until_complete(accel.available())
        if availb:
            axis = loop.run_until_complete(accel.read())

            x = axis[3]
            y = axis[4]
            z = axis[5]

            tap = loop.run_until_complete(accel.read_tap())
            if tap:
                tap = 'TAPPED'
            else:
                tap = 'NO TAP'
            port_land = loop.run_until_complete(accel.read_portrait_landscape())
            if port_land == accel.LOCKOUT:
                port_land = 'Flat   '
            elif port_land == 0:
                port_land = 'Tilt Lf'
            elif port_land == 1:
                port_land = 'Tilt Rt'
            elif port_land == 2:
                port_land = 'Tilt Up'
            else:
                port_land = 'Tilt Dn'
            print('{0:.2f}   {1:.2f}   {2:.2f}   {3}   {4}'.format(x, y, z, port_land, tap))
    loop.run_forever()
