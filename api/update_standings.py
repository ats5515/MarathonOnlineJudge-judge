#!/usr/bin/env python
# coding: utf-8

import os
import time
import sys
import subprocess
import json

args = sys.argv

problem_id = args[1]
user_id = args[2]

base_dir = subprocess.run(
    'basedir', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')

problems_path = subprocess.run(
    'problems_path', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')
problem_config = json.load(
    open(os.path.join(problems_path, problem_id, 'config.json')))

def get_shell_stdout(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf8")


def run_shell(cmds):
    try:
        for cmd in cmds:
            print('+ ' + cmd)
            subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(e)
        return False, str(e)
    return True, ""


def dump_json(obj, obj_path):
    full_path = os.path.join(base_dir, obj_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    json.dump(obj, open(full_path, "w"))
    run_shell(["sync_s3 {}".format(obj_path)])


pu_result = {}
pu_result_path = "cache/{}/{}/pu_result.json".format(problem_id, user_id)
try:
    pu_result = json.loads(
        get_shell_stdout("get_s3_file_cache {}".format(pu_result_path)))
except:
    print("no change needed")
    exit()


bestscore = 0.0
best_id = ""
first = True
for sub_id, res in pu_result.items():
    try:
        if res['status'] != 'AC':
            raise Exception
        score = float(res['score'])
        print(sub_id, score)
        if problem_config['objective'] == 'minimize':
            if first or bestscore > score:
                bestscore = score
                best_id = sub_id
        elif problem_config['objective'] == 'maximize':
            if first or bestscore < score:
                bestscore = score
                best_id = sub_id
        else:
            raise Exception
        first = False
    except:
        print('submission ' + str(sub_id) + ' has invalid result, just ignore')

best = {'score': bestscore, 'rank': 1000000007,
        'user': user_id, 'bestId': best_id}

best_path = "cache/{}/{}/best.json".format(problem_id, user_id)

dump_json(best, best_path)

standings = []
standings_path = "cache/{}/standings.json".format(problem_id)
try:
    standings = json.loads(
        get_shell_stdout("get_s3_file_cache {}".format(standings_path)))
except:
    print("new submission for problem {}".format(problem_id))

found = False
for i in range(len(standings)):
    if standings[i]['user'] == user_id:
        standings[i] = best
        found = True
if not found:
    standings.append(best)

standings = sorted(standings, key=lambda x: x['score'])

rank = 1
for value in standings:
    if value['rank'] != rank:
        value['rank'] = rank
        ranks = {}
        ranks_path = "user/{}/ranks.json".format(value['user'])
        try:
            ranks = json.loads(
                get_shell_stdout("get_s3_file_cache {}".format(ranks_path)))
        except:
            print("new valid submission by user {}".format(value['user']))
        ranks[problem_id] = value

        dump_json(ranks, ranks_path)

        run_shell(
            ["mkdir -p {}".format(os.path.join(base_dir, "user/update")),
             "touch {}".format(os.path.join(base_dir, "user/update", value['user']))])

    rank = rank + 1

print(standings)

dump_json(standings, standings_path)
