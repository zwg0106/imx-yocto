DESCRIPTION = "ebf-demo"
SECTION = "base"
DEPENDS = ""
LICENSE = "IMX"

RDEPENDS_${PN} += "python3-core"

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
	install -d ${D}${bindir}/scripts/${PN}
	install -m 755 ${S}/scripts/*.py ${D}${bindir}/scripts/${PN}
	install -m 755 ${S}/scripts/*.json ${D}${bindir}/scripts/${PN}
}
