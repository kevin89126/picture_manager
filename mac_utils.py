import os
from commands import getstatusoutput


def run_cmd(cmd):
    return getstatusoutput(cmd)

def remove(path):
    cmd = "rm -rf '{0}'".format(path)
    run_cmd(cmd)

def get_files(path, name=None):
    cmd = "find '{0}'".format(path)
    if name:
        cmd = cmd + " -name '{0}'".format(name)
    status, files = run_cmd(cmd)
    return files.split("\n")

def move(src, target):
    cmd = "mv '{0}' '{1}'".format(src, target)
    run_cmd(cmd)

def copy(src, target):
    cmd = "cp -n '{0}' '{1}'".format(src, target)
    return run_cmd(cmd)

def is_diff(src, target):
    cmd = "diff '{0}' '{1}'".format(src, target)
    status, res = run_cmd(cmd)
    if status == 0:
        return False
    else:
        return True

def path_exists(path):
    return os.path.exists(path)

def path_join(paths):
    return '/'.join(paths)

def create_folder(path):
    os.makedirs(path)
