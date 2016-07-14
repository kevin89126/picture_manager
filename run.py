# -*- coding: Big5 -*- 
from Tkinter import *
from tkFileDialog import askdirectory
from pic import PicManager
from utils import path_replace, path_exists, copy, \
     create_folder
import thread

INPUT_FIELD = 'Input Folder'
OUTPUT_FIELD = 'Output Folder'

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
        
class Action(object):

    def brows(self, entry, field):
        fd = askdirectory(parent=self.root)
        fd = path_replace(fd, "/")
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, fd)
        entry.configure(state='readonly')
        if field == INPUT_FIELD:
            self.pic_mgr.set_path('input_path', fd)
        elif field == OUTPUT_FIELD:
            self.pic_mgr.set_path('output_path', fd)

    def start_copy(self):
        test_list = []
        for _file in self.pic_mgr.files:
            fd = self.pic_mgr._get_time_folder(_file)
            text = copy(_file, fd)
            #print text
            self.txt_ent.insert(END, text + '\n')
            
    def create_time_folder(self):
        for _file in self.pic_mgr.files:
            fd = self.pic_mgr._get_time_folder(_file)
            if not path_exists(fd):
                text = create_folder(fd)
                #print text
                self.txt_ent.insert(END, 'dddd')

    def start(self):
        self.pic_mgr.get_files()
        #self.td_start = thread.start_new_thread(self.create_time_folder, ())
        self.td_start = thread.start_new_thread(self.start_copy, ())

    def cancel(self):
        self.td_start.exit()
       

class Utils(object):

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

    def get_scrollbar(self):
        row = self.get_row(self.root)
        vscrollbar = Scrollbar(row, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        
class Format(Action, Utils):

    def __init__(self, root):
        self.pic_mgr = PicManager()
        self.root = root
        self.fields = ['Input Folder', 'Output Folder']
        self.makeform(root, self.fields)
        
    def folder_format(self, root, field):
        row = self.get_row(root)
        lab = self.get_lab(row, width=11, text=field)
        ent = self.get_ent(row)
        button = self.get_button(row, text='Brows', command=lambda: self.brows(ent, field))
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=LEFT,fill=X)
        button.pack(side=LEFT)    
        
    def makeform(self, root, fields):
        entries = {}

        for field in fields:
            self.folder_format(root, field)


        self.scr = VerticalScrolledFrame(root)
        self.scr.pack(side=RIGHT)
        self.txt_ent = self.get_text(self.scr.interior, state='normal')
        self.txt_ent.pack(side=LEFT,fill=X, expand=True)
        b_fram = self.get_row(root)
        b_fram.pack(side=BOTTOM)
        button = self.get_button(b_fram, text='Start', command=lambda: self.start())
        button.pack(side=LEFT, fill=X, expand=True) 
        button = self.get_button(b_fram, text='Cancel', command=lambda: self.cancel())
        button.pack(side=LEFT, fill=X, expand=True)


root = Tk()
ents = Format(root)
root.mainloop() 
