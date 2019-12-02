#!/bin/bash

umask 022

set -x

mlog=/var/log/pkg-install.log

function mecho()
{
	echo -e "$*" | tee -a ${mlog}
}

function mexit() 
{
    if [ ${IMGMNT} ]; then
        if ( mount | grep "${IMGMNT} " > /dev/null ) ; then
            umount ${IMGMNT}
        fi
    fi
    exit $1
}

function setRecoverMedia()
{
	if [ "x${currentMedia}" == "x/dev/ram" ]; then
		#for ramdisk
		myDisk="mmcblk1"
		installMedia="/media/sda"
		newDev="/dev/${myDisk}"
		newDevBoot="${newDev}p1"
		newDevApp="${newDev}p2"
        currentApp=${installMedia}2
	else
		mecho "Can not find currentMedia: ${currentMedia}. Aborting operation."
		mexit 1
	fi
}

function unmountDrives() 
{
    if ( mount | grep "${newDevBoot}" > /dev/null ) ; then
        mecho "Unmounting ${newDevBoot}"
        umount ${newDevBoot}
        if [ $? != 0 ]; then
            mecho "ERROR: could not unmount ${newDevBoot}"
           	mexit 1 
        fi
    fi
    if ( mount | grep "${newDevApp}" > /dev/null ) ; then
        mecho "Unmounting ${newDevApp}"
        umount ${newDevApp}
        if [ $? != 0 ]; then
            mecho "ERROR: could not unmount ${newDevApp}"
            mexit 1
        fi
    fi
}


function partitionDisk()
{
mecho "Creating partitions..."

cat <<EOF | fdisk ${newDev}
d
1
d
n
p
1

+200M
t
83
n
p
2


t
2
83
w
EOF

sync; sync
mecho "Partitioning complete..."
}

function formatDisk()
{
    mecho "Formatting partitions..."

    mkfs.ext4 -F -q ${newDevBoot} -L ${part1LabelName}
    if [ $? != 0 ]; then
        mecho "mkfs.ext4 failed on ${newDevBoot}"
        mexit 1
    fi

    mkfs.ext4 -F -q ${newDevApp} -L ${part2LabelName}
    if [ $? != 0 ]; then
        mecho "mkfs.ext4 failed on ${newDevApp}"
        mexit 1
    fi

    mecho "Formatting complete..."
}


function setRootfsImage() 
{
    if [ ${rootfsImageType} ]; then
        return
    fi
    if [ ! ${rootfsImage} ]; then
        rootfsImage=$(ls *.rootfs.squashfs 2> /dev/null | head -n 1)
    fi
    if [ ! ${rootfsImage} ]; then
        mecho "Cannot find a rootfs image. Aborting installation."
        mexit 1
    fi
    rootfsImageBase=$(basename ${rootfsImage})
    rootfsImageFull=$(readlink -f ${rootfsImage})
    mecho "rootfsImageBase=${rootfsImageBase}"
    mecho "rootfsImageFull=${rootfsImageFull}"
    if [[ "$rootfsImageBase" =~ "squashfs" ]]; then
        rootfsImageType=squashfs
    else
        mecho "Unrecognized rootfs image. Aborting installation."
        mexit 1
    fi
    mecho "Rootfs image type is: ${rootfsImageType}."
    cd $(dirname ${rootfsImageFull})
}


function findCurrentPartitionAndMedia()
{
    if [ -z "${imgdev}" ]; then
        mecho "ERROR: Could not detect mounted media. This is how /proc/cmdline looks like:"
        cat /proc/cmdline
        mexit 1
    else
        currentMedia=$(echo -n ${imgdev} | tr -d "12")
        currentPartition="${imgdir}"
    fi

    # next partition
    if [ "x${currentPartition}" == "ximgx" ]; then
        nextPartition=imgy
    elif [ "x${currentPartition}" == "ximgy" ]; then
        nextPartition=imgx
    elif [ "x${currentMedia}" == "x/dev/ram" ]; then
        # for ramdisk
        currentPartition=imgx
        nextPartition=imgx
        return 0
    else
        mecho "ERROR: No ${currentMedia}, ${currentPartition}"
        mecho "ERROR: Cannot find current partition. Aborting installation."
        mexit 1
    fi

    currentBoot=${currentMedia}1
    currentApp=${currentMedia}2

   	installMedia="/media/sda"
}

function umountRootfsImage()
{
    umount ${IMGMNT}
    ret=$?
    if [ ${ret} != 0 ]; then
        mecho "Unmount fialed with rc=${ret},  Aborting upgrade."
    fi

    mecho "umount ROOTFS successfully"
}


function mountRootfsImage()
{
    export IMGMNT=/mnt/img

    if mount | grep /mnt/img; then
        mecho "ROOTFS already mounted at /mnt/img"
        return 0
    fi
    
	setRootfsImage

    mkdir -p ${IMGMNT}
    mecho "Mounting upgrade image ${rootfsImageBase} at ${IMGMNT}... "
    sleep 1
    mecho "Issuing: mount -o loop,ro -t ${rootfsImageType} ${rootfsImageFull} ${IMGMNT}"
	mount -o loop,ro -t ${rootfsImageType} ${rootfsImageFull} ${IMGMNT}
    if [ $? != 0 ]; then
        mecho "ERROR: Mount failed. Aborting installation."
        mexit 1
    fi

    mecho "finish to mount rootfs"
}

function copyBootImagesToMedia()
{
    media=$1
    olddir=${PWD}
    boot=${media}1
    partition=$2

    mecho "Removing all files under ${boot}/${partition}..."
    if [ -d ${boot}/${partition} ]; then
        rm -vrf ${boot}/${partition}
    fi
    sync;sync

    mkdir -p "${boot}/lost+found"
    mkdir -p ${boot}/${partition}

    # copy files to boot partition
    if [ ${IMGMNT} ]; then
        cp -af ${IMGMNT}/boot/* ${boot}/${partition}/
        
        #create link
        mecho "Creating boot links..."
        cd ${boot}/${partition}
        ln -sf $(readlink ${KERNEL_LINK_NAME})      zImage
        ln -sf $(readlink ${DTS_LINK_NAME})         zImage.dtb
        ln -sf $(readlink ${INITRAMFS_LINK_NAME})   initramfs.u-boot

        mecho "Removing unused links..."
        rm -f ${KERNEL_LINK_NAME}
        rm -f ${DTS_LINK_NAME}
        rm -f ${INITRAMFS_LINK_NAME}
    fi

    cd ${olddir}
}

function copyAppImagesToMedia()
{
    media=$1
    olddir=${PWD}
    app=${media}2
    partition=$2

    mecho "Removing all files under ${app}/${partition}..."
    if [ -d ${app}/${partition} ]; then
        rm -vrf ${app}/${partition}
    fi
	sync;sync
	mkdir -p "${app}/lost+found"
	mkdir -p ${app}/${partition}

	mecho "Copy files to ${app}/${partition}..."
	cp -r . ${app}/${partition}
	sync;sync
	
	# Creating links
    mecho "Creating app links..."
	cd ${app}/${partition}
	ln -sf ${rootfsImageBase} image.rootfs

	cd ${olddir}
}

function setNextBootPartition()
{
    media=$1
	part=$2
	olddir=${PWD}

	mecho "Creating boot partition links..."
	cd ${media}1
	ln -sf ${part} boot.imgdir
	
	sync;sync
	
	cd ${olddir}
}


function parseCmdline()
{
    cmd=`cat /proc/cmdline`

    for l in ${cmd};do
        case "${l}" in
            imgdev\=*)
                eval $l
                ;;
            imgdir\=*)
                eval $l
                ;;
            img\=*)
                eval $l
                ;;
            root\=*)
                eval $l
                # For ramdisk, force the imgdev to ${root}
                imgdev=${root}
                ;;
        esac
    done
    mecho "parseCmdline: imgdev=${imgdev}, imgdir=${imgdir}, img=${img}"
}



########################################################################
#                             START
########################################################################
myRealName=$(basename $0)
myFullName=$(readlink -f $0)

########################################################################
#                             HELP
########################################################################
man="
 NAME
    $myRealName

 SYNOPSIS
    $myRealName [-h] [-i] [--recover]

 DESCRIPTION
    This script installs package images into one or more partitions to emmc.
    For image upgrades:
       -r               	   : recover from ramdisk image.
       -h                      : show this Help
       -i                      : show Information about current partition status
 EXAMPLES
    (1) Install rootfs image in current dir to standby partition and make it primary:
        $myRealName

 RETURNS
    0 = no errors
    1 = something bad
"

function showUsage()
{
	echo "$man"
}

MACHINE=hwasin
installMedia=""
rootfsImage=""
reqRecover=0
IMGMNT=""
rootfsImageType=""
imageType=""
part1LabelName="boot"
part2LabelName="app"
UBOOT_LINK_NAME=u-boot-${MACHINE}.imx
KERNEL_LINK_NAME=zImage-${MACHINE}.bin
DTS_LINK_NAME=zImage-${MACHINE}-emmc.dtb
INITRAMFS_LINK_NAME=imx-image-initramfs-${MACHINE}.cpio.gz.u-boot

########################################################################
#                             OPTION
########################################################################


while getopts "rih" options
do
    case $options in
		r) reqRecover=1;;
		i) reqShowInfo=1;;
       	h) showUsage; OPTIND=0; exit 0;;
        *) showUsage; OPTIND=0; exit 0;;

	esac
done

parseCmdline

findCurrentPartitionAndMedia

if [ ${reqRecover} == 1 ]; then
    mecho "recover request"
    setRecoverMedia
    unmountDrives
    partitionDisk
    sleep 2 
    formatDisk

    mecho "Mounting emmc partitions"
    [ ! -d ${installMedia}1 ] && mkdir ${installMedia}1
    [ ! -d ${installMedia}2 ] && mkdir ${installMedia}2
    mount -v -t ext4 ${newDevBoot} ${installMedia}1
    mount -v -t ext4 ${newDevApp} ${installMedia}2
fi

mountRootfsImage

copyBootImagesToMedia ${installMedia} ${nextPartition}

umountRootfsImage

copyAppImagesToMedia ${installMedia} ${nextPartition}

if [ ${reqRecover} == 1 ]; then
	mecho "Deleting all files under ${installMedia}2/persist/..."
	rm -rf ${installMedia}2/persist/*
fi

setNextBootPartition ${installMedia} ${nextPartition}

mexit 0
