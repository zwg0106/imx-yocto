FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

COMPATIBLE_MACHINE_hwasin = "hwasin"

SRCREV_aufs = "34be418bd4f0bb069e3971c76f5a8d8a6038558a"

SRC_URI_append = " \
    git://github.com/sfjro/aufs4-standalone.git;branch=aufs4.9;name=aufs;destsuffix=aufs4-standalone \
    file://0001-imx6ull-misc-patch.patch \
    file://0002-dht-patch.patch \
    file://0003-leds-patch.patch \
    file://0004-ov5460-patch.patch \
    file://0005-touch-screen-gt9xx-patch.patch \
    file://0006-bcmdhd-patch.patch \
    file://0007-mmc-patch.patch \
    file://0008-usb-patch.patch \
    file://0009-video-patch.patch \
    file://0010-bcm43430-patch.patch \
    file://new-files/arch/arm/configs/hwasin_defconfig \
    file://new-files/arch/arm/boot/dts/hwasin.dts \
    file://new-files/arch/arm/boot/dts/hwasin-emmc.dts \
    file://new-files/arch/arm/boot/dts/hwasin-emmc-hdmi.dts \
"

do_copy_new_files() {
    if [ -d ${WORKDIR}/new-files ]; then
        cp -a ${WORKDIR}/new-files/* ${S}/
    fi
}

addtask copy_new_files after do_patch before do_merge_defconfig

do_merge_defconfig() {
    cp ${S}/arch/arm/configs/hwasin_defconfig ${KERNEL_DEFCONFIG}
}

addtask merge_defconfig before do_preconfigure after do_patch

# The following steps are as per ${WORKDIR}/aufs4-standalone/README
do_aufs() {
    cd ${S}
    patch -p1 -d ${S} -i ${WORKDIR}/aufs4-standalone/aufs4-kbuild.patch
    patch -p1 -d ${S} -i ${WORKDIR}/aufs4-standalone/aufs4-base.patch
    patch -p1 -d ${S} -i ${WORKDIR}/aufs4-standalone/aufs4-mmap.patch
    patch -p1 -d ${S} -i ${WORKDIR}/aufs4-standalone/lockdep-debug.patch
    patch -p1 -d ${S} -i ${WORKDIR}/aufs4-standalone/tmpfs-idr.patch
    patch -p1 -d ${S} -i ${WORKDIR}/aufs4-standalone/vfs-ino.patch


    aufs_doc="${WORKDIR}/aufs4-standalone/Documentation/*"
    cp -r ${aufs_doc} ${S}/Documentation
    cp -r ${WORKDIR}/aufs4-standalone/fs/aufs ${S}/fs
    cp ${WORKDIR}/aufs4-standalone/include/uapi/linux/aufs_type.h ${S}/include/uapi/linux/
}

addtask aufs after do_unpack before do_patch
