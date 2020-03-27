#!/bin/bash
cd `dirname $0`

set -x

EXTENSION=$(./get_extension.sh)

COMPILE_CMD=$(./compile_cmd.sh main.${EXTENSION} main)

sh -c "$COMPILE_CMD"