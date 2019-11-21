DESCRIPTION = "initramfs modular system"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
RDEPENDS_${PN} = "busybox"

PR = "r5"

inherit allarch

SRC_URI = "file://init \
           file://finish \
           file://mdev \
           file://mnt \
           file://udev \
           file://resume \
           file://e2fs \
           file://debug \
           file://fstab"

S = "${WORKDIR}"

do_install() {
    install -d ${D}/init.d
    install -d ${D}/${sysconfdir}

    # fstab
    install -m 0644 ${WORKDIR}/fstab ${D}/${sysconfdir}/fstab

    # base
    install -m 0755 ${WORKDIR}/init ${D}/init
    install -m 0755 ${WORKDIR}/finish ${D}/init.d/99-finish

    # mdev
    install -m 0755 ${WORKDIR}/mdev ${D}/init.d/01-mdev

    # mnt
    install -m 0755 ${WORKDIR}/mnt ${D}/init.d/20-mnt

    # udev
    install -m 0755 ${WORKDIR}/udev ${D}/init.d/01-udev

    # resume after udev
    install -m 0755 ${WORKDIR}/resume ${D}/init.d/02-resume

    # e2fs
    install -m 0755 ${WORKDIR}/e2fs ${D}/init.d/10-e2fs

    # debug
    install -m 0755 ${WORKDIR}/debug ${D}/init.d/00-debug
}

PACKAGES = "${PN}-base \
            initramfs-imx-module-mdev \
            initramfs-imx-module-mnt \
            initramfs-imx-module-udev \
            initramfs-imx-module-e2fs \
            initramfs-imx-module-debug"

FILES_${PN}-base = "/init /init.d/99-finish /etc/fstab /init.d/02-resume"

DESCRIPTION_initramfs-imx-module-mdev = "initramfs support for mdev"
RDEPENDS_initramfs-imx-module-mdev = "${PN}-base"
FILES_initramfs-imx-module-mdev = "/init.d/01-mdev"

DESCRIPTION_initramfs-imx-module-mnt = "initramfs support for mnt"
RDEPENDS_initramfs-imx-module-mnt = "${PN}-base"
FILES_initramfs-imx-module-mnt = "/init.d/20-mnt"

DESCRIPTION_initramfs-imx-module-udev = "initramfs support for udev"
RDEPENDS_initramfs-imx-module-udev = "${PN}-base udev"
#RDEPENDS_initramfs-imx-module-udev = "${PN}-base udev udev-utils"
FILES_initramfs-imx-module-udev = "/init.d/01-udev"

DESCRIPTION_initramfs-imx-module-resume = "initramfs support for hibernate resume"
RDEPENDS_initramfs-imx-module-resume = "${PN}-base"
FILES_initramfs-imx-module-resume = "/init.d/02-resume"

DESCRIPTION_initramfs-imx-module-e2fs = "initramfs support for ext4/ext3/ext2 filesystems"
RDEPENDS_initramfs-imx-module-e2fs = "${PN}-base"
FILES_initramfs-imx-module-e2fs = "/init.d/10-e2fs"

DESCRIPTION_initramfs-imx-module-debug = "initramfs dynamic debug support"
RDEPENDS_initramfs-imx-module-debug = "${PN}-base"
FILES_initramfs-imx-module-debug = "/init.d/00-debug"
