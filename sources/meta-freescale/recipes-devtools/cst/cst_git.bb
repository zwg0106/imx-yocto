SUMMARY = "utility for security boot"
SECTION = "cst"
LICENSE = "BSD"

LIC_FILES_CHKSUM = "file://COPYING;md5=e959d5d617e33779d0e90ce1d9043eff"

DEPENDS += "openssl"
RDEPENDS_${PN} = "bash"

inherit kernel-arch

SRC_URI = "git://source.codeaurora.org/external/qoriq/qoriq-components/cst;nobranch=1 \
    file://0001-gen_otpmk_drbg-fails-compilation-due-to-uninitialize.patch \
"
SRCREV = "e9abf79077fc8faf976e9a3c46a38111aa5b2e69"

S = "${WORKDIR}/git"

EXTRA_OEMAKE = 'CC="${CC}" LD="${CC}"'

PARALLEL_MAKE = ""

do_install () {
    oe_runmake install DESTDIR=${D} BIN_DEST_DIR=${bindir}
}

FILES_${PN}-dbg += "${bindir}/cst/.debug"
BBCLASSEXTEND = "native nativesdk"
