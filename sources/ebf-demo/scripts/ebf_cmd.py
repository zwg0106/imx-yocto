from abc import abstractmethod
import subprocess

from logger import ebf_logger
LOGGER = ebf_logger(__name__)


class EbfCmd(object):

    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    def runShellCmd(self, cmd):
        """
        run shell cmd
        """

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            process.wait()
            stdoutData, stderrData = process.communicate()
        except ValueError:
            LOGGER.error("Invalid argument provided to Popen while trying to exec cmd")
            return None, None
        except OSError as e:
            LOGGER.error("Error forking the process while trying to exec cmdline")
            errorStr = "[%s]: %s" % (str(e.errno), e.message)
            LOGGER.error(errorStr)
            return None, None

        return stdoutData, stderrData
