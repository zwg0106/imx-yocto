#!/usr/bin/python3

import subprocess

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

showActiveVersionCmd = r"pkg-install.sh -i | egrep Active | tail -n 1 | awk '{print $3}'"
showStandbyVersionCmd = r"pkg-install.sh -i | egrep Standby | tail -n 1 | awk '{print $3}'"
showAllVersionCmd = r"pkg-install.sh -i | egrep 'Active|Standby' | tail -n 2 | awk '{print $3}'"


class EbfShowVersionCmd(object):
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

        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            p.wait()
            output = p.communicate()[0].decode()
        except ValueError:
            LOGGER.error(
                "Invalid argument provided to Popen while trying to exec cmd")
            return
        except OSError as e:
            LOGGER.error("Error forking the process while trying to exec cmdline")
            errorStr = "[%s]: %s" % (str(e.errno), e.message)
            LOGGER.error(errorStr)
            return

        if output:
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
