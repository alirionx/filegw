#!/bin/bash

if [[ -z "${src}" ]]; then
  src=/tmp
else
  inf="src isset"
fi

#echo $src
sed -i "s|{{src}}|$src|g" /etc/samba/smb.conf

/usr/sbin/smbd
. /venv/bin/activate && apachectl -D FOREGROUND

