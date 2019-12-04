FILESEXTRAPATHS_prepend := "${THISDIR}/${P}:"

SRC_URI += " \
            file://banner.sh                    \
            file://10_persist                   \
            file://20_volatiles                 \
            file://umountfs                     \
            file://bootmisc.patch               \
            file://app-path.sh                  \
            "

RDEPENDS_${PN} += "bash"

do_unpack_append() {
    bb.build.exec_func('do_link_files', d)
}

do_link_files() {
    bbnote "WORKDIR=${WORKDIR}"
    bbnote "S=${S}"
    /usr/bin/rsync -av ${WORKDIR}/ ${S}/ --exclude ${BP}
}

do_install_append() {
    install -d ${D}${sysconfdir}/default/volatiles
    install -d ${D}${sysconfdir}/init.d
    install -m 0644 ${WORKDIR}/10_persist  ${D}${sysconfdir}/default/volatiles
    install -m 0644 ${WORKDIR}/20_volatiles  ${D}${sysconfdir}/default/volatiles
    install -m 0755 ${S}/populate-volatile.sh ${D}${sysconfdir}/init.d
    install -m 0755 ${S}/bootmisc.sh ${D}${sysconfdir}/init.d

    install -d ${D}/etc/profile.d
    install -m 0644 ${WORKDIR}/app-path.sh ${D}/etc/profile.d/app-path.sh
}

PR := "${PR}.3"
