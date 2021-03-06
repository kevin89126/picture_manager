from commands import getstatusoutput
from utils import remove, get_files, is_diff, path_exists, \
    create_folder, move, path_join, copy
from constant import NOTIME_PATH, MOVE_PATH, SRC_PATH
from PIL import Image as img

class PicManager(object):

    def __init__(self, name=None):
	self.img = img
        self.path = SRC_PATH
        self.mv_path = MOVE_PATH
        self.notime_path = NOTIME_PATH
        self.files = get_files(self.path, name)
        self.dics = self.to_dic(self.files)

    def _get_time(self, _file):
        time = ''
	try:
	    time = self.img.open(_file)._getexif().get(36867, '')
	except Exception as err:
	    print 'No time: ', _file
	return time

    def _get_time_folder(self, time):
        if not time:
           return self.notime_path
        return time.split(' ')[0].strip().replace(':','/')

    def _seperate_one(self, _file):
        time = self._get_time(_file)
        folder = self._get_time_folder(time)
        fd_path = path_join([self.mv_path, folder, ''])
        if not path_exists(fd_path):
            create_folder(fd_path)
        print _file, fd_path
        print copy(_file, fd_path)

    def seperate(self):
	for _file in self.files:
            self._seperate_one(_file)

    def _get_name(self, _file):
        return _file.strip().split("/")[-1]

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


if __name__ == "__main__":
    path = '/USB_BACKUP/Picture'
    pm = PicManager(path)
    pm.handle_files()
