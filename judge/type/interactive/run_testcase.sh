#!/bin/bash
cd `dirname $0`

set -x


IDX=$1
SEED=$2
TL=$3
ML=$4

RUN_CMD=$(./run_cmd.sh main)

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
	exit 0
}

throw_wrong_answer () {
	echo -n "WA" > $STATUS
	echo $1 > $ERR
	exit 0
}

./setup_cgroup.sh $ML

state="AC"
TIMEOUT=$(($TL+1))

SWITCH_CMD=$(./setup_sandbox.sh main judge)

SAND="/home/ec2-user/upper"

start_time=$(date +%s%N)
sudo cgexec -g pids,cpuset,memory:judge $SWITCH_CMD sh -c "cd sand; mkfifo mj jm; sh -c \"./judge ${SEED} score.txt < mj | cat > jm & \" ; timeout $TIMEOUT sh -c \"$RUN_CMD < jm 2> stderr.txt | cat > mj \" " || state="RE"
end_time=$(date +%s%N)

./rm_sandbox.sh stderr.txt score.txt
mv score.txt ${SCORE}

timeout 1 wait || state="WA"

if [ ! -s ${SCORE} ]; then
  state="WA"
fi


time_elapsed=$((($end_time - $start_time)/1000000))

memory_used=$(cat '/sys/fs/cgroup/memory/judge/memory.max_usage_in_bytes')

cat stderr.txt > $ERR

$MAXBYTES=1024
if [ $(wc -c < $ERR) -gt $MAXBYTES ]; then
	truncate -s $MAXBYTES $ERR
fi

echo -n $time_elapsed > $TIME
echo -n $memory_used > $MEMORY

ML_num=$(cat '/sys/fs/cgroup/memory/judge/memory.limit_in_bytes')

if [ $ML_num -le $memory_used ]; then
	echo -n "MLE" > $STATUS
	exit 0
fi

if [ $(($TL * 1000)) -le $time_elapsed ]; then
	echo -n "TLE" > $STATUS
	exit 0
fi


if [ $state = "AC" ]; then
	echo -n "AC" > $STATUS
else
	echo -n "RE" > $STATUS
fi
