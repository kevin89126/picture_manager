import os
import time
import subprocess
import shutil
import filecmp
from Tkinter import *

    
def get_row(root, bg=None):
    return Frame(root,bg=bg)

def get_ent(row, state='readonly'):
    e = Entry(row)
    e.configure(state=state)
    return e

def get_text(row, state='readonly'):
    e = Text(row)
    e.configure(state=state)
    return e

def get_lab(row, width, text):
    return Label(row, width=width, text=text)

def get_button(row, text, command):
    return Button(row, text=text, command=command)

def get_img_button(row, img, command):
    return Button(row, image=img, command=command)
    
def get_scrollbar(root):
    row = get_row(root)
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

def check_box(row, text):
    var = IntVar()
    return Checkbutton(row, text=text, variable=var)


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
    shutil.copy2(src, target)
    return 'Copy {0} to {1}'.format(src.encode('utf-8'), target.encode('utf-8'))

def is_diff(src, target):
    return filecmp.cmp(src, target)

def path_exists(path):
    return os.path.exists(path)

def path_join(paths):
    return os.path.join(*paths)

def get_folder(path):
    return os.path.dirname(path)

def get_name(path):
    return os.path.basename(path)
    
def path_replace(path, cha):
    return path.replace(cha, "\\")

def create_folder(path):
    os.makedirs(path)
    return 'Create folder: {0}'.format(path.encode('utf-8'))
    
