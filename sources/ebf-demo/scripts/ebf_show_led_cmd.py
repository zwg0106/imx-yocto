#!/usr/bin/python3

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

from ebf_show_cmd import EbfShowCmd

showLedStatusBaseCmd = r"cat /sys/class/leds/"
showLedStatusRedCmd = showLedStatusBaseCmd + r"red/brightness"
showLedStatusGreenCmd = showLedStatusBaseCmd + r"green/brightness"
showLedStatusBlueCmd = showLedStatusBaseCmd + r"blue/brightness"
showLedStatusAllcmd = [showLedStatusRedCmd, showLedStatusGreenCmd, showLedStatusBlueCmd]
showLedTriggerModRedCmd = showLedStatusBaseCmd + r"red/trigger"
showLedTriggerModGreenCmd = showLedStatusBaseCmd + r"green/trigger"
showLedTriggerModBlueCmd = showLedStatusBaseCmd + r"blue/trigger"
showLedTiggerModAllcmd = [showLedTriggerModRedCmd, showLedTriggerModGreenCmd, showLedTriggerModBlueCmd]


class EbfShowLedCmd(EbfShowCmd):
    args = None

    def __init__(self, args):
        self.args = args

    def execute(self):
        """
        Get Led Status
        """

        LOGGER.debug(self.args)
        if self.args["--All"]:
            cmdStatus = showLedStatusAllcmd
            cmdTrigger = showLedTiggerModAllcmd
            ledLabel = ["Red", "Green", "Blue"]
        elif self.args["--Red"]:
            cmdStatus = showLedStatusRedCmd
            cmdTrigger = showLedTriggerModRedCmd
            ledLabel = "Red"
        elif self.args["--Blue"]:
            cmdStatus = showLedStatusBlueCmd
            cmdTrigger = showLedTriggerModBlueCmd
            ledLabel = "Blue"
        elif self.args["--Green"]:
            cmdStatus = showLedStatusGreenCmd
            cmdTrigger = showLedTriggerModGreenCmd
            ledLabel = "Green"
        else:
            LOGGER.debug("Unkonwn LED args, set args to All be default")
            cmdStatus = showLedStatusAllcmd
            cmdTrigger = showLedTiggerModAllcmd
            ledLabel = ["Red", "Green", "Blue"]

        if isinstance(cmdStatus, list) and isinstance(cmdTrigger, list):
            # loop cmd trigger & status 
            for index in range(len(cmdStatus)):
                self._handleShowLedCmd(ledLabel[index], cmdStatus[index], cmdTrigger[index])
        else:
            self._handleShowLedCmd(ledLabel, cmdStatus, cmdTrigger)

    def _handleShowLedCmd(self, label, statusCmd, triggerCmd):
        
        if statusCmd is None or triggerCmd is None:
            LOGGER.error("Cmd of status or trigger is NOne")
            return

        output, errData = self.runShellCmd(triggerCmd)
        if errData:
            LOGGER.error("Error cmd (%s) output: %s", cmd, errData.decode())

        if output:
            output = output.decode()
            LOGGER.debug("Cmd: %s, output: %s", triggerCmd, output)
            result = r"[none]" in output
            if result:
                output, errData = self.runShellCmd(statusCmd)
                if errData:
                    LOGGER.error("Error cmd (%s) output: %s", cmd, errData.decode())

                if output:
                    output = output.decode().replace('\n', '')
                    LOGGER.debug("Cmd: %s, output: %s", statusCmd, output)
                    if int(output) != 0:
                        print("{} : {} - [{}/{}]".format(label, "ON", output, "255"))
                    else:
                        print("{} : {}".format(label, "OFF"))
                else:
                    LOGGER.error("No response data from cmd (%s)", statusCmd)
                
                return

            else:
                result = r"[heartbeat]" in output
                if result:
                    print("{} : {}".format(label, "BLINK"))
                else:
                    LOGGER.error("Unknow LED trigger mode [%s]", output)

        else:
            LOGGER.error("No response data from cmd (%s)", triggerCmd)
