#!/bin/bash

# Create a run file from the currently running image on the target

source /etc/build_info

if [ $1 ]; then
    img=$1
else
    img=$(upgrader.sh -i | grep "Active image:" | awk '{print $3}')
fi

flash=$(upgrader.sh -i | grep "Current flash" | awk '{print $3}')

if [ ! ${img} ]; then
    echo "Cannot figure out which img I should use"
    exit 1
fi

if [ ! -d ${flash}/${img} ]; then
    echo "Cannot locate the img I should use (${flash}/${img})"
    exit 1
fi

WORKDIR=${flash}/tmp_install
rm -fr ${WORKDIR}
mkdir ${WORKDIR}
cd ${WORKDIR}
echo WORKDIR=${WORKDIR}

# What is my IP ?
myIF=$(route | grep default | awk '{print $8}')
if [ ! $myIF ]; then
    echo "Cannot determine my network interface"
else
    myIP=$(ip address show dev $myIF | grep "inet " | tr '/' ' ' | awk '{print $2}')
fi

if [ ! $myIP ]; then
    echo "Cannot determine my IP"
    myIP="0.0.0.0"
fi

ROOTFS_IMAGE=$(ls ${flash}/${img}/imx-image-*.squashfs)
source ${flash}/${img}/build_info
ORIG_RUN_NAME=${ImageName}
RUN_NAME=${HOSTNAME}_${myIP}_${ORIG_RUN_NAME}

echo ROOTFS_IMAGE=${ROOTFS_IMAGE}
echo ORIG_RUN_NAME=${ORIG_RUN_NAME}
echo RUN_NAME=${RUN_NAME}

ARCHIVE_DIR=${WORKDIR}/4makeself
mkdir ${ARCHIVE_DIR}
cp -rs ${flash}/${img}/* ${ARCHIVE_DIR}/
cp -r  /FLASH/persist ${ARCHIVE_DIR}/
# Remove this one, as it will get created during upgrade:
rm -f ${ARCHIVE_DIR}/image.rootfs

startup_script=upgrader.sh

# Invoke makeself:
# makeself.sh [args] archive_dir file_name label startup_script [script_args]

label="Full upgrade image for platform ${Platform}, imagename: ${RUN_NAME}"
echo "Exec'ing: makeself.sh --follow --nocomp ${ARCHIVE_DIR} ${RUN_NAME} \"${label}\" ./${startup_script}"
makeself.sh --follow --nocomp ${ARCHIVE_DIR} ${RUN_NAME} "${label}" ./${startup_script}
if [ $? == 0 ]; then
    echo "Look for ${RUN_NAME} in ${WORKDIR}"
    exit 0
else
    echo "Something went awry during makeself.sh"
    exit 1
fi
