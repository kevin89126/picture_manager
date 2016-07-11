from Tkinter import *
from tkFileDialog import askdirectory
from seperate import seperate

class Action(object):

    def brows(self, entry):
        fd = askdirectory(parent=self.root)
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, fd)
        entry.configure(state='readonly')
        return fd

    def start(self):
        seperate()      

class BrowEntry(object):

    def get_entry(self, msg, row, col):
        self.e = Entry(self.root, width=50)
        self.e.insert(0, msg)
        self.e.configure(state='readonly')
        #self.e.grid(row=row, column=col)
        self.e.pack(pady=pady, padx = padx)
        return self.e
        
class BrowButton(Action, BrowEntry):

    def __init__(self, root):
        self.root = root
        input_e = self.get_entry('Select a input folder ...', 0,0)
        output_e = self.get_entry('Select a output folder ...', 1,0)
        self.input_b = Button(root, text='Brows', command=lambda: self.brows(input_e))
        #self.input_b.grid(row=0, column=0)
        self.input_b.pack(side=RIGHT, pady=20, padx = 20)
        
        self.output_b = Button(root, text='Brows', command=lambda: self.brows(output_e))
        self.output_b.pack(pady=20, padx = 20)
        self.start_b = Button(root, text='Start', command=lambda: self.start())
        self.start_b.pack(pady=20, padx = 20)

root = Tk()

root.geometry('600x400')
button = BrowButton(root)
root.mainloop() 
