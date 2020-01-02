#!/usr/bin/python3

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

from ebf_show_cmd import EbfShowCmd

PATH=r"/sys/bus/iio/devices/iio:device0/in_voltage3_raw"
RANGE=4095
REF_VOL=3.3


class EbfShowAdcCmd(EbfShowCmd):
    args = None

    def __init__(self, args):
        self.args = args

    def execute(self):
        """
        Get adc value
        """

        LOGGER.debug(self.args)
        
        cmd = "{} {}".format("cat", PATH)
        output, errData = self.runShellCmd(cmd)

        output=output.decode().replace('\n', '')

        val = int(output)

        LOGGER.debug(val)

        vol = self._hex2vol(val)

        print("Current Voltage: %s V" % vol)

    def _hex2vol(self, val):
        """
        convert hex to valtage 
        """
        
        cmd = 'echo "scale=4;{}*{}/{}" | bc'.format(str(val), REF_VOL, RANGE)
        output, errData = self.runShellCmd(cmd)
       
        LOGGER.debug(output)
        return output.decode().replace('\n', '')
