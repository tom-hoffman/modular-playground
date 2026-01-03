#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
from pathlib import Path


# Arguments are:
# 1) the path to mpy-cross
# 2) the path to the destination drive, including its name, 
# e.g., ./make.py /home/hoffman/Desktop/mpy-cross /media/hoffman/EUCLID0

# We're assuming this is run from the root directory
# of the project, and not iterating through any sub-directories.

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def addM(name):
    return name[:-2] + 'm' + name[-2:]

excluded_files = ['make.py', 'code.py', 'boot.py']

print("Scanning current directory...")

if __name__ == "__main__":
    mpy_cross_path = sys.argv[1]
    remote_path = sys.argv[2]
    for local_name in files('.'):
        if (local_name[-3:] == '.py'):
            go_ahead = False
            local_time = os.path.getmtime(local_name)
            excluded = local_name in excluded_files
            if excluded:
                remote_new_name = local_name
            else:
                remote_new_name = addM(local_name)
            remote_full_path = remote_path + '/' + remote_new_name
            remote_path_object = Path(remote_full_path)
            remote_exists = remote_path_object.is_file()
            if remote_exists:
                remote_time = os.path.getmtime(remote_path + '/' + remote_new_name) # change ofc
                if local_time > remote_time:
                    go_ahead = True
            else:
                go_ahead = True
            if go_ahead and (not excluded):
                subprocess.run(mpy_cross_path + " " + local_name, shell=True)
                shutil.move(remote_new_name, remote_full_path)
                print("Created " + remote_full_path)
            elif go_ahead:
                shutil.copyfile(remote_new_name, remote_full_path)
                print("Copied " + remote_full_path)
