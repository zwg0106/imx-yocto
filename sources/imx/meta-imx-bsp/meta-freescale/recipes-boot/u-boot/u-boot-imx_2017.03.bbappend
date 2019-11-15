FILESEXTRAPATHS_prepend := "${THISDIR}/u-boot-imx_2017.03:"

COMPATIBLE_MACHINE_hwasin = "hwasin"

SRC_URI_append = " \
    file://new-files/arch/arm/dts/hwasin.dts \
    file://new-files/arch/arm/dts/hwasin-emmc.dts \
    file://new-files/arch/arm/dts/hwasin-gpmi-weim.dts \
    file://new-files/board/freescale/hwasin/hwasin.c \
    file://new-files/board/freescale/hwasin/imximage.cfg \
    file://new-files/board/freescale/hwasin/imximage_lpddr2.cfg \
    file://new-files/board/freescale/hwasin/Kconfig \
    file://new-files/board/freescale/hwasin/MAINTAINERS \
    file://new-files/board/freescale/hwasin/Makefile \
    file://new-files/board/freescale/hwasin/plugin.S \
    file://new-files/board/freescale/hwasin/README \
    file://new-files/configs/hwasin_defconfig \
    file://new-files/configs/hwasin_emmc_defconfig \
    file://new-files/include/configs/hwasin.h \
    file://0001-Fix-x86_64-linux-gnu-gcc-compilation-error.patch \
    file://0002-add-hwasin-supporting.patch \
"

do_copy_new_files() {
    cp -a ${WORKDIR}/new-files/* ${S}/
}

addtask copy_new_files after do_patch before do_configure
