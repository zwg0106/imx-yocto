DESCRIPTION = "package install"
SECTION = "base"
DEPENDS = ""
LICENSE = "IMX"

RDEPENDS_${PN} = "bash"

PR = "r0"
# Major.Minor.Patch-prerelease
VER_MAJOR  = "1"
VER_MINOR  = "0"
VER_PATCH  = "0"

PV = "${VER_MAJOR}.${VER_MINOR}.${VER_PATCH}${VER_PREREL}"
SRCREV = "R${PV}"

inherit externalsrc
EXTERNALSRC = "${srcDir}/${PN}"

S = "${WORKDIR}/git/"

do_install_append () {
	install -d ${D}${bindir}/scripts
	install ${S}/pkg-install.sh	${D}${bindir}/scripts
}

sysroot_stage_all_append () {
    destDir="${SYSROOT_DESTDIR}/usr/share/${PN}"
    install -d $destDir
    install -m 0755 ${S}/pkg-install.sh $destDir
}
