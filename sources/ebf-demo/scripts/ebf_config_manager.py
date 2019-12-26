#!/usr/bin/python3

from ebf_config_led_cmd import EbfConfigLedCmd
from ebf_config_input_cmd import EbfConfigInputCmd

from logger import ebf_logger
LOGGER = ebf_logger(__name__)


class EbfConfigManager(object):

    args = None

    def __init__(self, args):
        self.args = args

    def getCmdObject(self):
        cmdObjectList = {
            "led": "led",
            "input": "input"
        }

        methodName = None
        if self.args["led"]:
            methodName = "led"
        elif self.args["input"]:
            methodName = "input"

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
