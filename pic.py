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

    def get_files(self, _files, _format):
        for f in _format:
            if f in PIC_FORMAT:
                self.files = self.files + _files.get(f, [])

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
