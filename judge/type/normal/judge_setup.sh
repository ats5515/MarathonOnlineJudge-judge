#!/bin/bash
cd `dirname $0`

set -x

sudo yum -y install gcc gcc-c++
g++ --version

g++ generator.cpp -o generator -std=c++11 -Ofast
g++ judge.cpp -o judge -std=c++11 -Ofast