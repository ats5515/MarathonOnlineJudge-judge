#!/bin/bash
cd `dirname $0`

#set -x

CHROOT_ENV="/home/ec2-user/tmp"
UPPERDIR="/home/ec2-user/upper"

SAND=$CHROOT_ENV/sand

sudo pkill -KILL -u judge-user
sudo umount overlay
sudo umount -l ${CHROOT_ENV}/*
timeout 3 rm -rf ${CHROOT_ENV}

for arg in "$@"; do
  mv ${UPPERDIR}/${arg} ./
done

timeout 3 rm -rf ${UPPERDIR}