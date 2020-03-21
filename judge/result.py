#!/usr/bin/env python
# coding: utf-8

import re
from operator import itemgetter
import os
import time
import sys
import subprocess
import json

print('collect overall result')

args = sys.argv

judge_path = os.path.dirname(os.path.abspath(__file__))

submission_path = args[1]

submission_info = json.load(open(submission_path + '/info.json'))
problem_id = submission_info['problemId']
lang = submission_info['lang']
problems_path = subprocess.run(
    'problems_path', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')
problem_config = json.load(
    open(problems_path + '/' + problem_id + '/config.json'))
judgetype = problem_config['judgetype']


def run_shell(cmds):
    try:
        for cmd in cmds:
            subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(e)
        return False, str(e)
    return True, ""


results = {}
ret = {
    'status': '',
    'score': 0.0,
    'memory': 0,
    'time': 0,
    'err': '',
}
if os.path.isfile(submission_path+'/CE.txt'):
    ret['status'] = 'CE'
    with open(submission_path+'/CE.txt') as f:
        ret['err'] = f.read()
else:
    nt = problem_config["num_testcases"]
    for i in range(nt):
        path = submission_path + '/results/' + str(i)
        results[i] = {}
        try:
            results[i]['status'] = open(
                path + '/status.txt', 'r').read().rstrip('\n')
            results[i]['score'] = open(
                path + '/score.txt', 'r').read().rstrip('\n')
            results[i]['err'] = open(
                path + '/err.txt', 'r').read()
            results[i]['time'] = open(
                path + '/time.txt', 'r').read()
            results[i]['memory'] = open(
                path + '/memory.txt', 'r').read()

        except Exception as e:
            results[i]['status'] = 'IE'
            results[i]['err'] = str(e)

    for i in range(nt):
        if results[i]['status'] == '':
            results[i]['status'] = 'IE'
            results[i]['err'] += "\n"+'empty status'

    # status
    ret['status'] = 'AC'
    for i in range(nt):
        if results[i]['status'] != 'AC':
            ret['status'] = results[i]['status']
    
    for i in range(nt):
        try:
            results[i]['memory'] = int(results[i]['memory'])
            ret['memory'] = max(ret['memory'], results[i]['memory'])
        except Exception as e:
            print(str(e))
        try:
            results[i]['time'] = int(results[i]['time'])
            ret['time'] = max(ret['time'], results[i]['time'])
        except Exception as e:
            print(str(e))

    # score
    if ret['status'] == 'AC':
        try:
            for i in range(nt):
                results[i]['score'] = float(results[i]['score'])

            ret['score'] = 0.0
            if problem_config['aggregation'] == 'average':
                for i in range(nt):
                    if results[i]['status'] == 'AC':
                        ret['score'] += results[i]['score']
                    else:
                        ret['score'] += problem_config['default_score']
                ret['score'] /= nt
            else:
                assert False, 'unknown aggregation method'
        except Exception as e:
            results[i]['status'] = 'IE'
            ret['status'] = 'IE'
            ret['err'] += 'testcase' + str(i) + '\n' + str(e)


with open(submission_path+'/results.json', 'w') as f:
    json.dump(results, f, indent=4)

with open(submission_path+'/result.json', 'w') as f:
    json.dump(ret, f, indent=4)


print(results)
print(ret)
