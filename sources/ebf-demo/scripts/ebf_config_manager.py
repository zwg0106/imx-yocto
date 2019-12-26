#!/usr/bin/python3

from ebf_config_led_cmd import EbfConfigLedCmd
from ebf_config_input_cmd import EbfConfigInputCmd
from ebf_config_beep_cmd import EbfConfigBeepCmd

from logger import ebf_logger
LOGGER = ebf_logger(__name__)


class EbfConfigManager(object):

    args = None

    def __init__(self, args):
        self.args = args

    def getCmdObject(self):
        cmdObjectList = {
            "led": "led",
            "input": "input",
            "beep": "beep"
        }

        methodName = None
        if self.args["led"]:
            methodName = "led"
        elif self.args["input"]:
            methodName = "input"
        elif self.args["beep"]:
            methodName = "beep"
        else:
            LOGGER.error("Unknown device")
            return

        LOGGER.debug(methodName)
        if methodName in cmdObjectList:
            method = getattr(self, methodName, lambda: 'Invalid command')
            return method()
        elif self.cmd[0]:
            LOGGER.error("Invalid command")
            LOGGER.error(__doc__)


    def led(self):
        LOGGER.debug(self.args)
        return EbfConfigLedCmd(self.args)
    
    def input(self):
        LOGGER.debug(self.args)
        return EbfConfigInputCmd(self.args)
    
    def beep(self):
        LOGGER.debug(self.args)
        return EbfConfigBeepCmd(self.args)
