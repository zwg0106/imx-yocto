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
    coreutils               \
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
    e2fsprogs               \
    e2fsprogs-e2fsck        \
    e2fsprogs-tune2fs       \
    e2fsprogs-mke2fs        \
    python3-core            \
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
