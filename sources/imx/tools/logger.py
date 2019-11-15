import logging
from const import LOG_FILENAME

def yocto_imx_logger(mod_name):
    logger = logging.getLogger(mod_name)
    formatter = (
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    datefmt = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(level=logging.DEBUG, format=formatter, datefmt=datefmt, filename=LOG_FILENAME, filemode='w')
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(handler)

    return logger
