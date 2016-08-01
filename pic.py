# -*- coding: Big5 -*- 
from commands import getstatusoutput
from utils import remove, get_files, is_diff, path_exists, \
    create_folder, move, path_join, copy, path_sep, path_replace, \
    get_folder
from constant import NOTIME_PATH
from PIL import Image as img

class PicManager(object):

    def __init__(self):
        self.input_path = None
        self.output_path = None
	self.img = img
        self.notime_path = NOTIME_PATH

    def get_files(self):
        self.files = get_files(self.input_path)
        self.dics = self.to_dic(self.files)

    def set_path(self, att_name, _path):
        setattr(self, att_name, _path)

    def _get_time(self, _file):
        time = ''
	try:
	    time = self.img.open(_file)._getexif().get(36867, '')
	except Exception as err:
	    print 'No time: ', _file
	return time

    def get_file_num(self):
        return len(self.files)

    def _get_time_folder(self, _file):
        time = self._get_time(_file)
        if not time:
            return path_join([self.output_path, self.notime_path, ''])
        folder = get_folder(_file)
        time_folder = path_replace(time.split(' ')[0].strip(), ":")
        return path_join([self.output_path, time_folder, folder, ''])

            
    def _seperate_one(self, _file):
        fd = self._get_time_folder(_file)
        return copy(_file, fd)

    def _get_name(self, _file):
        return path_sep(_file)[-1]

    def get_names(self, files):
        names = []
        for _file in files:
            name = self._get_name(_file)
            names.append(name)
        return names

    def to_dic(self, files):
        def init_dic(names):
            dic = {}
            for name in names:
                dic[name] = []
            return dic
        names = self.get_names(files)
        dic = init_dic(names)
        for _file in files:
            dic[self._get_name(_file)].append(_file)
        return dic

    def _find_dup(self):
        res = []
        for key, value in self.dics.items():
            if len(value) > 1:
                dic = {}
                dic['name'] = key
                dic['paths'] = value
                res.append(dic)
        return res

    def _handle_file(self, vals, res=[]):
        src = vals.pop()
        _vals = vals
        df_vals = []
        res.append(src)
        for val in _vals:
            if is_diff(src, val):
                print 'Not diff: {0} , {1}'.format(src, val)
                df_vals.append(val)
                continue
            else:
                remove(val)
        if len(df_vals) > 1:
            self._handle_file(df_vals, res)
        else:
            res = res + df_vals
        return res

    def handle_files(self):
        dup = self._find_dup()
        for dic in dup:
            print '{0}: {1}'.format(dic['name'], dic['paths'])
            self._handle_file(dic['paths'])
