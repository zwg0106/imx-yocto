SUMMARY = "imx"
DESCRIPTION = "image ramdisk packagegroup"

ALLOW_EMPTY_${PN} = "1"
PR = "r1"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES = "packagegroup-ramdisk-base   \
    ${@bb.utils.contains('MACHINE_ARCH', 'hwasin', 'packagegroup-ramdisk-hwasin', '',d)} \
    "

RDEPENDS_packagegroup-ramdisk-base = "\
    ${@bb.utils.contains('MACHINE_ARCH', 'hwasin', 'packagegroup-ramdisk-hwasin', '',d)} \
    "

SUMMARY_packagegroup-ramdisk-hwasin = "hwasin specific"
DESCRIPTION_packagegroup-ramdisk-hwasin = "Packages required on the hwasin platform"
RDEPENDS_packagegroup-ramdisk-hwasin = "\
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
    init-ifupdown           \
    python3-core            \
    "
