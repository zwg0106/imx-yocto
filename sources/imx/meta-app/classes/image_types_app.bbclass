inherit image_types kernel-arch

# Create a self-extracting archive (.run) for the final image
oe_mkrun() {
    ROOTFS_IMAGE=$1
    bbnote "ROOTFS_IMAGE = ${ROOTFS_IMAGE}"
    bbnote "IMAGE_NAME = ${IMAGE_NAME}"

    # Grab the DATETIME from the end of IMAGE_NAME
    # This string manipulation doesn't work for some reason
    myDATETIME=$(echo ${IMAGE_NAME} | sed -e 's/.*-//')

    # Generate the self-extracting archive name:
    PKG_TYPE=Package_imx6u
    if [ ${machine_codename} ]; then
        PLATFORM="${machine_codename}"
    else
        bbwarn "Cannot find machine"
        PLATFORM="${MACHINE_ARCH}"
    fi
    # If EXA_TAG starts with V or R, then do not use the date/time stamp or the user:
    local BuildUser="None"
    if [ "Z${USER}" != "Z" ]; then
        BuildUser="${USER}"
    fi
    RUN_NAME=${PKG_TYPE}_${PLATFORM}_${myDATETIME}_${BuildUser}.run
    bbnote "Self-extracting package name = ${RUN_NAME}"
    SHORT_RUN_NAME=${PKG_TYPE}_${PLATFORM}.run
    ARCHIVE_DIR=${IMGDEPLOYDIR}/4makeself
    rm -fr ${ARCHIVE_DIR}
    mkdir -p ${ARCHIVE_DIR}
    bbnote "Linking ${ARCHIVE_DIR}/${ROOTFS_IMAGE} to ../${ROOTFS_IMAGE}"
    ln -s ../${ROOTFS_IMAGE} ${ARCHIVE_DIR}/${ROOTFS_IMAGE}
    startup_script=pkg-install.sh
    # Copy scripts from sysroot to Deploy Dir
    #cp ${STAGING_DATADIR}/pkg-install.sh/${startup_script} ${ARCHIVE_DIR}/
    cp ${COMPONENTS_DIR}/${TUNE_PKGARCH}/pkg-install/usr/share/pkg-install/${startup_script} ${ARCHIVE_DIR}/
    bifile=${IMAGE_ROOTFS}/${sysconfdir}/image_info
    if [ -e ${bifile} ]; then
        cp ${bifile} ${ARCHIVE_DIR}/
    else
        bbwarn "Missing ${bifile}. The .run file will be incomplete !!!"
    fi
    bbnote "Generating md5sum for ${IMGDEPLOYDIR}/${ROOTFS_IMAGE}"
    echo "rootfs=${ROOTFS_IMAGE}" >> ${ARCHIVE_DIR}/image_info
    echo -n "md5_rootfs=" >> ${ARCHIVE_DIR}/image_info
    md5sum ${IMGDEPLOYDIR}/${ROOTFS_IMAGE} | awk '{print $1}' >> ${ARCHIVE_DIR}/image_info

    # Generate md5 checksum for all files
    local curDir=$PWD
    bbnote "Generating md5sum for files under ${ARCHIVE_DIR}/"
    cd  ${ARCHIVE_DIR}
    find * -maxdepth 1 -type f -print0 | sed -e 's/\.\///g' | grep -zZv ".md5" | xargs -0 md5sum > ./flashFiles.md5
    cd ${curDir}

    bbwarn "current dir is ${curDir}"

    # Don't compress if it is squashfs image:
    if [[ "${ROOTFS_IMAGE}" =~ "squashfs" ]]; then
        compress="--nocomp"
    else
        compress=""
    fi

    #remove old .run 
    if [ "${RM_OLD_IMAGE}" ]; then
        bbnote "Delete old .run file under DEPLOY_DIR_IMAGE"
        local curDir=$PWD
        cd ${DEPLOY_DIR_IMAGE}
        find . -type f -name "*.run" -print | xargs rm -f
        cd ${curDir}
    fi

    label="package for platform ${PLATFORM}, imagename: ${RUN_NAME}"
    bbnote "Exec'ing: makeself.sh --follow ${compress} ${ARCHIVE_DIR} ${ROOTFS_IMAGE}.run \"${label}\" ./${startup_script}"
    makeself.sh --follow ${compress} ${ARCHIVE_DIR} ${ROOTFS_IMAGE}.run "${label}" ./${startup_script}
    cp ${ROOTFS_IMAGE}.run ${DEPLOY_DIR_IMAGE}

    # Create link with a simpler name
    ln -sf ${ROOTFS_IMAGE}.run ${DEPLOY_DIR_IMAGE}/${RUN_NAME}
    ln -sf ${RUN_NAME} ${DEPLOY_DIR_IMAGE}/${SHORT_RUN_NAME}

    # Add an MD5SUM inside the .run image - this doesn't affect the extractor verification, 
    # as long as we don't add a new line.
    # upgmgr will use the built-in MD5 info for integrity check after download, but before install.
    sum=$(md5sum ${DEPLOY_DIR_IMAGE}/${RUN_NAME} | awk '{print $1}')
    str="# This script was generated using Makeself 2.1.6"
    if (grep "$str" ${DEPLOY_DIR_IMAGE}/${RUN_NAME}) ; then
        sed -i "s/^${str}/${str} - MD5SUM $sum/" ${DEPLOY_DIR_IMAGE}/${RUN_NAME}
    else
        bbfatal "Cannot find the comment line to insert MD5SUM. Perhaps makeself got upgraded?"
    fi
}

COMPRESSIONTYPES += "run"

COMPRESS_DEPENDS_run = "makeself-native"
COMPRESS_CMD_run = "oe_mkrun ${IMAGE_NAME}.rootfs.${type}"

IMAGE_TYPES += "squashfs.run"
