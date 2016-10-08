from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset
from base import BaseManager
from constant import VEDIO_FORMAT


# Get metadata for video file
class VedioManager(BaseManager):

    def __init__(self):
        self.files = []
        self.input_size = 0

    def get_files(self, _files, _format):
        for f in _format:
            if f in VEDIO_FORMAT:
                self.files = self.files + _files.get(f, [])
        
    def _handel_raw_meta(self, text):
        res = {}
        for line in text:
            if not line[0] == '-':
                continue
            raw = line[2:].split(':', 1)
            if len(raw) == 2:
                res[raw[0].strip()] = raw[1].strip()
        return res
    
    def get_metadata(self, filename):
        filename, realname = unicodeFilename(filename), filename
        parser = createParser(filename, realname)
        if not parser:
            print "Unable to parse file"
            exit(1)
        try:
            metadata = extractMetadata(parser)
        except HachoirError, err:
            print "Metadata extraction error: %s" % unicode(err)
            metadata = None
        if not metadata:
            print "Unable to extract metadata"
            exit(1)
        text = metadata.exportPlaintext()
        res = self._handel_raw_meta(text)
        return res

    def _get_time(self, _file):
        time = ''
	try:
	    time = self.get_metadata(_file.encode('utf-8'))['Creation date']
	    time = time.split(' ')[0].replace('-', ':')
	except Exception as err:
	    pass
	return time

#mgr = VedioManager()
#pathname = "C:\Users\kevin\Desktop\DCIM\\100APPLE\IMG_3009.MOV"
#meta = mgr.get_metadata(pathname)
#print meta['Creation date']
