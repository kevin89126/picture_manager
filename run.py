from Tkinter import *
from tkFileDialog import askdirectory
from seperate import seperate
import thread

class Action(object):

    def brows(self, entry):
        fd = askdirectory(parent=self.root)
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, fd)
        entry.configure(state='readonly')
        return fd

    def start(self):
        self.td_start = thread.start_new_thread(seperate, ())

    def cancel(self):
        self.td_start.exit()
       

class Utils(object):

    def get_row(self, root):
        return Frame(root)

    def get_ent(self, row):
        e = Entry(row)
        e.configure(state='readonly')
        return e

    def get_lab(self, row, width, text, anchor='w'):
        return Label(row, width=width, text=text, anchor=anchor)

    def get_button(self, row, text, command):
        return Button(row, text=text, command=command)
        
class Format(Action, Utils):

    def __init__(self, root):
        self.root = root
        self.fields = ['Input Foler', 'Output Folder']
        self.makeform(root, self.fields)
        
    def folder_format(self, root, field):
        row = self.get_row(root)
        lab = self.get_lab(row, width=11, text=field)
        ent = self.get_ent(row)
        button = self.get_button(row, text='Brows', command=lambda: self.brows(ent))
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=LEFT,fill=X)
        button.pack(side=LEFT)    
        
    def makeform(self, root, fields):
        entries = {}
        for field in fields:
            self.folder_format(root, field)
        button = self.get_button(root, text='Start', command=lambda: self.start())
        button.pack(side=LEFT, fill=X)
        button = self.get_button(root, text='Cancel', command=lambda: self.cancel())
        button.pack(side=LEFT, fill=X)

root = Tk()
ents = Format(root)
root.mainloop() 
