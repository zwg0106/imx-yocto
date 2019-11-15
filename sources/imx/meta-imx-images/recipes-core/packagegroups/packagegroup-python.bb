DESCRIPTION = "python packagegroup"

ALLOW_EMPTY_${PN} = "1"
PR = "r1"

PROVIDES = "${PACKAGES}"
PACKAGES = "\
        packagegroup-python \
        "

inherit packagegroup

RDEPENDS_packagegroup-python = "\
    python \
    python-argparse \
    python-compile \
    python-compiler \
    python-compression \
    python-core \
    python-curses \
    python-datetime \
    python-db \
    python-debugger \
    python-fcntl \
    python-io \
    python-json \
    python-logging \
    python-misc \
    python-mmap \
    python-multiprocessing \
    python-netclient \
    python-pexpect \
    python-pickle \
    python-pkgutil \
    python-pprint \
    python-re \
    python-shell \
    python-subprocess \
    python-syslog \
    python-textutils \
    python-threading \
    python-unixadmin \
    python-xmlrpc \
    python-xml  \
    python3-core \
        "
