#!/usr/bin/python3

from ebf_show_version import EbfShowVersionCmd
#from ebf_show_led import EbfShowLedCmd

from logger import ebf_logger
LOGGER = ebf_logger(__name__)


class EbfShowManager(object):

    args = None

    def __init__(self, args):
        self.args = args

    def getCmdObject(self):
        cmdObjectList = {
            "version": "version",
                "led": "led"
        }

        methodName = None
        if self.args["version"]:
            methodName = "version"
        elif self.args["led"]:
            methodName = "led"

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
        pass
        #return EbfShowLedCmd(self.args)
