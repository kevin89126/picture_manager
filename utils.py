import os
import time
from commands import getstatusoutput
import subprocess
import shutil
import logging
from Tkinter import *

logger = logging.getLogger('PicTool')
fh = logging.FileHandler('pictool.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

class UtilsManager(object):
    
    def get_row(self, root, bg=None):
        return Frame(root,bg=bg)

    def get_ent(self, row, state='readonly'):
        e = Entry(row)
        e.configure(state=state)
        return e

    def get_text(self, row, state='readonly'):
        e = Text(row)
        e.configure(state=state)
        return e

    def get_lab(self, row, width, text, anchor='w'):
        return Label(row, width=width, text=text, anchor=anchor)

    def get_button(self, row, text, command):
        return Button(row, text=text, command=command)

    def get_img_button(self, row, img, command):
        return Button(row, image=img, command=command)
    
    def get_scrollbar(self, root):
        row = self.get_row(root, bg='red')
        row.pack(side=TOP,fill=BOTH, expand=TRUE)
        vscrollbar = Scrollbar(row, orient=VERTICAL)
        hscrollbar = Scrollbar(row, orient=HORIZONTAL)
        vscrollbar.pack(fill=Y, side=RIGHT)
        hscrollbar.pack(fill=X, side=BOTTOM)
        listbox = Listbox(row)
        listbox.pack(side=LEFT, fill=BOTH, expand=TRUE)
        listbox.config(yscrollcommand=vscrollbar.set,
                       xscrollcommand=hscrollbar.set)
        vscrollbar.config(command=listbox.yview)
        hscrollbar.config(command=listbox.xview)
        return listbox


def run_cmd(cmd):
    subprocess.call(cmd, shell=True)

def remove(path):
    os.removedirs(path)

def get_time():
    return time.time()

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
    return res

def get_file_size(path):
    size = os.path.getsize(path)
    return size

def format_time(sec):
    return time.strftime('%H:%M:%S', time.gmtime(sec))

def move(src, target):
    cmd = "move '{0}' '{1}'".format(src, target)
    run_cmd(cmd)

def copy(src, target):
    shutil.copy(src, target)
    return 'Copy {0} to {1}'.format(src.encode('utf-8'), target.encode('utf-8'))

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

def get_folder(_f):
    return path_sep(_f)[-2]
    
def path_replace(path, cha):
    return path.replace(cha, "\\")

def create_folder(path):
    os.makedirs(path)
    return 'Create folder: {0}'.format(path.encode('utf-8'))
    
