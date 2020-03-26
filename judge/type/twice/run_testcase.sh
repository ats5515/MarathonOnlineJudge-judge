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
	echo $1 >> $ERR
	exit
}

throw_wrong_answer () {
	echo -n "WA" > $STATUS
	exit
}

./setup_cgroup.sh $ML

./generator ${SEED} > input1.txt || throw_internal_error "generator error"

state="AC"
TIMEOUT=$(($TL+1))


#encoder
SWITCH_CMD=$(./setup_sandbox.sh input1.txt main)

start_time1=$(date +%s%N)
sudo cgexec -g pids,cpuset,memory:judge $SWITCH_CMD sh -c "cd sand; timeout $TIMEOUT $RUN_CMD < input1.txt > output1.txt 2> stderr1.txt " || state="RE"
end_time1=$(date +%s%N)

./rm_sandbox.sh output1.txt stderr1.txt


time_elapsed1=$((($end_time1 - $start_time1)/1000000))

memory_used=$(cat '/sys/fs/cgroup/memory/judge/memory.max_usage_in_bytes')

cat stderr1.txt > $ERR
echo -n $time_elapsed1 > $TIME
echo -n $memory_used > $MEMORY

./mediator input1.txt < output1.txt > input2.txt 2>> $ERR|| throw_wrong_answer

#decoder
SWITCH_CMD=$(./setup_sandbox.sh input2.txt main)

start_time2=$(date +%s%N)
sudo cgexec -g pids,cpuset,memory:judge $SWITCH_CMD sh -c "cd sand; timeout $TIMEOUT $RUN_CMD < input2.txt > output2.txt 2> stderr2.txt " || state="RE"
end_time2=$(date +%s%N)

./rm_sandbox.sh output2.txt stderr2.txt

time_elapsed2=$((($end_time2 - $start_time2)/1000000))

time_elapsed=$(($time_elapsed1 + $time_elapsed2))

memory_used=$(cat '/sys/fs/cgroup/memory/judge/memory.max_usage_in_bytes')
cat stderr2.txt >> $ERR

$MAXBYTES=1024
if [ $(wc -c < $ERR) -gt $MAXBYTES ]; then
	truncate -s $MAXBYTES $ERR
fi


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
	./judge input1.txt output1.txt output2.txt > $SCORE 2>> $ERR || throw_wrong_answer
	echo -n "AC" > $STATUS
else
	echo -n "RE" > $STATUS
fi
