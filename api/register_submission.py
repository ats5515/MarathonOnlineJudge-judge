#!/usr/bin/env python
# coding: utf-8

import os
import time
import sys
import subprocess
import json

args = sys.argv

submission_id = args[1]

base_dir = subprocess.run(
    'basedir', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')
submissions_path = subprocess.run(
    'submissions_path', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')
submission_path = submissions_path + '/' + submission_id

submission_info = json.load(open(submission_path + '/info.json'))
problem_id = submission_info['problemId']
user_id = submission_info['user']
lang = submission_info['lang']
problems_path = subprocess.run(
    'problems_path', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')

problem_config = json.load(
    open(os.path.join(problems_path, problem_id, 'config.json')))


judgetype = problem_config['judgetype']


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


try:
    result = json.loads(get_shell_stdout(
        "get_s3_file_cache submissions/{}/result.json".format(submission_id)))
except:
    print('submission does not exist')
    exit()

pu_result = {}
pu_result_path = "cache/{}/{}/pu_result.json".format(problem_id, user_id)
try:
    pu_result = json.loads(
        get_shell_stdout("get_s3_file_cache {}".format(pu_result_path)))
except:
    print("new submissions by {} for problem {}".format(user_id, problem_id))

pu_result[submission_id] = result
dump_json(pu_result, pu_result_path)

u_result = {}
u_result_path = "user/{}/u_result.json".format(user_id)
try:
    u_result = json.loads(get_shell_stdout(
        "get_s3_file_cache {}".format(u_result_path)))
except:
    print("new submissions by {}".format(user_id))

u_result[submission_id] = result
dump_json(u_result, u_result_path)

p_result = {}
p_result_path = "cache/{}/p_result.json".format(problem_id)
try:
    p_result = json.loads(
        get_shell_stdout("get_s3_file {}".format(p_result_path)))
except:
    print("new submissions for problem {}".format(problem_id))

p_result[submission_id] = result
dump_json(p_result, p_result_path, True)

all_result = {}
all_result_path = "cache/all_result.json"
try:
    all_result = json.loads(
        get_shell_stdout("get_s3_file {}".format(all_result_path)))
except:
    print("new submissions")

all_result[submission_id] = result
dump_json(all_result, all_result_path, True)

run_shell(["update_standings {} {}".format(problem_id, user_id)])
