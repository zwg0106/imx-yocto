###############################################################################
#                                                                             #
#                  copyright 2013 by Calix, Inc.                              #
#                        Santa Barbara, CA                                    #
#                                                                             #
###############################################################################
#
# File:    Makefile
# Author:  Koral Ilgun
# Date:    Apr 30, 2013
# Purpose: Makefile for opentftp
###############################################################################

CWD    := $(shell basename ${PWD})
FILES  := opentftpd
OBJS   := $(FILES:=.o)
TARGET := opentftpd

override CFLAGS += -O3 -g -Werror -Wall

#
# The first (default) target MUST be 'build'.  It will
# be the entry point for building your application.
#
build: $(TARGET)

#
# Generic target to build all LIBTARGET application
#
$(TARGET): $(OBJS)
	$(CC) -l m -l pthread -o $(TARGET) $(OBJS)


#
# Generic target to build each '.c' resources
#
%.o: %.c
	$(CC) $(CFLAGS) $(INCLS) -o $@ -c $<

#
#
# The install target is used to install your
# application under ${DESTDIR}.  It SHOULD use
# the same path that your application is in under
# the cvs repository.  So if your application is
# under 'usr/occam/bin' in the cvs repository, your
# application should be installed in
#
# You should use the ${INSTALL} program to install
# you application.
#
INSTALL = install
install:
	${INSTALL} -d ${DESTDIR}${sbindir}
	${INSTALL} -m 0755 ${TARGET} ${DESTDIR}${sbindir}
	${INSTALL} -d ${DESTDIR}${sysconfdir}/init.d
	${INSTALL} -m 0755 rc.opentftp ${DESTDIR}${sysconfdir}/init.d/opentftp
	${INSTALL} -m 0644 opentftp.conf ${DESTDIR}${sysconfdir}

#
# Target is in charge of cleaning this module
#
clean:
	@rm -f *.o
	@rm -f $(TARGET)

distclean: clean

