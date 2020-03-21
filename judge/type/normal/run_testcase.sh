#!/bin/bash
cd `dirname $0`

set -x

IDX=$1
SEED=$2
TL=$3
ML=$4

RUN_CMD=$(./run_cmd.sh main)


mkdir -p ./lower

mkdir -p ./result
STATUS="./result/status.txt"
ERR="./result/err.txt"
SCORE="./result/score.txt"
TIME="./result/time.txt"
MEMORY="./result/memory.txt"

echo "WJ" > $STATUS
>${ERR}
>${SCORE}
>${TIME}
>${MEMORY}

throw_internal_error () {
	echo -n "IE" > $STATUS
	echo $1 > $ERR
	exit
}

throw_wrong_answer () {
	echo -n "WA" > $STATUS
	echo $1 > $ERR
	exit
}

./setup_cgroup.sh $ML

./generator ${SEED} > input.txt || throw_internal_error "generator error"

state="AC"
TIMEOUT=$(($TL+1))

SWITCH_CMD=$(./setup_sandbox.sh input.txt main)

start_time=$(date +%s%N)
sudo cgexec -g pids,cpuset,memory:judge $SWITCH_CMD sh -c "cd sand; timeout $TIMEOUT $RUN_CMD < input.txt > output.txt 2> stderr.txt " || state="RE"
end_time=$(date +%s%N)

./rm_sandbox.sh output.txt stderr.txt

time_elapsed=$((($end_time - $start_time)/1000000))

memory_used=$(cat '/sys/fs/cgroup/memory/judge/memory.max_usage_in_bytes')

cat stderr.txt > $ERR

echo -n $time_elapsed > $TIME
echo -n $memory_used > $MEMORY

ML_num=$(cat '/sys/fs/cgroup/memory/judge/memory.limit_in_bytes')

if [ $ML_num -le $memory_used ]; then
	echo -n "MLE" > $STATUS
	exit
fi

if [ $(($TL * 1000)) -le $time_elapsed ]; then
	echo -n "TLE" > $STATUS
	exit
fi


if [ $state = "AC" ]; then
	./judge input.txt < output.txt > $SCORE 2> judgeerr.txt || throw_wrong_answer
	echo -n "AC" > $STATUS
else
	echo -n "RE" > $STATUS
fi
