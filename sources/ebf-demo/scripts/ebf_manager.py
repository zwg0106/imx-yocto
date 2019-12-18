#!/usr/bin/python3

"""
Usage:
    show version [--Active | --Standby]
    show led [--Green | --Red | --Blue]
    show -h | --help
    config led (Green|Red|Blue) (ON|OFF|BLINK)
    exit
Options:
    -h --help:  show usage
    --Active: active partition
    --Standby: standby partition
"""

from ebf_show_command import EbfShowCommand
from ebf_show_manager import EbfShowManager

from logger import ebf_logger
LOGGER = ebf_logger(__name__)


class EbfManager(object):
    """
    manage cmds from user
    """
    cmd = None

    def __init__(self, cmd):
        self.cmd = cmd

    def getCmdObject(self):
        cmdObjectList = {
            "show": "show",
            "config": "config",
            "exit": "exit"
        }

        methodName = self.cmd[0]
        if methodName in cmdObjectList:
            method = getattr(self, methodName, lambda: 'Invalid command')
            return method()
        elif self.cmd[0]:
            LOGGER.error("Invalid command")
            LOGGER.error(__doc__)

    def isHelp(self, args, doc):
        if args and args["--help"]:
            LOGGER.debug(doc)
            return

        return args

    def show(self):
        args, doc = EbfShowCommand(self.cmd).execute()
        args = self.isHelp(args, doc)
        LOGGER.debug(args)
        if args:
            return EbfShowManager(args).getCmdObject()
