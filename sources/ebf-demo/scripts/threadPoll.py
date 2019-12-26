#!/usr/bin/python3

import os
from select import select
from threading import Thread
from evdev import InputDevice, ecodes

from logger import ebf_logger
LOGGER = ebf_logger(__name__)

keyInputPath = r"/dev/input/by-path/platform-gpio-keys-event"
onOffInputPath = r"/dev/input/by-path/platform-20cc000.snvs:snvs-powerkey-event"

inputKeyDict = {
    "key": InputDevice(keyInputPath),
    "onoff": InputDevice(onOffInputPath)
}


class ThreadPollDevice(object):
    pollPipe = os.pipe()

    def __init__(self):
        self.inputFd = []
        LOGGER.debug("Init ThreadPollDevice")

    def threadStart(self):

        Thread(target=self._monitorInput, daemon=True).start()

    def _monitorInput(self):
        """
        monitor pipe data and input devices
        """
        LOGGER.debug("Start to monitor pipe data and input devices...")

		# only poll pipe by default, input devices is added by CLI commands
        self.inputFd.append(self.pollPipe[0])

        while True:
            rd, _, _ = select(self.inputFd, [], [])
            # handle pipe
            if self.pollPipe[0] in rd:
				# read data from Pipe
                # 4 cases:
                #   1) "none"
                #   2) "key:enable/disable"
                #   3) "onoff:enable/disable"
                #   4) "all"
                tmpDev = os.read(self.pollPipe[0], 20).decode()
                if tmpDev == "none":
                    self.inputFd = [self.pollPipe[0]]
                elif tmpDev == "all":
                    self.inputFd = [self.pollPipe[0]]
                    for key in inputKeyDict.keys():
                        self.inputFd.append(inputKeyDict[key]) 
                else:
                    tmpL = tmpDev.split(':') 
                    if tmpL[1] == "enable":
                        self.inputFd.append(inputKeyDict[tmpL[0]]) if inputKeyDict[tmpL[0]] not in self.inputFd else self.inputFd
                    elif tmpL[1] == "disable":
                        self.inputFd.remove(inputKeyDict[tmpL[0]]) if inputKeyDict[tmpL[0]] in self.inputFd else self.inputFd
                    else:
                        LOGGER.error("Unknown input device type")
                LOGGER.debug("input Fd: %s", self.inputFd)

            # handle input devices
            for index in self.inputFd:
                if index is self.pollPipe[0]:
                    continue
                if index in rd:
                    for event in index.read():
                        if event.type != ecodes.EV_SYN:
                            LOGGER.info(event)

    @classmethod
    def writePipe(cls, data):
	
        LOGGER.debug("Write %s to pipe %d" % (data, cls.pollPipe[1]))
        os.write(cls.pollPipe[1], bytes(data, encoding='utf-8'))

    def threadStop(self):
		
        pass
