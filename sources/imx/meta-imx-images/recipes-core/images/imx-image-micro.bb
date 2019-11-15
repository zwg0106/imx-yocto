# BEGIN_INCLUDE_CORE_IMAGE_MINIMAL_BB
DESCRIPTION = "A small image just capable of allowing a device to boot."
IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_LINGUAS = " "
LICENSE = "MIT"
inherit core-image
IMAGE_ROOTFS_SIZE = "8192"

IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"
INITRAMFS_MAXSIZE = "300000"

# manufacturing stuff
IMAGE_INSTALL += "packagegroup-micro-base"

IMAGE_INSTALL += "kernel-modules"

do_decrease_image_size () {
    # delete /boot/zImage
    rm -f ${IMAGE_ROOTFS}/boot/zImage*

    # delete /etc/udev
    rm -rf ${IMAGE_ROOTFS}/${sysconfdir}/udev
}

do_gen_buildinfo () {
    local ts=$(echo ${IMAGE_NAME} | sed -e 's/.*-//')
    local timestamp="${ts:0:4}.${ts:4:2}.${ts:6:2} ${ts:8:2}:${ts:10:2}:${ts:12:2}"
    
    local bifile=${IMAGE_ROOTFS}/${sysconfdir}/build_info
    rm -f ${bifile}

    if [ ${machine_codename} ]; then
        local PLATFORM="${machine_codename}"
    else
        local PLATFORM="${MACHINE}"
    fi

    local BuildUser="root"
    if [ "Z${USER}" != "Z" ]; then
        BuildUser="${USER}"
    fi

    echo "====================="
    echo ${IMAGE_ROOTFS}
    echo "====================="
    echo "Branch=${EXA_TAG}"                    >> ${bifile}
    echo "Machine=${PLATFORM}"                  >> ${bifile}
    echo "ImageName=${IMAGE_NAME}"               >> ${bifile}
    echo "Timestamp=\"${timestamp}\""           >> ${bifile}
    echo "Description=\"${build_description}\"" >> ${bifile}
    echo "BuildUser=${BuildUser}"               >> ${bifile} 
}

addtask gen_buildinfo after do_decrease_image_size before do_image
addtask decrease_image_size after do_rootfs before do_image
