#!/bin/bash

myDir=$(readlink -e ${BASH_SOURCE[0]})
export toolsDir=$(dirname ${myDir})
export imxDir=$(dirname ${toolsDir})
export srcDir=$(dirname ${imxDir})
export projDir=$(dirname $srcDir)
export PATH=${toolsDir}:$PATH

export localConfFile="conf/local.conf"
export download_conf="download.conf"
export ssateCache=${projDir}/cache
export downloadDir=/home/$USER/download

SOURCE_MIRROR_URL="file:///$ssateCache"
init_conf=init.conf
imx_image="imx-image"

myName=$(basename $0 2>/dev/null)

function setupAlias()
{
    alias cd-sources="cd ${srcDir}"
    alias cd-tools="cd ${toolsDir}"
}

function updatePokyLocalConf() 
{
    cd ${yoctoBuildDirFull}
    local tmp=$(cat ${localConfFile} | grep "buildDescription")
    if [ -z "${tmp}" ]; then
        cp ${localConfFile} ${localConfFile}.tmp
        printf "\nbuildDescription = \"%s\" \n" "${defBuildDescription}" >> ${localConfFile}.tmp
        mv ${localConfFile}.tmp ${localConfFile}
    fi

    VER_PREREL=""
    local tmp=$(cat ${localConfFile} | grep "VER_PREREL")
    if [ -z "${tmp}" ]; then
        cp ${localConfFile} ${localConfFile}.tmp
        printf "\nVER_PREREL = \"%s\" \n" "${VER_PREREL}" >> ${localConfFile}.tmp
        mv ${localConfFile}.tmp ${localConfFile}
    else
        sed -i "s/VER_PREREL.*/VER_PREREL = \"${VER_PREREL}\"/" ${localConfFile}
    fi

    source ${toolsDir}/machines/${machine}.conf
    local tmp=$(cat ${localConfFile} | grep "machine_codename")
    if [ -z "${tmp}" ]; then
        cp ${localConfFile} ${localConfFile}.tmp
        printf "\nmachine_codename = \"%s\" \n" "${machine_codename}" >> ${localConfFile}.tmp
        mv ${localConfFile}.tmp ${localConfFile}
    else
        sed -i "s/machine_codename.*/machine_codename = \"${machine_codename}\"/" ${localConfFile}
    fi

    local tmp=$(cat ${localConfFile} | grep "SOURCE_MIRROR_URL")
    if [ -z "${tmp}" ]; then
        cp ${localConfFile} ${localConfFile}.tmp
        printf "\nSOURCE_MIRROR_URL ?= \"%s\" \n" $SOURCE_MIRROR_URL >> ${localConfFile}.tmp
        mv ${localConfFile}.tmp ${localConfFile}
    else
        sed -i "s|^SOURCE_MIRROR_URL.*|SOURCE_MIRROR_URL ?= \"${SOURCE_MIRROR_URL}\"|" ${localConfFile}
    fi
}

function envReInit()
{
    if [ -e ../${init_conf} ]; then
        cd ../
    fi
    if [ ! -e ${init_conf} ]; then
        echo "Failed to find a ${init_conf} in ${buildDir}."
        return 1
    else
        echo "Found a ${init_conf} at ${PWD}, reinitializing..."
    fi

    # Check and compare srcDir:
    dir_in_conf=$(grep srcDir ${init_conf} | tr '=' ' ' | tr -d '"' | awk '{print $2}')
    if [ ${dir_in_conf} != ${srcDir} ]; then
        echo "Aborting initialization. src dir(${dir_in_conf}) does not match in env (${srcDir})"
        return 1
    fi

    source ${init_conf}

    mv ${yoctoBuildDir}/conf/bblayers.conf ${yoctoBuildDir}/conf/bblayers.conf.bak
    export TEMPLATECONF="${imxMetadataDir}/meta-app/conf"
    rm -f ${yoctoBuildDir}/conf/templateconf.cfg
    source ${pokySrcDir}/oe-init-build-env "${yoctoBuildDir}"
    setupEnv
    return $?
}

function saveInitConf()
{
    echo "buildDir=\"${buildDir}\"" > ${buildDirFull}/${init_conf}
    echo "buildDirFull=\"${buildDirFull}\"" >> ${buildDirFull}/${init_conf}
    echo "yoctoBuildDir=\"${yoctoBuildDir}\"" >> ${buildDirFull}/${init_conf}
    echo "yoctoBuildDirFull=\"${yoctoBuildDirFull}\"" >> ${buildDirFull}/${init_conf}
    echo "machine=\"${machine}\"" >> ${buildDirFull}/${init_conf}
    echo "image=\"${image}\"" >> ${buildDirFull}/${init_conf}
    echo "downloadDir=\"$downloadDir\"" >> ${buildDirFull}/${init_conf}
    echo "pokySrcDir=\"${pokySrcDir}\"" >> ${buildDirFull}/${init_conf}
    echo "pokyMetadataDir=\"${pokyMetadataDir}\"" >> ${buildDirFull}/${init_conf}
    echo "imxMetadataDir=\"${imxMetadataDir}\"" >> ${buildDirFull}/${init_conf}
    echo "srcDir=\"${srcDir}\"" >> ${buildDirFull}/${init_conf}
    echo "buildDescription=\"${defBuildDescription}\"" >> ${buildDirFull}/${init_conf}
}


function setupPokyConfBblayers()
{
    source ${toolsDir}/machines/${machine}.conf
    local bblayerFile="conf/bblayers.conf"
    local metaFiles=${machine_bblayers}

    if [ ! -d conf ]; then
        echo "No conf dir here. PWD=$PWD"
        echo "Changing dir to yoctoBuildDirFull=${yoctoBuildDirFull}"
        cd ${yoctoBuildDirFull}
    fi

    for f in ${metaFiles}; do
        #echo `cat $bblayerFile`
        local fn="${srcDir}/${f}"
        #echo "bblayers: $fn"
        awk -v fName="$fn" '{ if ( $0 ~ /meta-yocto-bsp / ) {
               printf( "%s\n", $0);
               printf( "  %s \\\n",  fName );
             } else {
                   printf( "%s\n", $0);
             }
        }' ${bblayerFile}  > ${bblayerFile}.tmp

      mv ${bblayerFile}.tmp ${bblayerFile}
    done
}

function setupPokyConfLocal()
{
    cd ${yoctoBuildDirFull}
    #echo `cat ${localConfFile}`
    awk -v mach="$machine" -v dlDir="$downloadDir" \
    '{
    if ( $0 ~ /MACHINE \?\?\=/ ) {
        printf( "MACHINE = \"%s\"\n",  mach );
    } else if ( $0 ~ /#DL_DIR/ ) {
        printf( "DL_DIR = \"%s\"\n",  dlDir );
    } else {
        printf( "%s\n", $0);
    }
    }' ${localConfFile} > ${localConfFile}.tmp

    mv ${localConfFile}.tmp ${localConfFile}

    #echo `cat ${localConfFile}`
}

function setupPokyConfLocalExtra()
{
    cd ${yoctoBuildDirFull}
    cp ${localConfFile} ${localConfFile}.tmp

    sed -i s:%%SSTATE_DIR%%:\${TOPDIR}/sstate-cache: ${localConfFile}.tmp

    printf "\n####################  Additional Configurations  ####################\n" >> ${localConfFile}.tmp
    printf "\nSANITY_TESTED_DISTROS_append = \" Ubuntu \" \n" >> ${localConfFile}.tmp
    printf "\nSOURCE_MIRROR_URL ?= \"%s\" \n" "${SOURCE_MIRROR_URL}" >> ${localConfFile}.tmp
    printf "\ntoolsDir = \"%s\" \n" "${toolsDir}" >> ${localConfFile}.tmp

    mv ${localConfFile}.tmp ${localConfFile}
    
    #echo `cat ${localConfFile}`
}

function setupConf()
{
    echo "Setting up conf files"
    setupPokyConfBblayers
    setupPokyConfLocal
    setupPokyConfLocalExtra
}


function setupBldEnv()
{
    export machine
    export image
    export buildDir
    export srcDir
    export yoctoBuildDirFull 
    export imx_image

    # set alias
    alias cd-build="cd ${yoctoBuildDirFull}"
    alias cd-downloads="cd $downloadDir"
    alias cd-image="cd ${yoctoBuildDirFull}/tmp/deploy/images/${machine}"
    alias cd-rootfs="cd ${yoctoBuildDirFull}/tmp/work/${machine}*/${image}/*/rootfs"
    alias cd-initramfs-rootfs="cd ${yoctoBuildDirFull}/tmp/work/*/${image}-initramfs/*/rootfs"
    alias cd-ipk="cd ${yoctoBuildDirFull}/tmp/deploy/ipk"

    local logPath="tmp/work/*/*/*/temp/log.do_*"
    alias show-bld-errors="cd ${yoctoBuildDirFull}; find $logPath -type l | xargs grep '^ERROR:'"
    alias show-bld-warnings="cd ${yoctoBuildDirFull}; find $logPath -type l | xargs grep '^WARNING:'"
    alias show-bld-issues="cd ${yoctoBuildDirFull}; find $logPath -type l | xargs grep '^ERROR:\|^WARNING:'"

    local processor=`uname -p`

    source ${toolsDir}/machines/${machine}.conf
    local xpath=${yoctoBuildDirFull}/tmp/sysroots/${processor}-linux/usr/bin/${crosstools_path}
    local xprefix=${crosstools_prefix}

    alias x-addr2line="${xpath}/${xprefix}addr2line"
    alias x-ar="${xpath}/${xprefix}ar"
    alias x-as="${xpath}/${xprefix}as"
    alias x-c++="${xpath}/${xprefix}c++"
    alias x-c++filt="${xpath}/${xprefix}c++filt"
    alias x-cpp="${xpath}/${xprefix}cpp"
    alias x-g++="${xpath}/${xprefix}g++"
    alias x-gcc="${xpath}/${xprefix}gcc"
    alias x-gcc-4.7.2="${xpath}/${xprefix}gcc-4.7.2"
    alias x-gcc-ar="${xpath}/${xprefix}gcc-ar"
    alias x-gcc-nm="${xpath}/${xprefix}gcc-nm"
    alias x-gdb="${xpath}/${xprefix}gdb"
    alias x-ddd="ddd -debugger ${xpath}/${xprefix}gdb --gdb"
    alias x-ld="${xpath}/${xprefix}ld"
    alias x-nm="${xpath}/${xprefix}nm"
    alias x-objcopy="${xpath}/${xprefix}objcopy"
    alias x-objdump="${xpath}/${xprefix}objdump"
    alias x-readelf="${xpath}/${xprefix}readelf"
    alias x-strip="${xpath}/${xprefix}strip"	
}


function showInfo()
{
    saveDir=$PWD
    if [ ${yoctoBuildDirFull} ]; then
        cd ${yoctoBuildDirFull}
    elif [ -d ${srcDir} ]; then
        source ${srcDir}/${download_conf}
    else
        echo "Environment not yet set."
        return 1
    fi
    echo "Machine        : ${machine}"
    echo "Image          : ${image}"
    echo "buildDir       : ${buildDirFull}"
    echo "yoctoBuildDir  : ${yoctoBuildDirFull}"
    echo "srcDir         : ${srcDir}"

    cd ${saveDir}
}

function setupEnv()
{
	# update local conf
    updatePokyLocalConf	

	setupBldEnv
	
	showInfo
}

function createYoctoBuildDir()
{
    echo "Associating with srcDir: ${srcDir}"

    # save packages to ${downloadDir}
    # need approximately 10G disk space to save packages
    if [[ ! -d $(dirname $downloadDir) ]]; then
        mkdir -p $downloadDir
    fi

    # Set srcDir dependent variables
    sstateMirror="${srcDir}/sstate-cache"
    pokySrcDir="${srcDir}/poky"
    pokyMetadataDir="${srcDir}"
    imxMetadataDir="${srcDir}/imx"

    export yoctoBuildDir=${yoctoBuildDir:-"build"}

    export TEMPLATECONF="${imxMetadataDir}/meta-app/conf"
    source ${pokySrcDir}/oe-init-build-env "${yoctoBuildDir}"

    yoctoBuildDirFull=${PWD}

    if [ ${USER} ] && [ ${HOSTNAME} ]; then
        defBuildDescription="built by ${USER} with depot ${HOSTNAME}:${srcDir}"
    else
        defBuildDescription="built with depot ${srcDir}"
    fi

    saveInitConf
    setupConf
    setupEnv
    return 0
}

function createBuildDir()
{
	buildDir=$1
	echo "Creating directory ${buildDir}"

	if [ -d ${buildDir} ]; then
		echo "${buildDir} already exists. Using 'setup_build_env.sh -b ${buildDir}' to reinitialize your environment"
		return 1
	fi

	buildDirFull=$(readlink -m $buildDir)
	mkdir -p ${buildDirFull}
	if [ $? != 0 ]; then
		echo "Could not create ${buildDir}"
		return 1
	fi

	cd ${buildDir}
	createYoctoBuildDir
	if [ $? != 0 ]; then
		return 1
	fi
}

man="
  NAME 
    $myName
  SYNOPSIS
	$myName [-h] [-m <machine>] [-b <buildDir>]
  DESCRIPTION
	Utility to setup an project build environment.

  	Options:
		-h, --help         : show Help
		-m <machine>       : Machine name
		-b <buildDir>      : top level build directory name (one above yocto's build)

  EXAMPLES
	source setup_build_env.sh -m hwasin -b ${projDir}/srcBuild

  RETURN VALUES
	0 = no errors
	1 = an error occurred
"

function showUsage()
{
	echo "${man}"
}

# Special handling for -h only:
if [ "$1" == "-h" ]; then
    showUsage
    return 0
fi

machine=""
buildDir=""
buildDirFull=""
yoctoBuildDir=""
yoctoBuildDirFull=""

OPTIND=0
while getopts "hb:m:" options
do
	case $options in
		m ) machine=$OPTARG	
			;;

		b ) buildDir=$OPTARG
			;;

		* ) 
			echo "Unknown option: $OPTARG. See: setup_build_env.sh -h"
			return 1
			;;
	esac
done

shift $((OPTIND - 1))
if [ $1 ]; then
    echo "Unknown option \"$1\". See -h for help"
    return 1
fi

if [ -z ${machine} ]; then
    echo "Please specify a machine with -m"
    return 1
fi

if [ -z ${buildDir} ]; then
    echo "Please specify an imx_buildDir with -b."
    cd ${srcDir}
    return 1
fi

setupAlias

if [ ${buildDir} ] && [ -d ${buildDir} ]; then
    cd ${buildDir}
    envReInit
	if [ $? != 0 ]; then
		echo "Failed to reinitialize build environment."
		cd ${srcDir}
		return 1
	fi
	cd ${yoctoBuildDirFull}
	setupPokyConfBblayers
	echo "All Done."
    
    return 0
fi

createBuildDir ${buildDir}
if [ $? != 0 ]; then
    cd ${srcDir}
    return 1
fi
cd ${yoctoBuildDirFull}

# All done
echo "All Done."
