SUMMARY = "3rd party packages"
DESCRIPTION = "3rd party packagegroup"

ALLOW_EMPTY_${PN} = "1"
PR = "r2"

inherit packagegroup

PROVIDES = "${PACKAGES}"
PACKAGES = "packagegroup-3rd-party  \
    	packagegroup-networking         \
    	packagegroup-ostools            \
    	packagegroup-platform           \
    	packagegroup-protocols          \
    	packagegroup-security           \
        ${@bb.utils.contains('MACHINE_ARCH', 'hwasin', 'packagegroup-hwasin', '',d)} \
"

RDEPENDS_packagegroup-3rd-party = "\
    	packagegroup-networking         \
    	packagegroup-ostools            \
    	packagegroup-platform           \
    	packagegroup-protocols          \
    	packagegroup-security           \
        ${@bb.utils.contains('MACHINE_ARCH', 'hwasin',     'packagegroup-hwasin', '',d)} \
"

SUMMARY_packagegroup-protocols = "Protocol packages"
DESCRIPTION_packagegroup-protocols = "Packages required for protocols"
RDEPENDS_packagegroup-protocols = "      \
    opentftp                        \
"

SUMMARY_packagegroup-security = "Security packages"
DESCRIPTION_packagegroup-security = "Packages required for security"
RDEPENDS_packagegroup-security = "      \
    openssh                         \
"

SUMMARY_packagegroup-platform = "Platform packages"
DESCRIPTION_packagegroup-platform = "Packages required for platform"
RDEPENDS_packagegroup-platform = "      \
    i2c-tools                       \
    usbutils                        \
"

SUMMARY_packagegroup-networking = "Networking packages"
DESCRIPTION_packagegroup-networking = "Packages required for networking"
RDEPENDS_packagegroup-networking = "      \
    curl                            \
    iputils                         \
    net-tools                       \
"

SUMMARY_packagegroup-ostools = "OS tools packages"
DESCRIPTION_packagegroup-ostools = "Packages required for ostools"
RDEPENDS_packagegroup-ostools = "      \
    bash                        \
    expect                      \
    file                        \
    findutils                   \
    tar                         \
    vim-tiny                    \
"


SUMMARY_packagegroup-hwasin = "hwasin specific"
DESCRIPTION_packagegroup-hwasin = "Packages required on the hwasin platform"
RDEPENDS_packagegroup-hwasin = "\
    mmc-utils \
"
