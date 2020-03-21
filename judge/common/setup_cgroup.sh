#!/bin/bash
cd `dirname $0`

set -x

ML=$1

sudo cgdelete pids,cpuset,memory:/judge
sudo cgcreate -g pids,cpuset,memory:/judge
sudo cgset -r pids.max=1000 judge
sudo cgset -r cpuset.cpus=0 judge
sudo cgset -r cpuset.mems=0 judge
sudo cgset -r memory.limit_in_bytes=$ML judge
sudo cgset -r memory.memsw.limit_in_bytes=$ML judge
