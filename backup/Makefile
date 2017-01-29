#
# Copyright (C) 2007 - Gerrit Beine <gerrit@beine-computer.de>
#
# $Revision: 1.10 $
# $Date: 2007/12/29 15:07:50 $
#

include	config

ECHO=		/bin/echo
MV=		/bin/mv
RM=		/bin/rm

VERSION=	0.1
CHOWN=		/usr/sbin/chown
CP=		/bin/cp
GPG=		/usr/local/bin/gpg
HOSTNAME=	/bin/hostname
MKDIR=		/bin/mkdir
PERL=		/usr/bin/perl
PW=		/usr/sbin/pw

#
# Global variables
#
BACKUPDIR?=	/backup
USERNAME?=	backup
USERID?=	1000
USERCOMMENT?=	"Backup user"
HOMEDIR?=	/home/backup
BIN=		${HOMEDIR}/bin
ETC=		${HOMEDIR}/etc

#
# Client variables
#
FTPSERVER?=	127.0.0.1
FTPUSER?=	ftpuser
FTPPASS?=	ftppass

#
# Server variables
#
LOCALHOST?=	localhost
LOCALPORT?=	1873
REMOTEHOST?=	localhost
REMOTEPORT?=	873
REMOTEUSER?=	localhost
JAILDIR?=	/data/jails
FQDN?=		localhost

#
# MySQL variables
#
MYSQLUSER?=	root
MYSQLPASSWORD?=	secret
MYSQLHOST?=	localhost
MYSQLDATADIR?=	/var/db/mysql

server: configure-server install-server

client: configure-client install-client

configure-server: save-config
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-host
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-jail
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-ldap
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-mysql
	@${PERL} -p -i.bak -e 's^%%BACKUP%%^${BACKUPDIR}^;' etc/global.conf
	@${PERL} -p -i.bak -e 's;%%HOST%%;${FQDN};' etc/host.conf
	@${PERL} -p -i.bak -e 's;%%JAILDIR%%;${JAILDIR};' etc/jail.conf
	@${PERL} -p -i.bak -e '\
		s^%%MYSQLHOST%%^${MYSQLHOST}^; \
		s^%%MYSQLUSER%%^${MYSQLUSER}^; \
		s^%%MYSQLPASSWORD%%^${MYSQLPASSWORD}^; \
		s^%%MYSQLDATADIR%%^${MYSQLDATADIR}^;' etc/mysql.conf
	@${PERL} -p -i.bak -e '\
		s^%%LOCALHOST%%^${LOCALHOST}^; \
		s^%%LOCALPORT%%^${LOCALPORT}^; \
		s^%%REMOTEHOST%%^${REMOTEHOST}^; \
		s^%%REMOTEPORT%%^${REMOTEPORT}^; \
		s^%%REMOTEUSER%%^${REMOTEUSER}^;' etc/rsync.conf

configure-client: save-config
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-archive
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-clean
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-decrypt
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-encrypt
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-extract
	@${PERL} -p -i.bak -e 's;%%ETC%%;${ETC};' bin/backup-upload
	@${PERL} -p -i.bak -e '\
		s^%%FTPSERVER%%^${FTPSERVER}^; \
		s^%%BACKUP%%^${BACKUPDIR}^;' etc/global.conf
	@${PERL} -p -i.bak -e '\
		s^%%FTPSERVER%%^${FTPSERVER}^; \
		s^%%FTPUSER%%^${FTPUSER}^; \
		s^%%FTPPASS%%^${FTPPASS}^;' netrc

install-server: install
	@${CP} bin/backup-host ${BIN}
	@${CP} bin/backup-jail ${BIN}
	@${CP} etc/global.conf ${ETC}
	@${CP} etc/host.conf ${ETC}
	@${CP} etc/host-excludes.conf ${ETC}
	@${CP} etc/jail.conf ${ETC}
	@${CP} etc/jail-excludes.conf ${ETC}
	@${CP} etc/rsync.conf ${ETC}
	@${CP} bin/backup-mysql ${BIN}
	@${CP} etc/mysql.conf ${ETC}
	@${CP} bin/backup-ldap ${BIN}
	@${CP} etc/ldap.conf ${ETC}
	@${CHOWN} -R ${USERNAME}:${USERNAME} ${HOMEDIR} || true

install-client: install
	@${CP} bin/backup-archive ${BIN}
	@${CP} bin/backup-extract ${BIN}
	@${CP} etc/archive.conf ${ETC}
	@${CP} bin/backup-clean ${BIN}
	@${CP} etc/clean.conf ${ETC}
	@${CP} etc/clean.ftpscript ${ETC}
	@${CP} bin/backup-encrypt ${BIN}
	@${CP} bin/backup-decrypt ${BIN}
	@${CP} etc/encrypt.conf ${ETC}
	@${CP} bin/backup-upload ${BIN}
	@${CP} etc/upload.conf ${ETC}
	@${CP} etc/upload.ftpscript ${ETC}
	@${CP} etc/global.conf ${ETC}
	@${CP} bin/backup-restore ${BIN}
	@${CP} netrc ${HOMEDIR}/.netrc
	@${CHOWN} -R ${USERNAME}:${USERNAME} ${HOMEDIR}
	@${CHOWN} -R ${USERNAME}:${USERNAME} ${HOMEDIR}/.netrc

install: adduser
	@${MKDIR} ${BIN} || true
	@${MKDIR} ${ETC} || true

adduser:
	@${PW} useradd ${USERNAME} -u ${USERID} -d ${HOMEDIR} -c ${USERCOMMENT} || true

clean:
	@${MV} bin/backup-archive.bak bin/backup-archive || true
	@${MV} bin/backup-clean.bak bin/backup-clean || true
	@${MV} bin/backup-decrypt.bak bin/backup-decrypt || true
	@${MV} bin/backup-encrypt.bak bin/backup-encrypt || true
	@${MV} bin/backup-extract.bak bin/backup-extract || true
	@${MV} bin/backup-host.bak bin/backup-host || true
	@${MV} bin/backup-jail.bak bin/backup-jail || true
	@${MV} bin/backup-ldap.bak bin/backup-ldap || true
	@${MV} bin/backup-mysql.bak bin/backup-mysql || true
	@${MV} bin/backup-upload.bak bin/backup-upload || true
	@${MV} etc/global.conf.bak etc/global.conf || true
	@${MV} etc/host.conf.bak etc/host.conf || true
	@${MV} etc/jail.conf.bak etc/jail.conf || true
	@${MV} etc/mysql.conf.bak etc/mysql.conf || true
	@${MV} etc/rsync.conf.bak etc/rsync.conf || true
	@${MV} netrc.bak netrc || true

save-config:
	@${RM} config
	@${ECHO} VERSION=${VERSION} >> config
	@${ECHO} CHOWN=${CHOWN} >> config
	@${ECHO} CP=${CP} >> config
	@${ECHO} GPG=${GPG} >> config
	@${ECHO} HOSTNAME=${HOSTNAME} >> config
	@${ECHO} MKDIR=${MKDIR} >> config
	@${ECHO} PERL=${PERL} >> config
	@${ECHO} PW=${PW} >> config
	@${ECHO} BACKUPDIR=${BACKUPDIR} >> config
	@${ECHO} USERNAME=${USERNAME} >> config
	@${ECHO} USERID=${USERID} >> config
	@${ECHO} USERCOMMENT=${USERCOMMENT} >> config
	@${ECHO} HOMEDIR=${HOMEDIR} >> config
	@${ECHO} BIN=${BIN} >> config
	@${ECHO} ETC=${ETC} >> config
	@${ECHO} FTPSERVER=${FTPSERVER} >> config
	@${ECHO} FTPUSER=${FTPUSER} >> config
	@${ECHO} FTPPASS=${FTPPASS} >> config
	@${ECHO} LOCALHOST=${LOCALHOST} >> config
	@${ECHO} LOCALPORT=${LOCALPORT} >> config
	@${ECHO} REMOTEHOST=${REMOTEHOST} >> config
	@${ECHO} REMOTEPORT=${REMOTEPORT} >> config
	@${ECHO} REMOTEUSER=${REMOTEUSER} >> config
	@${ECHO} JAILDIR=${JAILDIR} >> config
	@${ECHO} FQDN=${FQDN} >> config
	@${ECHO} MYSQLUSER=${MYSQLUSER} >> config
	@${ECHO} MYSQLPASSWORD=${MYSQLPASSWORD} >> config
	@${ECHO} MYSQLDATADIR=${MYSQLDATADIR} >> config
	@${ECHO} MYSQLHOST=${MYSQLHOST} >> config


