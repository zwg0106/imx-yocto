#!/usr/bin/python3

import time
import smbus

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

from ebf_show_cmd import EbfShowCmd

ADDRESS = 0x68

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48


class EbfShowMpu6050Cmd(EbfShowCmd):
    args = None

    def __init__(self, args):
        self.args = args
        self.bus = smbus.SMBus(0)

    def execute(self):
        """
        Get mpu6050 Parameter
        """

        LOGGER.debug(self.args)

        # config
        self._writeByte(PWR_MGMT_1, 0x0)
        self._writeByte(SMPLRT_DIV, 0x7)
        self._writeByte(CONFIG, 0x6)
        self._writeByte(ACCEL_CONFIG, 0x1)

        time.sleep(0.1)
        
        # get data
        print("ACCE_X: %6d" % self._readWord(ACCEL_XOUT_H))
        print("ACCE_Y: %6d" % self._readWord(ACCEL_YOUT_H))
        print("ACCE_Z: %6d" % self._readWord(ACCEL_ZOUT_H))
        print("GYRO_X: %6d" % self._readWord(GYRO_XOUT_H))
        print("GYRO_Y: %6d" % self._readWord(GYRO_YOUT_H))
        print("GYRO_Z: %6d" % self._readWord(GYRO_ZOUT_H))


    def _readByte(self, addr):
        """
        read one byte from device
        """
        return self.bus.read_byte_data(ADDRESS, addr)

    
    def _writeByte(self, addr, val):
        """
        write one byte data to device
        """
        return self.bus.write_byte_data(ADDRESS, addr, val)

    def _readWord(self, addr):
        """
        read one word from device
        """
        high = self.bus.read_byte_data(ADDRESS, addr)
        low = self.bus.read_byte_data(ADDRESS, addr + 1)
        val = (high << 8) + low
        return self._hex2signed(val)

    def _hex2signed(self, val):
        """
        convert 16bit hex to signed number
        """
        return -(val & 0x8000) | (val & 0x7fff)
