DESCRIPTION = "3rdparty packagegroup"

ALLOW_EMPTY_${PN} = "1"
PR = "r1"

PROVIDES = "${PACKAGES}"
PACKAGES = "\
        packagegroup-3rdparty \
        "

inherit packagegroup

RDEPENDS_packagegroup-3rdparty = "\
    bash                    \
    file                    \
    coreutils               \
    findutils               \
    tar                     \
    vim-tiny                \
    mmc-utils               \
    opentftp                \
    openssh                 \
    xinetd                  \
    netkit-telnet           \
    i2c-tools               \
    usbutils                \
    iputils                 \
    net-tools               \
    start-stop-daemon       \
    procps                  \
    init-ifupdown           \
    e2fsprogs               \
    e2fsprogs-e2fsck        \
    e2fsprogs-tune2fs       \
    e2fsprogs-mke2fs        \
	hostapd					\
	rfkill					\
	dhcp-client				\
	dhcp-server				\
	libuio					\
	libuio-tools			\
	memtester				\
	mtd-utils				\
	usbutils				\
	curl					\
	ethtool					\
	rsync					\
	tcpdump					\
	cronie					\
	daemonize				\
	expect					\
	lsof					\
	makeself				\
	bc				        \
        "
