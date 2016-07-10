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
            res.append(_f)
    return res

def get_files(path, _format=['JPG']):
    res = []
    for root, dirs, files in os.walk(path):
        for _f in files:
	    _f_end = _f.split('.')[-1].strip()
	    if _f_end.upper() in _format:
	        res.append(path_join([root, _f]))
    print res
    return res


def move(src, target):
    cmd = "move '{0}' '{1}'".format(src, target)
    run_cmd(cmd)

def copy(src, target):
    cmd = "copy {0} {1}".format(src, target)
    print cmd
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
    return '\\'.join(paths)

def path_sep(path):
    return path.split("\\")

def path_replace(path):
    return path.replace(":", "\\")

def create_folder(path):
    print 'Create path: {0}'.format(path)
    os.makedirs(path)
