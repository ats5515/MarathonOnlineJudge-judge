#!/bin/bash
set -x

sudo yum -y install python3
sudo pip3 install numpy scipy
python3 -V

python3 -c 'print("Hello")'