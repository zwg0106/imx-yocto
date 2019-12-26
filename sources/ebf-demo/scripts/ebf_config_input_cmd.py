#!/usr/bin/python3

import os
from threadPoll import ThreadPollDevice

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

from ebf_config_cmd import EbfConfigCmd

class EbfConfigInputCmd(EbfConfigCmd):

    def __init__(self, args):
        self.args = args
        
    def execute(self):
        """
        Get input args
        """
        
        LOGGER.debug(self.args)
        if self.args["--All"]:
            if self.args["--Enable"]:
                # add all devices
                dev = "all"
            elif self.args["--Disable"]:
                # remove all devices
                dev = "none"
            
        elif self.args["--Key"]:
            if self.args["--Enable"]:
                dev = "key:enable" 
            elif self.args["--Disable"]:
                dev = "key:disable"

        elif self.args["--OnOff"]:
            if self.args["--Enable"]:
                dev = "onoff:enable"
            elif self.args["--Disable"]:
                dev = "onoff:disable"

        else:
            LOGGER.debug("Unkonwn input args")
            return
       
        LOGGER.debug("Update devices: %s", dev)
        if dev:
            ThreadPollDevice.writePipe(dev)
        else:
            LOGGER.error("Incorrect input devices args")

