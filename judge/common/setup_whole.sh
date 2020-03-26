#!/bin/bash
cd `dirname $0`

set -x

chmod 755 ./*.sh
./judge_setup.sh
./lang_setup.sh
sudo useradd judge-user -u 990 -r -s /sbin/nologin -M
sudo yum install libcgroup libcgroup-tools -y
sudo service cgconfig start

./setup_sandbox.sh
./rm_sandbox.sh
sleep 5