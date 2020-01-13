#!/usr/bin/python3

import time
import smbus
import cfilter
from struct import unpack

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

ADDRESS = 0x68
XA_OFFS_USRH = 0x6
XA_OFFS_USRL = 0x7
YA_OFFS_USRH = 0x8
YA_OFFS_USRL = 0x9
ZA_OFFS_USRH = 0xA
ZA_OFFS_USRL = 0xB
XG_OFFS_USRH = 0x13
XG_OFFS_USRL = 0x14
YG_OFFS_USRH = 0x15
YG_OFFS_USRL = 0x16
ZG_OFFS_USRH = 0x17
ZG_OFFS_USRL = 0x18
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
RA_CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48

ACCEL_RANGE = [2, 4, 8, 16]
GYRO_RANGE = [250, 500, 1000, 2000]

ACCEL_FSR_2 = 0
ACCEL_FSR_4 = 1
ACCEL_FSR_8 = 2
ACCEL_FSR_16 = 3
GYRO_FSR_250 = 0
GYRO_FSR_500 = 1
GYRO_FSR_1000 = 2
GYRO_FSR_2000 = 3


class MPU(object):
    """
    mpu6050 device
    """

    def __init__(self):

        self.bus = smbus.SMBus(0)

        self.filter = cfilter.ComplementaryFilter()

        self._setupMpu()

        self.temp = 0.0

        self.accel = [0] * 3

        self.avg = [0] * 7

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

        # calibrate is disable by default
        #self._setOffset(XA_OFFS_USRH, [0] * 6)
        #self._setOffset(XG_OFFS_USRH, [0] * 6)

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
        sensors = bytearray(14)
        sensors = self.bus.read_i2c_block_data(ADDRESS, ACCEL_XOUT_H, len(sensors))

        data = unpack('>hhhhhhh', bytes(sensors))

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

        self.temp = data[3]/340.0 + 36.25
        self.accel = data[0:3]

        return data

    def readPos(self):
        """
        app filter
        """
        self.filter.input(self._readSensorScaled())
        return [self.filter.filterPos, self.accel, self.temp]

    def _setOffset(self, addr, val):
        """
        set accel and gyro offset registers
        """

        self.bus.write_i2c_block_data(ADDRESS, addr, val)

    def _getSensorAvg(self, samples):
        """
        get average data
        """
        _sum = [0] * 7

        for i in range(samples):
            time.sleep(0.05)

            val = self._readSensor()

            for j, val in enumerate(val):
                _sum[j] += val

        return [x//samples for x in _sum]

    def calibrate(self, numSamples=500, accelDeadzone=8, gyroDeadzone=3):
        """
        numSamples: Amount of readings used to average
        accelDeadzone: Acelerometer error allowed
        gyroDeadzone: Gyro error allowed

        Current only enable gyro calibration. 
        """

        gx_off, gy_off, gz_off = [0] * 3

        while True:

            readyCount = 0

            self.avg = self._getSensorAvg(numSamples)

            LOGGER.debug(self.avg)

            # test
            LOGGER.debug(self._readWord(XG_OFFS_USRH))
            LOGGER.debug(self._readWord(YG_OFFS_USRH))
            LOGGER.debug(self._readWord(ZG_OFFS_USRH))

			# gyro_xyz
            if abs(self.avg[4]) <= gyroDeadzone:
                readyCount += 1
            else:
                gx_off = gx_off - self.avg[4]//gyroDeadzone

            if abs(self.avg[5]) <= gyroDeadzone:
                readyCount += 1
            else:
                gy_off = gy_off - self.avg[5]//gyroDeadzone

            if abs( self.avg[6]) <= gyroDeadzone:
                readyCount += 1
            else:
                gz_off = gz_off - self.avg[6]//gyroDeadzone
            
            LOGGER.debug("gx_off: %s, gy_off: %s, gz_off: %s," % (gx_off, gy_off, gz_off))
            if readyCount == 3:
                break

            # set gyro offset
            data = []
            for val in (gx_off, gy_off, gz_off):
                data.append((val >> 8) & 0xff)
                data.append(val & 0xff)

            LOGGER.debug("gyro offset: %s" % data)
            self._setOffset(XG_OFFS_USRH, data)
