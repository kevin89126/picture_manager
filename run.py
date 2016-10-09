# -*- coding: Big5 -*- 
from Tkinter import *
import math
from tkFileDialog import askdirectory
import tkMessageBox
from pic import PicManager
from vedio import VedioManager
from utils import path_exists, copy, \
     create_folder, get_file_size, format_time, get_time, \
     logger, path_join, UtilsManager, get_files
from constant import TOTAL_FORMAT, PIC_FORMAT, VEDIO_FORMAT
import threading
import os
import webbrowser


INPUT_FOLDER = u'檔案資料夾'
OUTPUT_FOLDER = u'備份資料夾'
BROWS = u'瀏覽'
WIDTH = 315
HEIGHT = 380
PERID_TIME = 500
REMAIN_FORMAT = u'剩餘時間: {0}'
COPY_CANCEL = u'取消備份'
CANCEL = u'取消'
DONE = u'完成'
INIT_COPY_FILE = u'備份檔案準備中'
COUNT_FILE_SIZE = u'計算備份檔案大小'
NO_PICTURE = u'此資料下夾無符合照片'
WARNING = u'警告'
NO_DUPLICATE = u'此資料下夾無重複照片'
INFO = u'通知'
DEL_WINDOW_MSG = u'請先取消備份，再關閉程式'
START = u'開始'
DUPLICATE = u'尋找重複照片'
ARTHOR = u'作者'
EMAIL = u'信箱'
FACEBOOK = u'粉絲團'
VERSION = u'版本'
RELEASE_DATE = u'版本日期'
COPY_FILE = u'備份照片'
RULE = u'規則:'
TYPE = u'檔案類型:'

PWD = os.getcwd()

class StartThread(threading.Thread, UtilsManager):
    
    def __init__(self, listbox, time_bar, remain_can):
        threading.Thread.__init__(self)
        self.pic_mgr = PicManager()
        self.vedio_mgr = VedioManager()
        self.state = 'idel'
        self.listbox = listbox
        self.time_bar = time_bar
        self.remain_can = remain_can
        self.input_size = 0
        self.output_size = 0
        self.percent = 0
        self.next_bar = 1
        self.width = WIDTH
        self.replace = False
        self.str_time = get_time()

    def reset_time_bar(self):
        self.time_bar.delete('all')
        self.remain_can.delete('all')

    def set_path(self, input_path, output_path):
        self.pic_mgr.input_path = self.vedio_mgr.input_path = input_path
        self.pic_mgr.output_path = self.vedio_mgr.output_path = output_path

    def listbox_insert(self, msg):
        self.listbox.insert(END, msg)
        self.listbox.see(END)

    def get_remain_time(self):
        diff_time = get_time() - self.str_time
        rem_size = self.input_size - self.output_size
        if self.output_size == 0 or diff_time < 0:
            return 0
        res = (diff_time * 1.0/self.output_size) * rem_size
        return int(math.ceil(res))

    def precent(self):
        return self.percent

    #def show_time_bar(self):
    #    bar_num = int((self.output_size*10)/self.input_size) % 11
    #    while bar_num >= self.next_bar:
    #        x1 = 15 * (self.next_bar -1)
    #        x2 = x1 + 10
    #        self.time_bar.create_rectangle(x1, 0, x2, 20, fill="blue", outline = 'blue')
    #        self.time_bar.pack(side=LEFT,fill=X, expand=TRUE)
    #        self.next_bar = self.next_bar + 1

    def show_time_line(self):
        raw = self.output_size * 1.0 /self.input_size
        bar_line = int(raw * self.width)
        self.percent = str(int(raw * 100)) + "%"
        if not isinstance(self.next_bar, int) or not isinstance(bar_line, int) \
           or self.next_bar == bar_line:
            return
        self.time_bar.create_rectangle(self.next_bar, 0, bar_line, 20,
                                       fill="blue", outline = 'blue')
        self.remain_can.itemconfig(self.percent_id, text=self.percent)
        self.time_bar.pack(side=LEFT,fill=X, expand=TRUE)
        self.next_bar = bar_line
    
    def run(self):
        self.percent_id = self.remain_can.create_text(WIDTH-20, 10, text="0%", state=NORMAL)
        self.listbox_insert(INIT_COPY_FILE)        
        self.listbox_insert(COUNT_FILE_SIZE)
        self.input_size = self.pic_mgr.get_size() + self.vedio_mgr.get_size()
        pic_run = self.pic_mgr.run()
        vedio_run = self.vedio_mgr.run()
        for gen in [pic_run, vedio_run]:
            if not self.handel_run_gen(gen):
                return
        self.set_state('done')

    def handel_run_gen(self, run_gen):
        for f_size, text in run_gen:
            self.listbox_insert(text + '\n')
            self.output_size = f_size + self.output_size
            try:
                self.show_time_line()
            except Exception as err:
                pass
            if self.state == 'cancel':
                self.listbox_insert(COPY_CANCEL)
                self.set_state('cancel')
                return False
        return True
            

    def state(self):
        return self.state

    def set_state(self, state):
        self.state = state

class Action(object):

    def dup_info(self):
        if not self.check_format():
            return
        pic_mgr = PicManager()
        vedio_mgr = VedioManager()
        title = INFO
        files = get_files(self.input_path, _format=self.total_format)
        pic_mgr.get_files(files)
        p_dup = pic_mgr._find_dup()
        vedio_mgr.get_files(files)
        v_dup = vedio_mgr._find_dup()
        dup = {}
        dup.update(p_dup)
        dup.update(v_dup)
 
        if len(dup) == 0:
            self.show_msg(WARNING, NO_DUPLICATE)
            return
        max_len = 0
        t = Toplevel()
        t.wm_title(title)
        dup_farme = self.get_scrollbar(t)
        #t.lower()
        i = 1
        for key, value in dup.items():
            res = []
            for v in value:
                res.append(v)
            res = ', '.join(res)
            if max_len < len(res):
                max_len = len(res) + 10
            msg = '{2} {0}: {1}'.format(key, res, i)
            dup_farme.insert(END, msg)
            dup_farme.see(END)
            i = i + 1
        dup_farme.config(width=max_len)
        msg = DONE
        self.show_msg(title, msg)
        t.lift()
        
    def brows(self, entry, field):
        fd = askdirectory(parent=self.root)
        #fd = path_replace(fd, "/")
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, fd)
        entry.configure(state='readonly')
        if field == INPUT_FOLDER:
            self.input_path = fd
        elif field == OUTPUT_FOLDER:
            self.output_path = fd
        if self.input_path and self.output_path:
            self.start_bt.config(state=NORMAL)
        else:
            self.start_bt.config(state=DISABLED)

        if self.input_path:
            self.dup_bt.config(state=NORMAL)
        else:
            self.dup_bt.config(state=DISABLED)

    def check_format(self):
        self.total_format = []
        for fm in [self.v_mov, self.v_jpeg]:
            if fm['value'].get():
                self.total_format.append(fm['name'])
        if len(self.total_format) == 0:
            self.show_msg(WARNING, "Please select type first")
            return False
        return True
 
    def start(self):
        if self.start_t and self.start_t.state == 'running' or \
            self.check_format():
            return
        self.start_t = StartThread(self.listbox, self.time_bar, self.remain_can)
        self.start_t.set_path(self.input_path, self.output_path)

        files = get_files(self.input_path, _format=self.total_format)
        self.start_t.pic_mgr.get_files(files, PIC_FORMAT)
        self.start_t.vedio_mgr.get_files(files, VEDIO_FORMAT)
        if len(self.start_t.pic_mgr.files) == 0 and \
           len(self.start_t.vedio_mgr.files) == 0:
            self.show_msg(WARNING, NO_PICTURE)
            return
        self.start_t.set_state('running')
        self.start_t.reset_time_bar()
        #remain_time = format_time(0)
        #text = REMAIN_FORMAT.format(remain_time)
        #self.remain_time_id = self.remain_can.create_text(
        #    80, 10, text=text, state=NORMAL)
        self.start_t.start()
        self.cancel_bt.config(state=NORMAL)

    def periodical_check(self):
        self.check_start_t()
        self.check_start_bt()
        self.root.after(PERID_TIME, self.periodical_check)

    def show_msg(self, title, msg):
        tkMessageBox.showinfo(title, msg)

    def check_remain_time(self):
        if not self.start_t:
            return
        if not self.start_t.state == 'running':
            return
        
        cur_remain_time = self.start_t.get_remain_time()
        if not cur_remain_time == 0:
            self.remain_time = cur_remain_time
        cur_time = self.start_t.remain_time
        remain_time = format_time(cur_time)
        text = REMAIN_FORMAT.format(remain_time) 
        self.remain_can.itemconfig(self.remain_time_id, text=text)
        

    def check_start_t(self):
        
        if not self.start_t:
            self.cancel_bt.config(state=DISABLED)
            return
        if self.start_t.state == 'running':
            self.start_bt.config(state=DISABLED)
            self.dup_bt.config(state=DISABLED)
            #self.check_remain_time()

        if self.start_t.state == 'done':
            self.start_t = None
            self.cancel_bt.config(state=DISABLED)
            self.start_bt.config(state=NORMAL)
            self.dup_bt.config(state=NORMAL)
            self.show_msg(INFO, DONE)
        elif self.start_t.state == 'cancel':
            self.start_t = None
            self.cancel_bt.config(state=DISABLED)
            self.start_bt.config(state=NORMAL)
            self.dup_bt.config(state=NORMAL)
            self.show_msg(INFO, CANCEL)

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
        l = Label(r1, text=u'{0}: Kevin Chen'.format(ARTHOR))
        l.pack(side=LEFT)
        r2 = self.get_row(t)
        r2.pack(side=TOP, fill=BOTH)
        l = Label(r2, text=u'{0}: u3300035@gmail.com'.format(EMAIL))
        l.pack(side=LEFT)
        r3 = self.get_row(t)
        r3.pack(side=TOP, fill=BOTH)
        l = Label(r3, text=u'{0}: 1.6'.format(VERSION))
        l.pack(side=LEFT)
        r4 = self.get_row(t)
        r4.pack(side=TOP, fill=BOTH)
        l = Label(r4, text=u'{0}: 2016/10/9'.format(RELEASE_DATE))
        l.pack(side=LEFT)
        r5 = self.get_row(t)
        r5.pack(side=TOP, fill=BOTH)
        fb = 'https://www.facebook.com/Littletool-342467976084787/'
        l = Label(r5, text=u'{0}: '.format(FACEBOOK))
        l.pack(side=LEFT)
        l = Label(r5, text=fb, fg="blue", cursor="hand2")
        l.pack(side=LEFT)
        l.bind("<Button-1>", callback)


        
class Format(Action, UtilsManager):

    def __init__(self, root):
        self.root = root
        self.fields = [INPUT_FOLDER, OUTPUT_FOLDER]
        self.wideth = 250
        self.img = PhotoImage(file=path_join([".", "img", "info.gif"]))
        self.makeform(root, self.fields)
        self.input_path = None
        self.output_path = None
        self.start_t = None
        self.percent_id= None
        self.periodical_check()
        root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)
        self.total_format = []

    def wm_delete_window(self):
        if self.start_t and self.start_t.state == 'running':
            tkMessageBox.showerror(
            WARNING,
            DEL_WINDOW_MSG)
        else:
            self.root.destroy()

        
    def folder_format(self, root, field):
        row = self.get_row(root)
        lab = self.get_lab(row, width=11, text=field)
        ent = self.get_ent(row)
        button = self.get_button(row, text=BROWS, command=lambda: self.brows(ent, field))
        row.pack(side=TOP, expand=True,fill=X)
        lab.pack(side=LEFT)
        ent.pack(side=LEFT,fill=X, expand=TRUE)
        button.pack(side=LEFT)

    def rule_frame(self, row):
        rule_f = self.get_row(row)
        rule_f.pack(side=TOP, anchor='w', fill=BOTH)
        lab = self.get_lab(rule_f, 0, TYPE)
        lab.pack(side=LEFT)
        self.int_var_mov = IntVar()
        self.v_mov = {"name": "MOV", "value": self.int_var_mov}
        chk_mov = self.check_box(rule_f, 'MOV', self.int_var_mov)
        chk_mov.pack(side=LEFT)
        self.int_var_jpeg = IntVar()
        self.v_jpeg = {"name": "JPG", "value": self.int_var_jpeg}
        chk_jpeg = self.check_box(rule_f, 'JPG', self.int_var_jpeg)
        chk_jpeg.pack(side=LEFT)

        
    def makeform(self, root, fields):
        info_frame = self.get_row(root)
        info_frame.pack(side=TOP, expand=TRUE, fill=X)
        self.info_bt = self.get_img_button(
            info_frame, self.img, command=lambda: self.info())
        self.info_bt.pack(side=LEFT, fill=BOTH)
        
        for field in fields:
            self.folder_format(root, field)

        self.rule_frame(root)

        
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
            b_frame, text=START, command=lambda: self.start())
        self.start_bt.config(state=DISABLED)
        self.start_bt.pack(side=LEFT)
        self.cancel_bt = self.get_button(
            b_frame, text=CANCEL, command=lambda: self.cancel())
        self.cancel_bt.config(state=DISABLED)
        self.cancel_bt.pack(fill=BOTH, side=LEFT)
        self.dup_bt = self.get_button(
            b_frame, text=DUPLICATE, command=lambda: self.dup_info())
        self.dup_bt.config(state=DISABLED)
        self.dup_bt.pack(fill=BOTH, side=LEFT) 
        

root = Tk()
root.title('PicTool')
root.iconbitmap('.\img\\top_icon.ico')
root.geometry('{}x{}'.format(WIDTH, HEIGHT))
root.resizable(width=False, height=False)
ents = Format(root)
root.mainloop() 
