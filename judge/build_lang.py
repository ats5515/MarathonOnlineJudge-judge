#!/usr/bin/env python
# coding: utf-8

import re
from operator import itemgetter
import os
import time
import sys
import subprocess
import json


def get_shell_stdout(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode("utf8")


args = sys.argv
langs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang")

lang_list = []
for lang in os.listdir(langs_dir):
    if os.path.isdir(os.path.join(langs_dir, lang)):
        lang_list.append(lang)
print(lang_list)

langs_json = {}

for lang in lang_list:
    try:
        base = os.path.join(langs_dir, lang)
        langs_json[lang]={}
        langs_json[lang]["compile"] = get_shell_stdout(
            "{} {} {}".format(os.path.join(base, "compile_cmd.sh"), "SRC", "OUT"))
        langs_json[lang]["run"] = get_shell_stdout(
            "{} {}".format(os.path.join(base, "run_cmd.sh"), "OUT"))
        langs_json[lang]["extension"] = get_shell_stdout(
            "{}".format(os.path.join(base, "get_extension.sh")))
        print("{} : configuration success".format(lang))
    except Exception as e:
        print("{} : configuration failed \n {}".format(lang, str(e)))


with open(os.path.join(langs_dir, 'langs.json'), "w") as f:
    json.dump(langs_json, f, indent=4)
