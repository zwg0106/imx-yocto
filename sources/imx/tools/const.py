import os

LOG_FILENAME = "imx_build.log"

MY_FILE = os.path.abspath(os.path.dirname(__file__))
TOOLS_DIR = os.path.abspath(MY_FILE)
USER_DIR = os.path.abspath(TOOLS_DIR)
SRC_DIR = os.path.abspath(USER_DIR)
PRJ_DIR = os.path.abspath(SRC_DIR)

LOCAL_CONF = "conf/local.conf"
SSATE_CACHE = PRJ_DIR + "/cache"
SOURCE_MIRROR_URL = "file:///" + SSATE_CACHE

INIT_CONF = "init.json"
IMX_IMAGE = imx-image
