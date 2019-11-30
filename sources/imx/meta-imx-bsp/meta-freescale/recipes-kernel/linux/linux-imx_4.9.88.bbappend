FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

DEPENDS += "imx-image-initramfs"

COMPATIBLE_MACHINE_hwasin = "hwasin"

SRC_URI_append = " \
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
