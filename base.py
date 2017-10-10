# -*- coding: Big5 -*- 
from commands import getstatusoutput
from utils import remove, get_files, is_diff, path_exists, \
    create_folder, move, path_join, copy, get_name, get_folder, \
    get_file_size, get_modify_date
from constant import NOTIME_PATH
import platform


class BaseManager(object):

    
    def _create_time_folder(self, f):
        fd = self._get_time_folder(f)
        if not path_exists(fd):
            create_folder(fd)
        return fd

    def get_size(self):
        for f in self.files:
            self.input_size = self.input_size + get_file_size(f)
        return self.input_size

    def set_path(self, att_name, _path):
        setattr(self, att_name, _path)

    def set_time(self, _file):
        #self.img.open(_file)
        pass

    def get_file_num(self):
        return len(self.files)

    def _base_get_time_folder(self, _file):
        time = self._get_time(_file)
        if not time:
            time = get_modify_date(_file)
        if not time:
            print 'No time: ', _file
            return path_join([self.output_path, NOTIME_PATH, folder, ''])
        time_folder = time.split(' ')[0].strip().split(":")
        return path_join([self.output_path] + time_folder)

    def _get_time_folder(self, _file):
        folder = get_folder(_file)
        time_folder = self._base_get_time_folder(_file)
        return path_join([time_folder] + [folder, u''])
            
    def _seperate_one(self, _file):
        fd = self._get_time_folder(_file)
        return copy(_file, fd)

    def get_names(self, files):
        names = []
        for _file in files:
            name = get_name(_file)
            names.append(name)
        return names

    def to_dic(self):
        def init_dic(names):
            dic = {}
            for name in names:
                dic[name] = []
            return dic
        names = self.get_names(self.files)
        dic = init_dic(names)
        for _file in self.files:
            print _file
            if platform.system() == 'Windows':
                dic[get_name(_file).encode('utf-8')].append(_file.encode('utf-8'))
            else:
                dic[get_name(_file)].append(_file)      
        return dic

    def _find_dup(self):
        dics = self.to_dic()
        res = {}
        for key, value in dics.items():
            if len(value) > 1:
                res[key] = value
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

    def check_dup(self, f, exist_files):
        for _format, e_files in exist_files.iteritems():
            for e_f in e_files:
                if f in e_f:
                    return True
        return False
        

    def run(self):
        for f in self.files:
            base_time_folder = self._base_get_time_folder(f)
            exist_files = get_files(base_time_folder, _format=self._format)
            f_name = get_name(f)
            text = 'Ignore exist file: {0}'.format(f)
            if not self.check_dup(f_name, exist_files):
                fd = self._create_time_folder(f)
                tar = path_join([fd, f_name])
                text = copy(f, tar, ignore_exist=True)
            yield get_file_size(f), text
