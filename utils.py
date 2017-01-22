import os
import time
from commands import getstatusoutput
import subprocess
import shutil
import logging
import filecmp
from Tkinter import *
import os
from datetime import datetime
import platform
import unicodedata


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
        row = self.get_row(root)
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

    def check_box(self, row, text, v):
        return Checkbutton(row, text=text, variable=v)


def run_cmd(cmd):
    subprocess.call(cmd, shell=True)

def remove(path):
    os.removedirs(path)

def rename(src, des):
    os.rename(src, des)

def get_time():
    return time.time()

def _handle_files(files, _format=['MOV']):
    res = []
    for _f in files:
        _f = _f.split(' ')[-1].strip('\r')
	if not _f:
	    continue
	_f_end = _f.split('.')[-1].strip()
	if _f_end.upper() in _format:
            res.append(_f)
    return res

def get_files(path, depth=1):
    i = 0
    res = []
    for root, dirs, files in os.walk(path):
        i = i + 1
        if depth == i:
            return files
        res.extend(files)
        #print res
    return res

def get_folders(path, depth=1):
    i = 0
    res = []
    for root, dirs, files in os.walk(path):
        i = i + 1
        if depth == i:
            return dirs
        res.extend(dirs)
        #print res
    return res
        

def get_file_size(path):
    try:
        size = os.path.getsize(path)
        return size
    except:
        return 0

def format_time(sec):
    return time.strftime('%H:%M:%S', time.gmtime(sec))

def move(src, target):
    cmd = "move '{0}' '{1}'".format(src, target)
    run_cmd(cmd)

def copy(src, target, ignore_exist=False):
    if not ignore_exist or not path_exists(target):
        shutil.copy2(src, target)
        return 'Copy {0} to {1}'.format(
            src.encode('utf-8'), target.encode('utf-8'))
    try:
        if not ignore_exist or not path_exists(target):
            shutil.copy2(src, target)
            return 'Copy {0} to {1}'.format(
                src.encode('utf-8'), target.encode('utf-8'))
    #shutil.copystat(src, target)
    except:
        pass
    if platform.system() == "Windows":
        return 'Exist: {0}'.format(target.encode('utf-8'))
    else:
        return 'Exist: {0}'.format(target)

def is_diff(src, target):
    return filecmp.cmp(src, target)

def path_exists(path):
    return os.path.exists(path)
    
def get_name(path):
    return os.path.basename(path)

def path_join(paths):
    if platform.system() == "Windows":
        return os.path.join(*paths)

    # For mac
    res = []
    for s in paths:
        if isinstance(s, unicode):
            try:
                s = s.encode('utf-8')
            except:
                pass
        res.append(s)
    x = os.path.join(*res)
    return x


def get_folder(path):
    res = os.path.dirname(path)
    return get_name(res)


def create_folder(path):
    os.makedirs(path)
    if platform.system() == "Windows":
        return 'Create folder: {0}'.format(path.encode('utf-8'))
    return 'Create folder: {0}'.format(path)

    
def get_modify_date(path):
    time = os.path.getmtime(path)
    return datetime.fromtimestamp(int(time)).strftime('%Y:%m:%d')


def is_chinese(uchar):
    res = unicodedata.category(uchar)
    #print res
    if res == 'Lo':
        #print uchar
        return True
    else:
        return False

    
def collect_chinese(string):
    res = u''
    for i in string:
        if is_chinese(i):
            res = res + i
    #print res
    return res

def has_chinese(string):
    for i in string:
        if is_chinese(i):
            return True
    return False
