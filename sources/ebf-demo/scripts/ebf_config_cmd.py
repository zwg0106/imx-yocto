#!/usr/bin/python3

"""
Usage:
    config led (--Green | --Red | --Blue | --All) (--ON | --OFF | --BLINK)
    config input (--Key | --OnOff | --All) (--Enable | --Disable)
    config beep (--On | --Off)
    config -h | --help
Options:
    -h --help:  show usage
    --Green: green led
    --Blue: blue led
    --Red: red led
    --All: all leds/keys
    --Enable: enable to monitor keys
    --Disable: disable to monitor keys
"""

from docopt import docopt, DocoptExit, DocoptLanguageError

from logger import ebf_logger
LOGGER=ebf_logger(__name__)

from ebf_cmd import EbfCmd

class EbfConfigCmd(EbfCmd):
    """
    handle config command
    """
    
    cmd = None

    def __init__(self, cmd):
        self.cmd = cmd

    def execute(self):
        self.cmd.pop(0)
        LOGGER.debug(self.cmd)
        LOGGER.debug(__doc__)

        try:
            args = docopt(__doc__, self.cmd, help=True)
            return args, __doc__
        except DocoptExit as e:
            LOGGER.error(e)
            return None, None
