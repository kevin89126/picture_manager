# -*- coding: Big5 -*- 
from commands import getstatusoutput
from PIL import Image as img
from base import BaseManager
from constant import PIC_FORMAT

class PicManager(BaseManager):

    def __init__(self):
	self.img = img
	self.files = []
	self.input_size = 0

    def get_files(self, _files):
        for f in PIC_FORMAT:
            res = _files.get(f, [])
            if res:
                self.files = self.files + res

    def set_time(self, _file):
        #self.img.open(_file)
        pass

    def _get_time(self, _file):
        time = ''
	try:
	    time = self.img.open(_file)._getexif().get(36867, '')
	except Exception as err:
	    pass
	return time
