SUMMARY = "imx"
DESCRIPTION = "image micro packagegroup"

ALLOW_EMPTY_${PN} = "1"
PR = "r1"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES = "packagegroup-micro-base   \
    ${@bb.utils.contains('MACHINE_ARCH', 'hwasin', 'packagegroup-micro-hwasin', '',d)} \
    "

RDEPENDS_packagegroup-micro-base = "\
    ${@bb.utils.contains('MACHINE_ARCH', 'hwasin', 'packagegroup-micro-hwasin', '',d)} \
    "

SUMMARY_packagegroup-micro-hwasin = "hwasin specific"
DESCRIPTION_packagegroup-micro-hwasin = "Packages required on the hwasin platform"
RDEPENDS_packagegroup-micro-hwasin = "\
    bash                    \
    file                    \
    findutils               \
    tar                     \
    vim-tiny                \
    mmc-utils               \
    opentftp                \
    openssh                 \
    i2c-tools               \
    usbutils                \
    iputils                 \
    net-tools               \
    start-stop-daemon       \
    procps                  \
    python3-core            \
    "
