#!/usr/bin/python3

import os
from mpu_server import MpuServer 

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

from ebf_config_cmd import EbfConfigCmd

class EbfConfigMpu6050Cmd(EbfConfigCmd):

    def __init__(self, args):
        self.args = args
        
    def execute(self):
        """
        Get input args
        """
        
        LOGGER.debug(self.args)
        if self.args["--Enable"]:
            status = "enable"
        elif self.args["--Disable"]:
            status = "disable"
        else:
            LOGGER.debug("Unkonwn mpu args")
            return

        if status:
            MpuServer.writePipe(status)
        else:
            LOGGER.error("Incorrect mpu args")

