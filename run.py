# -*- coding: Big5 -*- 
from Tkinter import *
import math
from tkFileDialog import askdirectory
import tkMessageBox
from pic import PicManager
from utils import path_replace, path_exists, copy, \
     create_folder, get_file_size, format_time, get_time, \
     path_join, get_row, get_ent, get_text, get_lab, \
     get_button, get_img_button, get_scrollbar, check_box
import threading
import os
import webbrowser


INPUT_FIELD = 'Input Folder'
OUTPUT_FIELD = 'Output Folder'
WIDTH = 700
HEIGHT = 500
PERID_TIME = 500
REMAIN_FORMAT = 'Remain Time: {0}'
PWD = os.getcwd()
RULE = u'規則:'
TYPE = u'檔案類型:'
INPUT = u'輸入資料夾'
OUTPUT = u'備份資料夾'
MTYPE = u'相機型號:'

class StartThread(threading.Thread):
    
    def __init__(self, listbox, time_bar, remain_can):
        threading.Thread.__init__(self)
        self.pic_mgr = PicManager()
        self.state = 'idel'
        self.listbox = listbox
        self.time_bar = time_bar
        self.remain_can = remain_can
        self.input_size = 0
        self.output_size = 0
        self.percent = 0
        self.remain_time = None
        self.next_bar = 1
        self.width = WIDTH
        self.replace = False

    def reset_time_bar(self):
        self.time_bar.delete('all')
        self.remain_can.delete('all')

    def set_path(self, input_path, output_path):
        self.pic_mgr.input_path = input_path
        self.pic_mgr.output_path = output_path

    def listbox_insert(self, msg):
        self.listbox.insert(END, msg)
        self.listbox.see(END)

    def get_remain_time(self, str_time):
        diff_time = get_time() - str_time
        rem_size = self.input_size - self.output_size
        if self.output_size == 0:
            return 0
        res = (diff_time * 1.0/self.output_size) * rem_size
        return int(math.ceil(res))
        
    def remain_time(self):
        return self.remain_time

    def precent(self):
        return self.percent

    def show_time_bar(self):
        bar_num = int((self.output_size*10)/self.input_size) % 11
        while bar_num >= self.next_bar:
            x1 = 15 * (self.next_bar -1)
            x2 = x1 + 10
            self.time_bar.create_rectangle(x1, 0, x2, 20, fill="blue", outline = 'blue')
            self.time_bar.pack(side=LEFT,fill=X, expand=TRUE)
            self.next_bar = self.next_bar + 1

    def show_time_line(self):
        raw = self.output_size * 1.0 /self.input_size
        bar_line = int(raw * self.width)
        self.percent = str(int(raw * 100)) + "%"
        if not isinstance(self.next_bar, int) or not isinstance(bar_line, int):
            return
        self.time_bar.create_rectangle(self.next_bar, 0, bar_line, 20,
                                       fill="blue", outline = 'blue')
        self.remain_can.itemconfig(self.percent_id, text=self.percent)
        self.time_bar.pack(side=LEFT,fill=X, expand=TRUE)
        self.next_bar = bar_line
    
    def run(self):
        self.percent_id = self.remain_can.create_text(WIDTH-20, 10, text="0%", state=NORMAL)
        self.listbox_insert('Init copy files')        

        self.listbox_insert('Counting file\'s size')
        for _file in self.pic_mgr.files:
            self.input_size = self.input_size + get_file_size(_file)
        str_time = get_time()
        for _file in self.pic_mgr.files:
            fd = self.create_time_folder(_file)
            f_size = get_file_size(_file)
            self.output_size = f_size + self.output_size
            self.copy_file(_file, fd)
            cur_remain_time = self.get_remain_time(str_time)
            if cur_remain_time + 1 < self.remain_time or \
               not self.remain_time:
                self.remain_time = cur_remain_time
            try:
                self.show_time_line()
            except Exception as err:
                pass
            if self.state == 'cancel':
                self.listbox_insert('Copy Cancel')
                self.set_state('cancel')
                return
        self.remain_time = 0
        self.set_state('done')

            
    def copy_file(self, _file, fd):
       text = copy(_file, fd)
       self.listbox_insert(text + '\n')

    def create_time_folder(self, _file):
        fd = self.pic_mgr._get_time_folder(_file)
        if not path_exists(fd):
            text = create_folder(fd)
            self.listbox.insert(END, text)
            self.listbox.see(END)
        return fd

    def state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def set_remain_time(self, remain_time):
        self.remain_time = remain_time

class Action(object):

    def dup_info(self):
        pic_mgr = PicManager()
        pic_mgr.input_path = self.input_path
        title = "Duplicate File"
        pic_mgr.get_files()
        if len(pic_mgr.files) == 0:
            self.show_msg('Duplication', 'No pictures!!')
            return

        max_len = 0
        dup = {}
        for key, value in pic_mgr.dics.items():
            if len(value) <= 1:
                continue
            dup[key] = value
        if not dup:
            self.show_msg('Duplication', 'No duplicate pictures!!')
            return
        t = Toplevel()
        t.wm_title(title)
        dup_farme = self.get_scrollbar(t)
        #t.lower()
        i = 1
        for key, value in dup.items():
            res = []
            for v in value:
                res.append(v.encode('utf-8'))
            res = ', '.join(res)
            if max_len < len(res):
                max_len = len(res) + 10
            msg = '{2} {0}: {1}'.format(key.encode('utf-8'), res, i)
            dup_farme.insert(END, msg)
            dup_farme.see(END)
            i = i + 1
        dup_farme.config(width=max_len)
        msg = 'Find duplicate file done.'
        self.show_msg(title, msg)
        t.lift()

        
    def brows(self, entry, field):
        fd = askdirectory(parent=self.root)
        fd = path_replace(fd, "/")
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, fd)
        entry.configure(state='readonly')
        if field == INPUT_FIELD:
            self.input_path = fd
        elif field == OUTPUT_FIELD:
            self.output_path = fd
        if self.input_path and self.output_path:
            self.start_bt.config(state=NORMAL)
        else:
            self.start_bt.config(state=DISABLED)

        if self.input_path:
            self.dup_bt.config(state=NORMAL)
        else:
            self.dup_bt.config(state=DISABLED)

    def start(self):
        if self.start_t and self.start_t.state == 'running':
            return
        self.start_t = StartThread(self.listbox, self.time_bar, self.remain_can)
        self.start_t.set_path(self.input_path, self.output_path)
        self.start_t.pic_mgr.get_files()
        if len(self.start_t.pic_mgr.files) == 0:
            self.show_msg('Empty Folder', 'No pictures!!')
            return
        self.start_t.set_state('running')
        self.start_t.reset_time_bar()
        remain_time = format_time(0)
        text = REMAIN_FORMAT.format(remain_time)
        self.remain_time_id = self.remain_can.create_text(
            80, 10, text=text, state=NORMAL)
        self.start_t.start()
        self.cancel_bt.config(state=NORMAL)

    def periodical_check(self):
        self.check_start_t()
        self.check_start_bt()
        self.root.after(PERID_TIME, self.periodical_check)

    def show_msg(self, title, msg):
        tkMessageBox.showinfo(title, msg)

    def check_remain_time(self):
        if not self.start_t.remain_time:
            return
        cur_time = self.start_t.remain_time
        remain_time = format_time(cur_time)
        text = REMAIN_FORMAT.format(remain_time) 
        self.remain_can.itemconfig(self.remain_time_id, text=text)
        #sec =  cur_time - PERID_TIME * 1.0 / 1000
        #if sec < 0:
        #    return
        #self.start_t.set_remain_time(sec)
        

    def check_start_t(self):
        
        if not self.start_t:
            self.cancel_bt.config(state=DISABLED)
            return
        if self.start_t.state == 'running':
            self.start_bt.config(state=DISABLED)
            self.check_remain_time()

        if self.start_t.state == 'done':
            self.start_t = None
            self.cancel_bt.config(state=DISABLED)
            self.start_bt.config(state=NORMAL)
            self.show_msg('Success', 'Copy Success')
        elif self.start_t.state == 'cancel':
            self.start_t = None
            self.cancel_bt.config(state=DISABLED)
            self.start_bt.config(state=NORMAL)
            self.show_msg('Cancel', 'Copy Cancel')

    def check_start_bt(self):
        if not self.input_path or not self.output_path:
            self.start_bt.config(state=DISABLED)
            
    def start_copy(self):
        self.pic_mgr.get_files()
        for _file in self.pic_mgr.files:
            fd = self.create_time_folder(_file)
            self.copy_file(_file, fd)
            
    def copy_file(self, _file, fd):
        text = copy(_file, fd)
        self.listbox.insert(END, text + '\n')
        self.listbox.see(END)

    def create_time_folder(self, _file):
        fd = self.pic_mgr._get_time_folder(_file)
        if not path_exists(fd):
            text = create_folder(fd)
            self.listbox.insert(END, text)
            self.listbox.see(END)
        return fd

    def cancel(self):
        if self.start_t and self.start_t.state == 'cancel':
            return
        self.start_t.set_state('cancel')

    def info(self):

        def callback(event):
            webbrowser.open_new(r"https://www.facebook.com/Littletool-342467976084787/")
        t = Toplevel()
        t.wm_title("Information")
        r1 = self.get_row(t)
        r1.pack(side=TOP, fill=BOTH)
        l = Label(r1, text='Author: Kevin Chen')
        l.pack(side=LEFT)
        r2 = self.get_row(t)
        r2.pack(side=TOP, fill=BOTH)
        l = Label(r2, text='Email: u3300035@gmail.com')
        l.pack(side=LEFT)
        r3 = self.get_row(t)
        r3.pack(side=TOP, fill=BOTH)
        l = Label(r3, text='Version: 1.4')
        l.pack(side=LEFT)
        r4 = self.get_row(t)
        r4.pack(side=TOP, fill=BOTH)
        l = Label(r4, text='Release Date: 2016/8/23')
        l.pack(side=LEFT)
        r5 = self.get_row(t)
        r5.pack(side=TOP, fill=BOTH)
        fb = 'https://www.facebook.com/Littletool-342467976084787/'
        l = Label(r5, text='Facebook: ')
        l.pack(side=LEFT)
        l = Label(r5, text=fb, fg="blue", cursor="hand2")
        l.pack(side=LEFT)
        l.bind("<Button-1>", callback)
        
    def wm_delete_window(self):
        if self.start_t and self.start_t.state == 'running':
            tkMessageBox.showerror(
            "Close windows",
            "Please cancel copy process first")
        else:
            self.root.destroy()
        
class Format(Action):

    def __init__(self, root):
        self.root = root
        self.fields = ['Input Folder', 'Output Folder']
        self.wideth = 250
        self.img = PhotoImage(file=".\img\info.gif")
        self.makeform(root, self.fields)
        self.input_path = None
        self.output_path = None
        self.start_t = None
        self.percent_id= None
        self.periodical_check()
        root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)

        
    def folder_format(self, root, field):
        row = self.get_row(root)
        lab = self.get_lab(row, width=11, text=field)
        ent = self.get_ent(row)
        button = self.get_button(row, text='Brows', command=lambda: self.brows(ent, field))
        row.pack(side=TOP, expand=True,fill=X)
        lab.pack(side=LEFT)
        ent.pack(side=LEFT,fill=X, expand=TRUE)
        button.pack(side=LEFT)

        
    def makeform(self, root, fields):
        info_frame = self.get_row(root)
        info_frame.pack(side=TOP, expand=TRUE, fill=X)
        self.info_bt = self.get_img_button(
            info_frame, self.img, command=lambda: self.info())
        self.info_bt.pack(side=LEFT, fill=BOTH)
        
        for field in fields:
            self.folder_format(root, field)
        self.listbox = self.get_scrollbar(self.root)
        time_frame = self.get_row(root, bg='red')
        time_frame.pack(side=TOP, expand=TRUE,fill=X)
        self.time_bar = Canvas(time_frame, width=WIDTH, height=20)

        for child in time_frame.winfo_children():
            child.configure(state='disable')
        self.time_bar.pack(side=LEFT,fill=X, expand=TRUE)

        remain_frame = self.get_row(root, bg='red')
        remain_frame.pack(side=TOP, expand=TRUE,fill=X)
        self.remain_can = Canvas(remain_frame, width=WIDTH, height=20)
        self.remain_can.pack(side=LEFT)

        b_frame = self.get_row(root)
        b_frame.pack(side=TOP)
        self.start_bt = self.get_button(
            b_frame, text='Start', command=lambda: self.start())
        self.start_bt.config(state=DISABLED)
        self.start_bt.pack(side=LEFT)
        self.cancel_bt = self.get_button(
            b_frame, text='Cancel', command=lambda: self.cancel())
        self.cancel_bt.config(state=DISABLED)
        self.cancel_bt.pack(fill=BOTH, side=LEFT)
        self.dup_bt = self.get_button(
            b_frame, text='Find Duplicate', command=lambda: self.dup_info())
        self.dup_bt.config(state=DISABLED)
        self.dup_bt.pack(fill=BOTH, side=LEFT)

class BaseWindows(Action):
    
    def __init__(self, root):
        self.root = root
        #self.fields = ['Input Folder', 'Output Folder']
        self.wideth = 250
        self.img = PhotoImage(file=".\img\info.gif")
        self.create_base_windows()
        self.input_path = None
        self.output_path = None
        self.start_t = None
        self.percent_id= None
        #self.periodical_check()
        root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)

    def folder_format(self, row, field):
        f_f = get_row(row, 'blue')
        f_f.pack(side=LEFT, expand=TRUE, fill=BOTH)
        lab = get_lab(f_f, width=11, text=field)
        lab.pack(side=TOP, anchor='nw')
        ent = get_ent(f_f)
        button = get_button(
            f_f, text='Brows', command=lambda: self.brows(ent, field))
        lab.pack(side=LEFT,  anchor='nw')
        ent.pack(side=LEFT,fill=X, expand=TRUE, anchor='nw')
        button.pack(side=LEFT,anchor='nw')
        
    def info_frame(self):
        info_frame = get_row(self.root)
        info_frame.pack(side=TOP, expand=TRUE, fill=X)
        self.info_bt = get_img_button(
            info_frame, self.img, command=lambda: self.info())
        self.info_bt.pack(side=LEFT, fill=BOTH)

    def content_frame(self):
        content = get_row(self.root, bg='red')
        content.pack(side=TOP, expand=TRUE, fill=BOTH)
        return content

    def rule_frame(self, row):
        rule_f = get_row(row, bg='black')
        rule_f.pack(side=LEFT, anchor='w', fill=BOTH)

        lab = get_lab(rule_f, 0, RULE).grid(row=0, sticky=W)
        lab = get_lab(rule_f, 0, TYPE).grid(row=1, sticky=W)
        chk_raw = check_box(rule_f, 'RAW').grid(row=2, sticky=W)
        chk_jpeg = check_box(rule_f, 'JPEG').grid(row=3, sticky=W)
        lab = get_lab(rule_f, 0, MTYPE).grid(row=4, sticky=W)


    def create_base_windows(self):
        # Top info frame
        self.info_frame()

        content_f = self.content_frame()
        self.rule_frame(content_f)
        self.folder_format(content_f, INPUT)
        self.folder_format(content_f, OUTPUT)
        
root = Tk()
root.title('PicTool')
root.iconbitmap('.\img\\top_icon.ico')
root.geometry('{}x{}'.format(WIDTH, HEIGHT))
root.resizable(width=False, height=False)
#ents = Format(root)
ents = BaseWindows(root)
root.mainloop() 
