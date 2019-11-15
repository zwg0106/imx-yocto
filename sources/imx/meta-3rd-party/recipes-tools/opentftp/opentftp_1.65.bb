DESCRIPTION = "OpenTFTP Daemon"
HOMEPAGE = "http://sourceforge.net/projects/tftp-server/"
SECTION = "base"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://LICENSE;md5=8a71d0475d08eee76d8b6d0c6dbec543"

RDEPENDS_${PN} = "bash"

inherit update-rc.d

PR = "r5"

SRC_URI = "http://iweb.dl.sourceforge.net/project/tftp-server/tftp%20server%20multithreaded/opentftpmtV${PV}.tar.gz"
#SRC_URI  = "${CLX_SOURCE_MIRROR_URL}/opentftpmtV${PV}.tar.gz"
SRC_URI += "file://Makefile \
            file://opentftp.conf \
            file://rc.opentftp \
            file://print-errno-for-opentftpd.patch \
            file://make-opentftpd-exit-directly-once-fd-leak.patch \
            file://fix-resources-leak.patch \
            "


# init-script rc.opentftp renamed to opentftp in Makefile
SRC_URI[md5sum] = "d012ba3651a7e1b375131e934218cf94"
SRC_URI[sha256sum] = "a89e3f8b2811534671c1e34506802aa27973b40c2c6e550a6c3568958cdbea3b"

# Go with the name in the tarball
S = "${WORKDIR}/opentftp"

INITSCRIPT_NAME = "opentftp"
INITSCRIPT_PARAMS = "defaults 4"
CONFFILES_${PN} = "${sysconfdir}/opentftp.conf"

do_link_files() {
    bbnote "Linking Files"
    cd ${S}
    # Files from the tarball that we don't need
    rm -rf opentftpd opentftp.ini rc.opentftp Makefile opentftp.conf
    ln -s ../Makefile .
    ln -s ../rc.opentftp .
    ln -s ../opentftp.conf .
}
addtask do_link_files after do_unpack before do_configure

do_install() {
    oe_runmake DESTDIR=${D} install
}

INSANE_SKIP_${PN} = "ldflags"
