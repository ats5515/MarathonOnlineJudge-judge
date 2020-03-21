#!/usr/bin/env python
# coding: utf-8

import os
import time
import sys
import subprocess
import json

args = sys.argv

judge_path = os.path.dirname(os.path.abspath(__file__))

submission_id = args[1]
submissions_path = subprocess.run(
    'submissions_path', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')
submission_path = submissions_path + '/' + submission_id

submission_info = json.load(open(submission_path + '/info.json'))
problem_id = submission_info['problemId']
user = submission_info['user']
lang = submission_info['lang']
problems_path = subprocess.run(
    'problems_path', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')


problem_config = json.load(
    open(problems_path + '/' + problem_id + '/config.json'))

judgetype = problem_config['judgetype']


def run_shell(cmds):
    try:
        for cmd in cmds:
            print('+ ' + cmd)
            subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(e)
        return False, str(e)
    return True, ""


cell_ids = subprocess.run(
    'get_sid_by_pid_uid {} {}'.format(problem_id, user), shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").strip()

cell_ids = json.loads(cell_ids)

cell_ids.append(submission_id)
cell_ids = list(set(cell_ids))

subprocess.run(
    "set_sid_by_pid_uid {} {} '{}'".format(
        problem_id, user, json.dumps(cell_ids)), shell=True)


bestscore = 0.0
valid = False

for i in cell_ids:
    try:
        result = json.load(
            open(submissions_path + '/' + str(i) + '/result.json'))
        if result['status'] != 'AC':
            raise Exception
        score = float(result['score'])
        print(str(i), score)
        if problem_config['objective'] == 'minimize':
            print("A", bestscore, score)
            if (not valid) or (bestscore > score):
                bestscore = score
            print("B", bestscore, score)
        elif problem_config['objective'] == 'maximize':
            if (not valid) or (bestscore < score):
                bestscore = score
        valid = True
    except:
        print('submission ' + str(i) + ' has invalid result, just ignore')

summary = {'score': '', 'rank': 1000000007, 'user': user}

if valid:
    summary['score'] = bestscore
else:
    exit()
    summary['score'] = ''

tmp = subprocess.run(
    'get_scorelist ' + problem_id, shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").strip()
score_list=[]

try:
    score_list = json.loads(tmp)
except:
    score_list=[]

found = False
for i in range(len(score_list)):
    if user == score_list[i]['user']:
        found = True
        score_list[i] = summary
if not found:
    score_list.append(summary)

print(score_list)

score_list = sorted(score_list, key=lambda x: x['score'])

print(len(score_list))
for i in range(len(score_list)):
    score_list[i]['rank'] = i+1
    subprocess.run(
        "set_summary {} {} '{}'".format(problem_id, score_list[i]["user"], json.dumps(score_list[i])), shell=True)

print(score_list)

subprocess.run(
        "set_scorelist {} '{}'".format(problem_id, json.dumps(score_list)), shell=True)
