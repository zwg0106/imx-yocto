DESCRIPTION = "makeself.sh is a small shell script that generates a \
self-extractable tar.gz archive from a directory. The resulting file \
appears as a shell script (many of those have a .run suffix), and \
can be launched as is. The archive will then uncompress itself to a \
temporary directory and an optional arbitrary command will be executed \
(for example an installation script)."
SECTION = "devel"
LICENSE = "GPLv2"
RDEPENDS_${PN} = "bash"

#
# SHA1 of master branch on Dec 03, 2012:
# 
SRCREV="521e0e35afcb49c38346a031bfc4025c2b2b1973"
SRC_URI = "git://github.com/megastep/makeself.git;protocol=git;branch=master \
            file://makerun.sh \
            file://makeself.patch"

S = "${WORKDIR}/git"

LIC_FILES_CHKSUM = "file://COPYING;md5=ea5bed2f60d357618ca161ad539f7c0a"

BBCLASSEXTEND = "native"

do_install () {
        install -d ${D}${bindir}
        install -m 0755 ${S}/makeself.sh ${S}/makeself-header.sh ${WORKDIR}/makerun.sh ${D}${bindir}/
}
