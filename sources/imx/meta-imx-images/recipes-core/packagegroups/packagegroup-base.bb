SUMMARY = "imx"
DESCRIPTION = "image base packagegroup"

ALLOW_EMPTY_${PN} = "1"
PR = "r1"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES = "packagegroup-base   \
    ${@bb.utils.contains('MACHINE_ARCH', 'hwasin', 'packagegroup-hwasin', '',d)} \
    "

RDEPENDS_packagegroup-base = "\
    ${@bb.utils.contains('MACHINE_ARCH', 'hwasin', 'packagegroup-hwasin', '',d)} \
    "

SUMMARY_packagegroup-hwasin = "hwasin specific"
DESCRIPTION_packagegroup-hwasin = "Packages required on the hwasin platform"
RDEPENDS_packagegroup-hwasin = "\
    pkg-install         \
    ebf-demo            \
    "
