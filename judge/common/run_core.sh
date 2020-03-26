#!/bin/bash
cd `dirname $0`

set -x

sudo unshare -fpnm --mount-proc su -l ec2-user -c "./run_testcase.sh $1 $2 $3 $4"