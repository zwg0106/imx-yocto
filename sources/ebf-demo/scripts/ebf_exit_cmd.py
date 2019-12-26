#!/usr/bin/python3

"""
Usage:
    exit
"""
import sys
from docopt import docopt, DocoptExit, DocoptLanguageError

from logger import ebf_logger
LOGGER=ebf_logger(__name__)

from ebf_cmd import EbfCmd

class EbfExitCmd(EbfCmd):
    """
    handle exit command
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
            print("Exiting ebf CLI...")
            sys.exit()
        except DocoptExit as e:
            LOGGER.error(e)
            return None, None
