#!/usr/bin/python3

import os
import socket
import time
import json
from threading import Thread
from select import select
from mpu6050 import MPU

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

#default udp port
#DEFAULT_IP_PORT = ("192.168.37.83", 5000)
DEFAULT_IP_PORT = ("10.245.105.204", 7000)

ITEM = ["filter", "accel", "gyro"]

def toJson(val):
    """
    convert list to json
    """
    msg = json.dumps(dict(zip(ITEM, val))) 

    return msg 

class MpuServer(object):
    pollPipe = os.pipe()

    def __init__(self, port=DEFAULT_IP_PORT):
        self.port = port
        self._initSocket()
        self.inputFd = [self.pollPipe[0]]

        self.mpu = MPU()
        LOGGER.debug("Init Mpu Server")

    def threadStart(self):

        Thread(target=self._handleInputData, daemon=True).start()

    def _initSocket(self):
        """
        setup UDP socket
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _handleInputData(self):
        """
        handle pipe data
        send mpu data if enabled by CLI
        """
        timeout = None

        while True:
            rd, _, _ = select(self.inputFd, [], [], timeout)
            # handle pipe
            if self.pollPipe[0] in rd:
				# read data from Pipe
                # 2 cases:
                #   1) "enable"
                #   2) "disable"
                tmp = os.read(self.pollPipe[0], 20).decode()
                if tmp == "enable" and timeout is None:
                    timeout = 0.01
                elif tmp == "disable":
                    timeout = None 
                else:
                    LOGGER.error("Unknown pipe data")

            # waked up by timeout
            # send mpu data 
            if timeout is not None:
                val = self.mpu.readPos()
                LOGGER.debug(toJson(val))
                self.sock.sendto(toJson(val).encode("utf-8"), DEFAULT_IP_PORT)


    @classmethod
    def writePipe(cls, data):
	
        LOGGER.debug("Write [%s] to pipe %d" % (data, cls.pollPipe[1]))
        os.write(cls.pollPipe[1], bytes(data, encoding='utf-8'))

    def threadStop(self):
		
        pass
