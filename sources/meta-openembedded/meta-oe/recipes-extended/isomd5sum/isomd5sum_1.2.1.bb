SUMMARY = "Tools for taking the MD5 sum of ISO images"
DESCRIPTION = "Tools for taking the MD5 sum of ISO images"

DEPENDS = "popt python3 openssl curl popt-native"
RDEPENDS_${PN} = "openssl curl"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=8ca43cbc842c2336e835926c2166c28b"

SRC_URI = "git://github.com/rhinstaller/isomd5sum.git;branch=master \
           file://0001-tweak-install-prefix.patch \
           file://0002-fix-parallel-error.patch \
"

S = "${WORKDIR}/git"
inherit python3native

EXTRA_OEMAKE += " \
    DESTDIR='${D}' \
    PYTHONINCLUDE='-I${STAGING_INCDIR}/${PYTHON_DIR}${PYTHON_ABI}' \
    PYTHONSITEPACKAGES='${PYTHON_SITEPACKAGES_DIR}' \
"

do_install () {
    oe_runmake install
}

PACKAGES += "${PYTHON_PN}-${PN} ${PYTHON_PN}-${PN}-dbg"

FILES_${PYTHON_PN}-${PN} = "${PYTHON_SITEPACKAGES_DIR}/pyisomd5sum.so"
FILES_${PYTHON_PN}-${PN}-dbg = "${PYTHON_SITEPACKAGES_DIR}/.debug/pyisomd5sum.so"

SRCREV = "69dc036d20761715b734ca9cc59ecc6dc8145026"

BBCLASSEXTEND = "native"
