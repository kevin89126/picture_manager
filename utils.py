import os
from commands import getstatusoutput
from subprocess import check_output


def run_cmd(cmd):
    return check_output(cmd, shell=True)

def remove(path):
    os.removedirs(path)

def _handle_files(files, _format=['JPG']):
    res = []
    for _f in files:
        _f = _f.split(' ')[-1].strip('\r')
	if not _f:
	    continue
	_f_end = _f.split('.')[-1].strip()
	if _f_end.upper() in _format:
	    print _f
            res.append(_f)
    return res

def get_files(path, name=None):
    cmd = "dir {0} /s".format(path)
    if name:
        cmd = cmd + " -name '{0}'".format(name)
    files = run_cmd(cmd).split('\n')
    return _handle_files(files)

def move(src, target):
    cmd = "move '{0}' '{1}'".format(src, target)
    run_cmd(cmd)

def copy(src, target):
    cmd = "copy /Y '{0}' '{1}'".format(src, target)
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
