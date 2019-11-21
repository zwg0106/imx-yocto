LICENSE = "MIT"

IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"
inherit core-image

IMAGE_ROOTFS_SIZE = "8192"

IMAGE_INSTALL = ""
IMAGE_INSTALL += "initramfs-framework-imx-base"
IMAGE_INSTALL += "initramfs-imx-module-mdev"
IMAGE_INSTALL += "initramfs-imx-module-udev"
IMAGE_INSTALL += "initramfs-imx-module-e2fs"
IMAGE_INSTALL += "initramfs-imx-module-debug"
IMAGE_INSTALL += "initramfs-imx-module-mnt"
IMAGE_INSTALL += "busybox"
IMAGE_INSTALL += "base-passwd"
IMAGE_INSTALL += "procps"
IMAGE_INSTALL += "findutils"
IMAGE_INSTALL += "udev-extraconf"
IMAGE_INSTALL += "e2fsprogs-e2fsck"
