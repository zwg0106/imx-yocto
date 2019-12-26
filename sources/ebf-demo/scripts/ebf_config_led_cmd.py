#!/usr/bin/python3

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

from ebf_config_cmd import EbfConfigCmd

configLedStatusBaseCmd = r" /sys/class/leds/"
configLedStatusRedCmd = configLedStatusBaseCmd + r"red/brightness"
configLedStatusGreenCmd = configLedStatusBaseCmd + r"green/brightness"
configLedStatusBlueCmd = configLedStatusBaseCmd + r"blue/brightness"
configLedStatusAllcmd = [configLedStatusRedCmd, configLedStatusGreenCmd, configLedStatusBlueCmd]
configLedTriggerModRedCmd = configLedStatusBaseCmd + r"red/trigger"
configLedTriggerModGreenCmd = configLedStatusBaseCmd + r"green/trigger"
configLedTriggerModBlueCmd = configLedStatusBaseCmd + r"blue/trigger"
configLedTiggerModAllcmd = [configLedTriggerModRedCmd, configLedTriggerModGreenCmd, configLedTriggerModBlueCmd]


class EbfConfigLedCmd(EbfConfigCmd):
    args = None

    def __init__(self, args):
        self.args = args

    def execute(self):
        """
        Get Led Status
        """

        LOGGER.debug(self.args)
        if self.args["--All"]:
            cmdStatus = configLedStatusAllcmd
            cmdTrigger = configLedTiggerModAllcmd
        elif self.args["--Red"]:
            cmdStatus = configLedStatusRedCmd
            cmdTrigger = configLedTriggerModRedCmd
        elif self.args["--Blue"]:
            cmdStatus = configLedStatusBlueCmd
            cmdTrigger = configLedTriggerModBlueCmd
        elif self.args["--Green"]:
            cmdStatus = configLedStatusGreenCmd
            cmdTrigger = configLedTriggerModGreenCmd
        else:
            LOGGER.debug("Unkonwn LED args, set args to All be default")
            return
        
        if self.args["--BLINK"]:
            val = None 
        elif self.args["--ON"]:
           val = 127
        elif self.args["--OFF"]:
            val = 0
        else:
            LOGGER.debug("Unknow LED value")
            return

        if isinstance(cmdStatus, list) and isinstance(cmdTrigger, list):
            for index in range(len(cmdTrigger)):
                if val is not None:
                    triggerCmd = "{} {} > {}".format("echo", "none", cmdTrigger[index])
                    statusCmd = "{} {} > {}".format("echo", str(val), cmdStatus[index])
                else:
                    triggerCmd = "{} {} > {}".format("echo", "heartbeat", cmdTrigger[index])
                    statusCmd = None

                self._handleconfigLedCmd(triggerCmd, statusCmd)
        else:
            if val is not None:
                triggerCmd = "{} {} > {}".format("echo", "none", cmdTrigger)
                statusCmd = "{} {} > {}".format("echo", str(val), cmdStatus)
            else:
                triggerCmd = "{} {} > {}".format("echo", "heartbeat", cmdTrigger)
                statusCmd = None

            self._handleconfigLedCmd(triggerCmd, statusCmd)

    def _handleconfigLedCmd(self, triggerCmd, statusCmd=None):
        
        if triggerCmd is None:
            LOGGER.error("Cmd of trigger is NOne")
            return

        LOGGER.debug(triggerCmd)
        output, errData = self.runShellCmd(triggerCmd)
        if errData:
            LOGGER.error("Error cmd (%s) output: %s", triggerCmd, errData.decode())
    
        if statusCmd:
            LOGGER.debug(statusCmd)
            output, errData = self.runShellCmd(statusCmd)
            if errData:
                LOGGER.error("Error cmd (%s) output: %s", statusCmd, errData.decode())
