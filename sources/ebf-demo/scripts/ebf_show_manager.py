#!/usr/bin/python3

from ebf_show_version_cmd import EbfShowVersionCmd
from ebf_show_led_cmd import EbfShowLedCmd
from ebf_show_adc_cmd import EbfShowAdcCmd

from logger import ebf_logger
LOGGER = ebf_logger(__name__)


class EbfShowManager(object):

    args = None

    def __init__(self, args):
        self.args = args

    def getCmdObject(self):
        cmdObjectList = {
            "version": "version",
                "led": "led",
                "adc": "adc"
        }

        methodName = None
        if self.args["version"]:
            methodName = "version"
        elif self.args["led"]:
            methodName = "led"
        elif self.args["adc"]:
            methodName = "adc"

        LOGGER.debug(methodName)
        if methodName in cmdObjectList:
            method = getattr(self, methodName, lambda: 'Invalid command')
            return method()
        elif self.cmd[0]:
            LOGGER.error("Invalid command")
            LOGGER.error(__doc__)

    def version(self):
        LOGGER.debug(self.args)
        return EbfShowVersionCmd(self.args)

    def led(self):
        LOGGER.debug(self.args)
        return EbfShowLedCmd(self.args)
    
    def adc(self):
        LOGGER.debug(self.args)
        return EbfShowAdcCmd(self.args)
