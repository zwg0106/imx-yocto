DESCRIPTION = "python packagegroup"

ALLOW_EMPTY_${PN} = "1"
PR = "r1"

PROVIDES = "${PACKAGES}"
PACKAGES = "\
        packagegroup-python \
        "

inherit packagegroup

RDEPENDS_packagegroup-python = "\
    python3-core 			\
    python3-logging         \
    python3-misc            \
    python3-json            \
    python3-shell           \
    python3-threading       \
    python3-prompt-toolkit  \
    python3-docopt          \
    python3-evdev           \
    python3-smbus           \
        "
