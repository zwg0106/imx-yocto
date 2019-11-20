# "head" and "date" command in busybox lost its ability that cause some errors report during card bootup
# so move them form busybox to coreutils

FILES_${PN} += "${sbindir}"

bindir_progs = ""

base_bindir_progs = "date"
base_bindir_progs += "head"

do_install_append_class-target() {
    install -d ${D}${base_bindir}
    for i in ${base_bindir_progs}; do \
         if [ -f ${D}${bindir}/$i];then \
             mv ${D}${bindir}/$i ${D}${base_bindir}/$i.${BPN}; \
         fi
    done
    rm -fr ${D}/usr
    install -d ${D}${sbindir}
    mv ${D}${base_bindir}/date.coreutils ${D}${base_bindir}/date
    mv ${D}${base_bindir}/head.coreutils ${D}${base_bindir}/head 
}
