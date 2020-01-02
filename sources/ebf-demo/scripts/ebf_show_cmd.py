#!/usr/bin/python3

"""
Usage:
    show version [--Active | --Standby | --All]
    show led [--Green | --Red | --Blue | --All]
    show mpu6050
    show -h | --help
Options:
    -h --help:  show usage
    --Active: active partition
    --Standby: standby partition
    --Green: green led
    --Blue: blue led
    --Red: red led
    --All: all partitions/leds
"""

from docopt import docopt, DocoptExit, DocoptLanguageError

from logger import ebf_logger
LOGGER=ebf_logger(__name__)

from ebf_cmd import EbfCmd

class EbfShowCmd(EbfCmd):
    """
    handle show command
    """
    
    cmd = None

    def __init__(self, cmd):
        self.cmd = cmd

    def execute(self):
        self.cmd.pop(0)
        LOGGER.debug(self.cmd)

        try:
            args = docopt(__doc__, self.cmd, help=True)
            return args, __doc__
        except DocoptExit as e:
            LOGGER.error(e)
            return None, None
