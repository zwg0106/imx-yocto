#!/usr/bin/python3

from os import path
from logger import ebf_logger
LOGGER = ebf_logger(__name__)

from ebf_config_cmd import EbfConfigCmd

configBeepPath=r"/sys/class/gpio/"
configBeepGpioIndex="19"
configBeepIndexPath=configBeepPath + "gpio" + configBeepGpioIndex
configBeepExport=configBeepPath + "export"
configBeepGpioDirection=configBeepIndexPath + "/" + "direction"
configBeepstatusPath=configBeepIndexPath + "/value"

class EbfConfigBeepCmd(EbfConfigCmd):
    args = None

    def __init__(self, args):
        self.args = args

    def execute(self):
        """
        set beep status
        """

        LOGGER.debug(self.args)
        if self.args["--On"]:
            val = "1"
        elif self.args["--Off"]:
            val = "0"
        else:
            LOGGER.debug("Unkown Beep args")
            return

        # check if beep gpio exported or not
        if not path.exists(configBeepIndexPath):
            exportCmd = "{} {} > {}".format("echo", configBeepGpioIndex, configBeepExport) 
            self._handleconfigBeepCmd(exportCmd)

            outModeCmd = "{} {} > {}".format("echo", "'out'", configBeepGpioDirection)
            self._handleconfigBeepCmd(outModeCmd)

        # set beep
        beepStatusCmd = "{} {} > {}".format("echo", val, configBeepstatusPath)
        self._handleconfigBeepCmd(beepStatusCmd)

    def _handleconfigBeepCmd(self, cmd):
        
        if cmd is None:
            LOGGER.error("Cmd of beep is None")
            return

        LOGGER.debug(cmd)
        _, errData = self.runShellCmd(cmd)
        if errData:
            LOGGER.error("Error cmd (%s) output: %s", cmd, errData.decode())
