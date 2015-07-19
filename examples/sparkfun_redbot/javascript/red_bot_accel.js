__author__ = 'afy'

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants


class RedBotAccel:
    """
    This library is directly derived from https://github.com/sparkfun/MMA8452_Accelerometer
    """

    def __init__(self, address, scale, output_data_rate):
        self.MMA8452Q_Register = {
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

        self.address = address
        self.scale = scale
        self.output_data_rate = output_data_rate
        self.callback_data = []
        self.board = PyMata3()
        self.board.i2c_config()
        if not self.check_who_am_i():
            print("Who am I fails")
            self.board.shutdown()
        else:
            print("Who Am I passes")

            # Correct device, continue with init
            # Must be in standby to change registers
            self.standby()

            # set up the scale register
            self.set_scale(self.scale)

            # set the output data rate
            self.set_output_data_rate(self.output_data_rate)

            # Set up portrait/landscape detection
            self.setup_potrait_landscape()

            #  Disable x, y, set z to 0.5g
            self.setup_tap(0x80, 0x80, 0x08)

            self.set_active()

    def data_val(self, data):
        self.callback_data = data

    def check_who_am_i(self):
        register = self.MMA8452Q_Register['WHO_AM_I']

        self.board.i2c_read_request(self.address, register, 1, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        if self.callback_data[4] == 42:
            rval = True
        else:
            rval = False

        self.callback_data = []
        return rval

    def standby(self):
        register = self.MMA8452Q_Register['CTRL_REG1']
        self.board.i2c_read_request(self.address, register, 1, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        # print(self.callback_data)
        ctrl1 = (self.callback_data[4]) & ~0x01
        self.callback_data = []

        self.board.i2c_write_request(self.address, register, ctrl1)

    def set_scale(self, scale):
        # call standby before calling this function
        register = self.MMA8452Q_Register['XYZ_DATA_CFG']
        self.board.i2c_read_request(self.address, register, 1, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        config_reg = self.callback_data[4]
        self.callback_data = []
        config_reg &= 0xFC  # Mask out scale bits
        config_reg |= (scale >> 2)
        self.board.i2c_write_request(self.address, register, config_reg)

    def set_output_data_rate(self, output_data_rate):
        register = self.MMA8452Q_Register['CTRL_REG1']
        self.board.i2c_read_request(self.address, register, 1, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        control_reg = self.callback_data[4]
        self.callback_data = []

        control_reg &= 0xCF  # Mask out data rate bits
        control_reg |= (output_data_rate << 3)
        self.board.i2c_write_request(self.address, register, control_reg)

    def setup_potrait_landscape(self):
        register = self.MMA8452Q_Register['PL_CFG']

        self.board.i2c_read_request(self.address, register, 1, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        control_reg = self.callback_data[4] | 0x40
        self.callback_data = []

        #  1. Enable P/L
        self.board.i2c_write_request(self.address, register, control_reg)

        register = self.MMA8452Q_Register['PL_COUNT']

        # 2. Set the debounce rate
        self.board.i2c_write_request(self.address, register, 0x50)

    def setup_tap(self, x_ths, y_ths, z_ths):
        # Set up single and double tap - 5 steps:
        # for more info check out this app note:
        # http://cache.freescale.com/files/sensors/doc/app_note/AN4072.pdf
        # Set the threshold - minimum required acceleration to cause a tap.

        temp = 0
        if not (x_ths & 0x80):  # If top bit ISN'T set
            temp |= 0x3  # Enable taps on x
            register = self.MMA8452Q_Register["PULSE_THSX"]
            self.board.i2c_write_request(self.address, register, x_ths)

        if not (y_ths & 0x80):  # If top bit ISN'T set
            temp |= 0x0C  # Enable taps on y
            register = self.MMA8452Q_Register["PULSE_THSY"]
            self.board.i2c_write_request(self.address, register, y_ths)

        if not (z_ths & 0x80):  # If top bit Izx
            register = self.MMA8452Q_Register["PULSE_THSZ"]
            self.board.i2c_write_request(self.address, register, z_ths)

            # Set up single and/or double tap detection on each axis individually.
            register = self.MMA8452Q_Register['PULSE_CFG']
            self.board.i2c_write_request(self.address, register, temp | 0x40)

            #  Set the time limit - the maximum time that a tap can be above the thresh
            register = self.MMA8452Q_Register['PULSE_TMLT']
            #  30ms time limit at 800Hz odr
            self.board.i2c_write_request(self.address, register, 0x30)

            #  Set the pulse latency - the minimum required time between pulses
            register = self.MMA8452Q_Register['PULSE_LTCY']
            self.board.i2c_write_request(self.address, register, 0xA0)

            #  Set the second pulse window - maximum allowed time between end of
            #  latency and start of second pulse
            register = self.MMA8452Q_Register['PULSE_WIND']
            self.board.i2c_write_request(self.address, register, 0xFF)  # 5. 318ms (max value) between taps max

    def set_active(self):
        register = self.MMA8452Q_Register['CTRL_REG1']
        self.board.i2c_read_request(self.address, register, 1, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        control_reg = self.callback_data[4] | 0x01
        self.callback_data = []
        self.board.i2c_write_request(self.address, register, control_reg)

    def available(self):
        register = self.MMA8452Q_Register['STATUS']
        self.board.i2c_read_request(self.address, register, 1, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        rval = (self.callback_data[4] & 0x08) >> 3
        self.callback_data = []

        # print("avail returns " + str(rval))
        return rval

    def read(self):
        """
        The device returns an MSB and LSB (in that order) for each axis.
        These are 12 bit values - that is only the upper 4 bits of the LSB are used.

        To make things more confusing, firmata returns each axis as 4 bytes, and reverses the order because
        it looks at the world as lsb, msb order.
        :return: callback data is set with x,y,z raw (integers) followed by x,y,z corrected ( floating point)
        """
        register = self.MMA8452Q_Register['OUT_X_MSB']
        self.board.i2c_read_request(self.address, register, 6, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        # value = (data[PrivateConstants.MSB] << 7) + data[PrivateConstants.LSB]
        xmsb = self.callback_data[4] & 0x7f
        xmsb += (self.callback_data[5] & 0x7f) << 7

        xlsb = self.callback_data[6] & 0x7f
        xlsb += (self.callback_data[7] & 0x7f) << 7

        # OR the 2 pieces together, shift 4 places to get 12 bits
        x = (xmsb << 8 | xlsb) >> 4

        ymsb = self.callback_data[8] & 0x7f
        ymsb += (self.callback_data[9] & 0x7f) << 7

        ylsb = self.callback_data[10] & 0x7f
        ylsb += (self.callback_data[11] & 0x7f) << 7

        y = (ymsb << 8 | ylsb) >> 4

        zmsb = self.callback_data[12] & 0x7f
        zmsb += (self.callback_data[13] & 0x7f) << 7

        zlsb = self.callback_data[14] & 0x7f
        zlsb += (self.callback_data[15] & 0x7f) << 7

        z = (zmsb << 8 | ylsb) >> 4

        cx = float(x) / float(2048) * float(self.scale)
        cy = float(y) / float(2048) * float(self.scale)
        cz = float(z) / float(2048) * float(self.scale)


        # x = self.callback_data[5] + (self.callback_data[4] << 7)
        # y = self.callback_data[7] + (self.callback_data[6] << 7)
        # z = self.callback_data[9] + (self.callback_data[6] << 7)

        # cx = (float) x / (float)(1<<11) * (float)(scale);
        # cy = (float) y / (float)(1<<11) * (float)(scale);
        # cz = (float) z / (float)(1<<11) * (float)(scale);

        self.callback_data = []
        return [x, y, z, cx, cy, cz]

    def is_active(self):
        register = self.MMA8452Q_Register['CTRL_REG1']
        self.board.i2c_read_request(self.address, register, 1, Constants.I2C_READ, self.data_val)
        while not self.callback_data:
            self.board.sleep(.01)

        # print( 'is active: ' + str(self.callback_data))
        # tbd assemble the data
        self.callback_data = []



accel = RedBotAccel(0x1d, 2, 0)
accel.check_who_am_i()
while True:
    # if accel.available():
    ab = accel.available()
    print(ab)
    #if v != 0:
    v = accel.read()
    print(v)
    #accel.is_active()
    accel.board.sleep(.1)

    # accel.board.sleep(1)
    # exit()
    # else:
    # accel.board.sleep(.001)
