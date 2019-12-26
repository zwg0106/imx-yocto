#!/usr/bin/python3

"""
Usage:
    show version [--Active | --Standby | --All]
    show led [--Green | --Red | --Blue | --All]
    show -h | --help
    config led (--Green | --Red | --Blue | --All) (--ON | --OFF | --BLINK)
    config input (--Key | --OnOff | --All) (--Enable | --Disable)
    config beep (--On | --Off)
    exit
Options:
    -h --help:  show usage
    --Active: active partition
    --Standby: standby partition
    --Green: green led
    --Blue: blue led
    --Red: red led
    --All: all partitions/leds/keys
    --Enable: enable to monitor keys
    --Disable: disable to monitor keys
"""

from ebf_show_cmd import EbfShowCmd
from ebf_show_manager import EbfShowManager
from ebf_config_cmd import EbfConfigCmd
from ebf_config_manager import EbfConfigManager

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
        args, doc = EbfShowCmd(self.cmd).execute()
        args = self.isHelp(args, doc)
        LOGGER.debug(args)
        if args:
            return EbfShowManager(args).getCmdObject()

    def config(self):
        args, doc = EbfConfigCmd(self.cmd).execute()
        args = self.isHelp(args, doc)
        LOGGER.debug(args)
        if args:
            return EbfConfigManager(args).getCmdObject()
