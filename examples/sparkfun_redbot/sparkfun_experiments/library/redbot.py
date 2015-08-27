#!/usr/bin/python
"""
  This class is a port from the https://github.com/sparkfun/RedBot Arduino library into Pymata-aio
  It is NOT a complete port. It just shows some of the main basic features.  Feel free to port more.
"""

from pymata_aio.constants import Constants

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


    # TODO: Implement
    pass


encoderObject = RedBotEncoder()


class RedBotMotors:
    """Controls the motors on the RedBot"""

    def __init__(self, board):
        global left_encoder_count
        global right_encoder_count
        left_encoder_count = 0
        right_encoder_count = 0


        """Constructor for pin setup"""
        self.board = board
        # The interface to the motor driver is kind of ugly. It's three pins per
        # channel: two that define role (forward, reverse, stop, brake) and one
        # PWM input for speed.
        board.set_pin_mode(L_CTRL_1, Constants.OUTPUT)
        board.set_pin_mode(L_CTRL_2, Constants.OUTPUT)
        board.set_pin_mode(PWM_L, Constants.PWM)  # Not done in RedBot motors but I just went ahead and added it.
        board.set_pin_mode(R_CTRL_1, Constants.OUTPUT)
        board.set_pin_mode(R_CTRL_2, Constants.OUTPUT)
        board.set_pin_mode(PWM_R, Constants.PWM)  # Not done in RedBot motors but I just went ahead and added it.


        board.set_pin_mode(ENCODER_PIN_LEFT, Constants.INPUT, self.encoderCallback)
        board.set_pin_mode(ENCODER_PIN_RIGHT, Constants.INPUT, self.encoderCallback)

        #TODO: Work out how to make this a single call
        board.encoder_config(ENCODER_PIN_LEFT, ENCODER_PIN_RIGHT, self.encoderCallback)
        board.encoder_config(ENCODER_PIN_RIGHT, ENCODER_PIN_RIGHT, self.encoderCallback)



    def brake(self):
        """effectively shorts the two leads of the motor together, which causes the motor to resist being turned. It stops quite quickly."""
        self.leftBrake()
        self.rightBrake()


    def drive(self, speed, durationS=-1.0):
        """
            Starts both motors. It figures out whether the motors should go
            forward or revers, then calls the appropriate individual functions. Note
            the use of a 16-bit integer for the speed input; an 8-bit integer doesn't
            have the range to reach full speed. The calls to the actual drive functions
            are only 8-bit, since we only have 8-bit PWM.
        """
        if speed > 0:
            self.leftFwd(min(abs(speed), 255))
            self.rightFwd(min(abs(speed), 255))
        else:
            self.leftRev(min(abs(speed), 255))
            self.rightRev(min(abs(speed), 255))
        if durationS > 0:
            self.board.sleep(durationS)
            self.leftStop()
            self.rightStop()


    def leftMotor(self, speed, durationS=-1.0):
        """Basically the same as drive(), but omitting the right motor."""
        if speed > 0:
            self.leftRev(min(abs(speed), 255))
        else:
            self.leftFwd(min(abs(speed), 255))
        if durationS > 0:
            self.board.sleep(durationS)
            self.leftStop()


    def rightMotor(self, speed, durationS=-1.0):
        """Basically the same as drive(), but omitting the left motor."""
        if speed > 0:
            self.rightFwd(min(abs(speed), 255))
        else:
            self.rightRev(min(abs(speed), 255))
        if durationS > 0:
            self.board.sleep(durationS)
            self.leftStop()


    def stop(self):
        """
            stop() allows the motors to coast to a stop, rather than trying to stop them
            quickly. As will be the case with functions affecting both motors, the
            global stop just calls the individual stop functions for each wheel.
        """
        self.leftStop()
        self.rightStop()


    def leftBrake(self):
        """allows left motor to coast to a stop"""
        self.board.digital_write(L_CTRL_1, 1)
        self.board.digital_write(L_CTRL_2, 1)
        self.board.analog_write(PWM_L, 0)


    def rightBrake(self):
        """allows left motor to coast to a stop"""
        self.board.digital_write(R_CTRL_1, 1)
        self.board.digital_write(R_CTRL_2, 1)
        self.board.analog_write(PWM_R, 0)


    def leftStop(self):
        """allows left motor to coast to a stop"""
        self.board.digital_write(L_CTRL_1, 0)
        self.board.digital_write(L_CTRL_2, 0)
        self.board.analog_write(PWM_L, 0)


    def rightStop(self):
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
            self.leftFwd(min(abs(speed), 255))
            self.rightRev(min(abs(speed), 255))
        else:
            self.leftRev(min(abs(speed), 255))
            self.rightFwd(min(abs(speed), 255))
        if durationS > 0:
            self.board.sleep(durationS)
            self.leftStop()
            self.rightStop()


    # ******************************************************************************
    #  Private functions for RedBotMotor
    # ******************************************************************************/
    # These are the motor-driver level abstractions for turning a given motor the
    #  right direction. Users never see them, and *should* never see them, so we
    #  make them private.

    def leftFwd(self, spd):
        self.board.digital_write(L_CTRL_1, 1)
        self.board.digital_write(L_CTRL_2, 0)
        self.board.analog_write(PWM_L, spd)
        # If we have an encoder in the system, we want to make sure that it counts
        # in the right direction when ticks occur.
        if encoderObject:
            encoderObject.lDir = 1


    def leftRev(self, spd):
        self.board.digital_write(L_CTRL_1, 0)
        self.board.digital_write(L_CTRL_2, 1)
        self.board.analog_write(PWM_L, spd)
        # If we have an encoder in the system, we want to make sure that it counts
        # in the right direction when ticks occur.
        if encoderObject:
            encoderObject.lDir = -1


    def rightFwd(self, spd):
        self.board.digital_write(R_CTRL_1, 1)
        self.board.digital_write(R_CTRL_2, 0)
        self.board.analog_write(PWM_R, spd)
        # If we have an encoder in the system, we want to make sure that it counts
        # in the right direction when ticks occur.
        if encoderObject:
            encoderObject.rDir = 1


    def rightRev(self, spd):
        self.board.digital_write(R_CTRL_1, 0)
        self.board.digital_write(R_CTRL_2, 1)
        self.board.analog_write(PWM_R, spd)
        # If we have an encoder in the system, we want to make sure that it counts
        # in the right direction when ticks occur.
        if encoderObject:
            encoderObject.rDir = -1


# Configure



#TODO: Work out how to use encoder_callback correctly, the individual left and right callbacks are unneccessary

# def encoder_callback(event=None):
#     global left_encoder_count
#     global right_encoder_count
#     left_encoder_count+=1
#     right_encoder_count+=1
#     print("Left: {} , Right: {}".format(left_encoder_count,right_encoder_count))

    def encoderCallback(self, data=None):
        global left_encoder_count
        global right_encoder_count
        if type(data) == list:  #Ugly workaround to stop it throwing up errors, as the data var changes from list to
        # int seemingly randomly
            if data[0] == ENCODER_PIN_LEFT: # data[0] is the pin id, data[1] is the encoder_read value (0 or 1).
                left_encoder_count += 1
            elif data[0] == ENCODER_PIN_RIGHT:
                right_encoder_count +=1

        # print("Left: {} , Right: {}".format(left_encoder_count,right_encoder_count))
        # print(type(data))

    def rightEncoderCallback(self, data=None):
        global right_encoder_count
        right_encoder_count += 1
        print("Left: {} , Right: {}".format(data,data))

    def clearEnc(self, flag=None):
        global left_encoder_count
        global right_encoder_count
        if flag == None:
            left_encoder_count = 0
            right_encoder_count = 0
        elif flag == ENCODER_PIN_RIGHT:
            right_encoder_count = 0
        elif flag == ENCODER_PIN_LEFT:
            left_encoder_count = 0


    def getTicks(self, encoder):
        if encoder == ENCODER_PIN_LEFT:
            return left_encoder_count
        elif encoder == ENCODER_PIN_RIGHT:
            return right_encoder_count
