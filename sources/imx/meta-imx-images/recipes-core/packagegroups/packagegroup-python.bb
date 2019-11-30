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
    python3-xml             \
    python3-logging         \
    python3-io              \
    python3-misc            \
    python3-json            \
    python3-multiprocessing \
    python3-shell           \
    python3-threading       \
    python3-pexpect         \
        "
