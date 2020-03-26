#!/bin/bash
cd `dirname $0`

#set -x

CHROOT_ENV="/home/ec2-user/tmp"
UPPERDIR="/home/ec2-user/upper"
WORKDIR="/home/ec2-user/workdir"
SAND=$CHROOT_ENV/sand
mkdir -p $CHROOT_ENV; sudo chmod -R 777 $CHROOT_ENV
mkdir -p $UPPERDIR; sudo chmod -R 777 $UPPERDIR
mkdir -p $WORKDIR; sudo chmod -R 777 $WORKDIR
mkdir -p $SAND; sudo chmod -R 777 $SAND

rm -r ./lower
mkdir lower
sudo chmod -R 777 lower

for arg in "$@"; do
  cp ./${arg} ${UPPERDIR}
done

mount_dirs=(
	'dev'
	'sys'
	'bin'
	'lib'
	'lib64'
	'usr'
	'etc'
	'opt'
	'var'
)

for dir in "${mount_dirs[@]}" ; do
	mkdir -p ${CHROOT_ENV}/${dir}
    sudo mount --bind -r /${dir} ${CHROOT_ENV}/${dir}
done

mkdir -p ${CHROOT_ENV}/tmp
sudo chmod -R 777 ${CHROOT_ENV}/tmp

sudo mount -t overlay overlay -o lowerdir=./lower,upperdir=${UPPERDIR},workdir=${WORKDIR} $SAND

echo -n "sudo chroot --userspec=judge-user:judge-user $CHROOT_ENV"
