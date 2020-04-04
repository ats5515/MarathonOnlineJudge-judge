#!/usr/bin/env python
# coding: utf-8

import os
import time
import sys
import subprocess
import json

args = sys.argv

base_dir = subprocess.run(
    'basedir', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')


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


def dump_json(obj, obj_path, rm=False):
    full_path = os.path.join(base_dir, obj_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    json.dump(obj, open(full_path, "w"))
    run_shell(["sync_s3 {}".format(obj_path)])
    if rm:
        run_shell(["rm -rf {}".format(full_path)])


score_table = {}
try:
    score_table = json.load(open(os.path.join(
        base_dir, "data", "score_table.json")))
except:
    print("file not found: score_table.json")
    exit()


def get_score(user):
    ranks = {}
    score = 0
    try:
        ranks = json.loads(
            get_shell_stdout("get_s3_file user/{}/ranks.json".format(user)))
        for problem, val in ranks.items():
            if str(val["rank"]) in score_table:
                score += score_table[str(val["rank"])]
    except:
        print("No valid submission found")

    return score


ranking = []
try:
    ranking = json.loads(
        get_shell_stdout("get_s3_file {}".format(
            os.path.join("data", "user_ranking.json"))))
except:
    print("First data")

update_user_list = []
update_dir = os.path.join(base_dir, "data", "update")
for username in os.listdir(update_dir):
    if os.path.isfile(os.path.join(update_dir, username)):
        update_user_list.append(username)

rev = {}
idx = 0
for data in ranking:
    rev[data['user']] = idx
    idx += 1

for user in update_user_list:
    if user in rev:
        idx = rev[user]
        ranking[idx]["score"] = get_score(user)
    else:
        ranking.append(
            {"rank": 100000007, "user": user, "score": get_score(user)}
        )

ranking = sorted(ranking, key=lambda x: -x["score"])

idx = 1
for data in ranking:
    data["rank"] = idx
    idx += 1

dump_json(ranking, os.path.join("data", "user_ranking.json"), rm=True)

rm_cmds = []
for user in update_user_list:
    rm_cmds.append("rm -f {}".format(os.path.join(update_dir, user)))

run_shell(rm_cmds)
