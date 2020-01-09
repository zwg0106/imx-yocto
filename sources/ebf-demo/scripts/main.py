#!/usr/bin/python3

import os
import re
import json
from threading import Thread
from select import select
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from ebf_manager import EbfManager
from key_poll import PollKeyDevice
from mpu_server import MpuServer

from logger import ebf_logger
LOGGER=ebf_logger(__name__)

CMDJSONFILE="commands.json"
dataPath=os.path.dirname(os.path.realpath(__file__))
jsonFile = dataPath + '/' + CMDJSONFILE
if os.path.isfile(jsonFile):
    with open (jsonFile, 'r') as fp:
        cmdJsonData = fp.read()
    ebfCmdList = json.loads(cmdJsonData)


def autoComplete(_input, collection, accessor=lambda x: x):
    suggestions = []
    _input = str(_input) if not isinstance(_input, str) else _input
    if any ( char in ['?', '^', '$', '(', ')', '[', ']', '+', '*', '.', '#', '\\', '|'] for char in _input ):
        _input = re.escape(_input)

    pat = '(?=(^' + _input + '))'
    regex = re.compile(pat, re.IGNORECASE)
    for item in collection:
        r = list(regex.finditer(accessor(item)))
        if r:
            best = min(r, key=lambda x: len(x.group(1)))   # find shortest match
            suggestions.append((len(best.group(1)), best.start(), accessor(item), item))

    return (z[-1] for z in sorted(suggestions))


class AutoComplete(Completer):
    def get_completions(self, document, complete_event):
        line_before_cursor = document.current_line_before_cursor
        word_before_cursor = document.get_word_before_cursor(WORD=True)

        cmd = line_before_cursor.split()
        if not line_before_cursor:
            cmdList = ebfCmdList.keys()
        else:
            cmdList = ebfCmdList
            index = 0
            while(len(cmd) > index):
                if cmd[index]:
                    try:
                        key = cmd[index]
                        cmdList = cmdList[key]
                    except:
                        if type(cmdList) is dict and cmdList.keys():
                            if any ( char in ['?', '^', '$', '(', ')', '[', ']', '+', '*', '.', '#', '\\', '|'] for char in key ):
                                key = re.escape(key)
                            cmdList = list(filter(lambda x: re.search(r'^' + key, x), cmdList.keys()))
                        else:
                            cmdList = []

                if not cmdList:
                    cmdList = []
                    break

                index += 1

        matches = autoComplete(word_before_cursor, cmdList)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


class ebfShell:
    """
    setup ebf shell
    """
    
    def __init__(self):
        
        try:
            while True:
                try:
                    userInput = prompt(u'\nebf> ', history=FileHistory('history.txt'), completer=AutoComplete())
                    
                    if userInput:
                        cmd = userInput.split()
                        if not cmd:
                            continue

                        cmd = [str(arg) for arg in cmd]

                        ebfManager = EbfManager(cmd)
                        cmdOject = ebfManager.getCmdObject()

                        if cmdOject:
                            cmdOject.execute()

                except KeyboardInterrupt as e:
                    return 
		
        except Exception as e:
            LOGGER.error("ERR")
            errorStr = "[%s]: %s" % (str(e.errno), e.message)
            LOGGER.error(errorStr)
            return


if __name__ == '__main__':
    
    keyPollIns = PollKeyDevice()
    keyPollIns.threadStart()

    mpuIns = MpuServer()
    mpuIns.threadStart()

    ebfShell()
