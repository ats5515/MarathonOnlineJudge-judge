#!/usr/bin/env python
# coding: utf-8

import boto3
import re
from operator import itemgetter
import os
import time
import sys
import subprocess
import json


args = sys.argv

judge_path = os.path.dirname(os.path.abspath(__file__))

submission_path = args[1]

submission_info = json.load(open(submission_path + '/info.json'))
problem_id = submission_info['problemId']
lang = submission_info['lang']
problems_path = subprocess.run(
    'problems_path', shell=True, stdout=subprocess.PIPE).stdout.decode("utf8").rstrip('\n')

problem_config = json.load(
    open(os.path.join(problems_path, problem_id, 'config.json')))

judgetype = problem_config['judgetype']

print("start judge process")
print("problem id:", problem_id)
print("submission:", submission_path)
print("judgetype:", judgetype)


def run_shell(cmds):
    try:
        for cmd in cmds:
            print('+ ' + cmd)
            subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(e)
        return False, str(e)
    return True, ""


def run_batch_test(seeds):
    ec2_client = boto3.client('ec2')

    secgroup_id = "sg-05f32bfe78686ac8d"
    keypair_name = "moj_key"
    instance_type = 't2.micro'
    image_id = 'ami-0af1df87db7b650f4'

    resp = ec2_client.run_instances(
        ImageId=image_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=keypair_name,
        InstanceInitiatedShutdownBehavior='terminate',
        NetworkInterfaces=[
            {
                'Groups': [secgroup_id],
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,
            }
        ],
    )

    instance_id = resp['Instances'][0]['InstanceId']
    print("Launched instance : {0}".format(instance_id))
    print("wating for acquiring Public IP Address...")

    ec2_resource = boto3.resource('ec2')
    judge_instance = ec2_resource.Instance(instance_id)

    judge_instance.wait_until_running()

    public_ip = judge_instance.public_ip_address
    print("got Public Ip:", public_ip)

    SCP = 'scp -i ~/.ssh/' + keypair_name + '.pem'
    RSYNC = 'rsync -e "ssh -i ~/.ssh/' + keypair_name + '.pem' + '"'
    DST = 'ec2-user@' + public_ip + ':~/'
    SSH = 'ssh -i ~/.ssh/' + keypair_name + '.pem ec2-user@' + public_ip

    for tryCount in range(100):
        statusOk = True
        try:
            print('try', tryCount)
            subprocess.run(SSH + ' ls -l', shell=True, check=True)
        except Exception as e:
            statusOk = False
            print(e)

        if statusOk:
            break
        time.sleep(1)

    # judge setup

    setup_cmds = []
    #setup_cmds.append(SSH + ' sudo yum -y update')
    src = judge_path + '/type/' + judgetype + '/*'
    setup_cmds.append(SCP + ' -r ' + src + ' ' + DST)
    src = judge_path + '/lang/' + lang + '/*'
    setup_cmds.append(SCP + ' -r ' + src + ' ' + DST)
    src = judge_path + '/common/*.sh'
    setup_cmds.append(SCP + ' -r {}/common/*.sh {}'.format(judge_path, DST))
    src = problems_path + '/' + problem_id + '/*'
    setup_cmds.append(SCP + ' -r ' + src + ' ' + DST)
    setup_cmds.append(SCP + ' -r ' + submission_path + '/* ' + DST)
    setup_cmds.append(SSH + ' ls')
    setup_cmds.append(SSH + ' chmod 755 ./setup_whole.sh')
    setup_cmds.append(SSH + ' ./setup_whole.sh')
    run_shell(setup_cmds)

    compile_result, err = run_shell([SSH + ' ./compile.sh 2> '
                                     + submission_path + '/CE.txt'])

    if(compile_result):
        # batch test
        run_shell(["rm {}/CE.txt".format(submission_path)])
        run_shell(['mkdir -p ' + submission_path + '/results'])
        for seed in seeds:
            try:
                subprocess.run(SSH + ' ./run_core.sh {} {} {} {}'.format(
                    str(seed["idx"]), str(seed["seed"]),
                    problem_config['timelimit'], problem_config['memorylimit']),
                    shell=True, check=True)
                subprocess.run(RSYNC + ' -r ' + DST + '/result/ ' + submission_path +
                               '/results/' + str(seed["idx"]) + '/', shell=True, check=True)
            except Exception as e:
                print(e)

    print(SSH)
    judge_instance.terminate()


seeds = []
for i in range(problem_config["num_testcases"]):
    seeds.append({'seed': i, 'idx': i})

print("seeds", seeds)
run_batch_test(seeds=seeds)
