#!/usr/bin/python3

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

showActiveVersionCmd = r"pkg-install.sh -i | egrep Active | tail -n 1 | awk '{print $3}'"
showStandbyVersionCmd = r"pkg-install.sh -i | egrep Standby | tail -n 1 | awk '{print $3}'"
showAllVersionCmd = r"pkg-install.sh -i | egrep 'Active|Standby' | tail -n 2 | awk '{print $3}'"

from ebf_show_cmd import EbfShowCmd

class EbfShowVersionCmd(EbfShowCmd):
    args = None

    def __init__(self, args):
        self.args = args

    def execute(self):
        """
        Get version
        """
        LOGGER.debug(self.args)
        if self.args["--Active"]:
            cmd = showActiveVersionCmd
        elif self.args["--Standby"]:
            cmd = showStandbyVersionCmd
        else:
            cmd = showAllVersionCmd

        output, errData = self.runShellCmd(cmd)

        if errData:
            LOGGER.error("Error cmd (%s) output: %s", cmd, errData.decode())

        if output:
            output = output.decode()
            if self.args["--Active"]:
                partition = "Active"
            elif self.args["--Standby"]:
                partition = "Standby"
            else:
                partition = "All"

            if partition == "All":
                act = output.split('\n')[0]
                sby = output.split('\n')[1]
                print("{}:{}".format("Active", act))
                print("{}:{}".format("Standby", sby))
            else:
                print("{}:{}".format(partition, output))
