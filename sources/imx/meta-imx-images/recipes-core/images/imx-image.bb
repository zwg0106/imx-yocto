#
DESCRIPTION = "A small image just capable of allowing a device to boot."
IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_LINGUAS = " "
LICENSE = "MIT"
inherit core-image
IMAGE_ROOTFS_SIZE = "8192"

# Populate the sysroots with the makeself scripts
DEPENDS += "makeself-native imx-image-initramfs imx-image-ramdisk"

# gdb cross
DEPENDS += "gdb-cross-${TARGET_ARCH}"

# all stuff
IMAGE_INSTALL += "packagegroup-base"

# 3rd
IMAGE_INSTALL += "packagegroup-3rdparty"

# python
IMAGE_INSTALL += "packagegroup-python"

# Kernel
IMAGE_INSTALL += "kernel-modules"


imx_rootfs_postprocess() {
	#generate /etc/image_info
    local ts=$(echo ${IMAGE_NAME} | sed -e 's/.*-//')
    local timestamp="${ts:0:4}.${ts:4:2}.${ts:6:2} ${ts:8:2}:${ts:10:2}:${ts:12:2}"

    local bifile=${IMAGE_ROOTFS}/${sysconfdir}/image_info
    rm -f ${bifile}

    if [ ${machine_codename} ]; then
        local PLATFORM="${machine_codename}"
    else
        local PLATFORM="${MACHINE}"
    fi

    local BuildUser="None"
    if [ "Z${USER}" != "Z" ]; then
        BuildUser="${USER}"
    fi

    IMG_NAME=Package_imx6u_${PLATFORM}_${ts}_${BuildUser}.run

    echo "====================="
    echo ${IMAGE_ROOTFS}
    echo "====================="
    echo "Machine=${PLATFORM}"                  >> ${bifile}
    echo "ImageName=${IMG_NAME}"                >> ${bifile}
    echo "Timestamp=\"${timestamp}\""           >> ${bifile}
    echo "BuildUser=${BuildUser}"               >> ${bifile}

	#copy uboot, zImage, dtb and initramfs to /boot
	#uboot
	targetDir=${IMAGE_ROOTFS}/boot
	rm -rf ${targetDir}/*
	if [ -e ${DEPLOY_DIR_IMAGE}/u-boot-${MACHINE}.imx ]; then
		local src=$(readlink -f ${DEPLOY_DIR_IMAGE}/u-boot-${MACHINE}.imx)
		cp ${src} ${targetDir}
		ln -sf $(basename ${src}) ${targetDir}/u-boot-${MACHINE}.imx
	fi

	#kernel(zImage)
	if [ -e ${DEPLOY_DIR_IMAGE}/${KERNEL_IMAGETYPE}-${MACHINE}.bin ]; then
		local src=$(readlink -f ${DEPLOY_DIR_IMAGE}/${KERNEL_IMAGETYPE}-${MACHINE}.bin)
		cp ${src} ${targetDir}
		ln -sf $(basename ${src}) ${targetDir}/${KERNEL_IMAGETYPE}-${MACHINE}.bin
	fi

	#device tree
	for fn in ${KERNEL_DEVICETREE}; do
		fnName=$(basename $fn)
		fnBaseName=${fnName%\.*}	
		local src=$(readlink -f ${DEPLOY_DIR_IMAGE}/${KERNEL_IMAGETYPE}-${fnBaseName}.dtb)
		cp ${src} ${targetDir}
		ln -sf $(basename ${src}) ${targetDir}/${KERNEL_IMAGETYPE}-${fnBaseName}.dtb
	done

	# initramfs
	if [ -e ${DEPLOY_DIR_IMAGE}/imx-image-initramfs-${MACHINE}.${INITRAMFS_FSTYPES} ]; then
		local src=$(readlink -f ${DEPLOY_DIR_IMAGE}/imx-image-initramfs-${MACHINE}.${INITRAMFS_FSTYPES})
		cp ${src} ${targetDir}
		ln -sf $(basename ${src}) ${targetDir}/imx-image-initramfs-${MACHINE}.${INITRAMFS_FSTYPES}
	fi
}

ROOTFS_POSTPROCESS_COMMAND += "imx_rootfs_postprocess; "
