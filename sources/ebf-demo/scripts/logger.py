#!/usr/bin/env python3

import logging
import logging.handlers

LOG_FILENAME="/var/log/ebf-demo.log"

def ebf_logger(mod_name):
    logger = logging.getLogger(mod_name)
    formatter = (
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    datefmt = '%Y-%m-%d %H:%M:%S'

    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, mode='a', maxBytes=1000000, encoding=None, delay=0)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(handler)
    
    return logger
