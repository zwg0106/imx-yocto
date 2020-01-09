#!/usr/bin/python3

import time
import smbus
import cfilter
from struct import unpack

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

ADDRESS = 0x68

PWR_MGMT_1      = 0x6B
SMPLRT_DIV      = 0x19
RA_CONFIG       = 0x1A
GYRO_CONFIG     = 0x1B
ACCEL_CONFIG    = 0x1C
ACCEL_XOUT_H    = 0x3B
ACCEL_XOUT_L    = 0x3C
ACCEL_YOUT_H    = 0x3D
ACCEL_YOUT_L    = 0x3E
ACCEL_ZOUT_H    = 0x3F
ACCEL_ZOUT_L    = 0x40
TEMP_OUT_H      = 0x41
TEMP_OUT_L      = 0x42
GYRO_XOUT_H     = 0x43
GYRO_XOUT_L     = 0x44
GYRO_YOUT_H     = 0x45
GYRO_YOUT_L     = 0x46
GYRO_ZOUT_H     = 0x47
GYRO_ZOUT_L     = 0x48

ACCEL_RANGE = [2, 4, 8, 16]
GYRO_RANGE = [250, 500, 1000, 2000]

ACCEL_FSR_2     = 0
ACCEL_FSR_4     = 1
ACCEL_FSR_8     = 2
ACCEL_FSR_16    = 3
GYRO_FSR_250    = 0
GYRO_FSR_500    = 1
GYRO_FSR_1000   = 2
GYRO_FSR_2000   = 3


class MPU(object):
    """
    mpu6050 device
    """
    def __init__(self):
        self.sensors = bytearray(14)
        
        self.avgGyroOff = [0] * 3

        self.bus = smbus.SMBus(0)

        self.filter = cfilter.ComplementaryFilter()

        self._setupMpu()

    def _setupMpu(self):
        """
        setup device
        """
        LOGGER.debug("Setup Mpu6050 device")

        # disable sleep mode
        self._writeByte(PWR_MGMT_1, 0x0)

        # set sample rate
        self._writeByte(SMPLRT_DIV, 0x7)

        # enable dlpf
        self._writeByte(RA_CONFIG, 0x1)

        # set accel & gyro range
        self._writeByte(ACCEL_CONFIG, ACCEL_FSR_2)
        self._writeByte(GYRO_CONFIG, GYRO_FSR_250)

        self.accelRange = ACCEL_RANGE[ACCEL_FSR_2]
        self.gyroRange = GYRO_RANGE[GYRO_FSR_250]

        #self._calibrate()

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

    def _readSensor(self):
        """
        read bytes from 0x3B to 0x48
        """
        self.sensors = self.bus.read_i2c_block_data(ADDRESS, ACCEL_XOUT_H, len(self.sensors))

        data = unpack('>hhhhhhh', bytes(self.sensors))

        return list(data)
        
    def _readSensorScaled(self):
        """
        apply divider to accel and gyro
        accel: data[0->2]
        temp: data[3]
        gyro: data[4->6]
        """
        data = self._readSensor()
        data[0:3] = [x/(65536//self.accelRange//2) for x in data[0:3]]
        data[4:7] = [x/(65536//self.gyroRange//2) for x in data[4:7]]
        
        # app offset for gyro
        #data[4:7] = [(x - y)/(65536//self.gyroRange//2) for x,y in zip(data[4:7], self.avgGyroOff)]
       
        data[3] = data[3]/340.0 + 36.25
        return data

    def readPos(self):
        """
        app filter
        """
        self.filter.input(self._readSensorScaled())
        return [self.filter.filterPos, self.filter.accelPos, self.filter.gyroPos]

    def _calibrate(self, numSamples=500):
        """
        get gyro offset
        """
        _sum = [0] * 7

        for i in range(numSamples):
            time.sleep(0.01)

            val = self._readSensor()

            for i, val in enumerate(val):
                _sum[i] += val

        avg = [x//numSamples for x in _sum]
        LOGGER.debug("Avg is %s", avg)

        self.avgGyroOff = avg[4:]

        LOGGER.debug("Calibrate complete...")
