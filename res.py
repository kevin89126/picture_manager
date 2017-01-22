#!/usr/bin/python
# -*- coding: UTF-8 -*-
from utils import get_files, get_folders, copy, rename, create_folder, \
     path_exists, has_chinese, collect_chinese
import re
import json

class HosongManager(object):

    def __init__(self):
        self.path = u"C:\\Users\\Kevin\\Desktop\\new_tree"
        #self.path = u"D:\\test"
        self.target = "D:\\new_tree"

    def rm_chinese(self):
        fds = get_folders(self.path)
        for fd in fds:
            path = '\\'.join([self.path, fd])
            print path
            target_path = '\\'.join([self.path, fd.split()[0]])
            print target_path
            rename(path, target_path)

    def _check_chinese_folders(self, fd, path):
        for src in FOLDER_MAP:
            _path = '\\'.join([path, fd])
            if re.search(src, fd):
                msg = _path.strip(self.path)
                print msg
                f.writelines([msg.encode('utf-8'), '\n'])
                tp = '\\'.join([path, FOLDER_MAP[src]])
                rename(_path, tp)
        return _path

    def change_folder_chinese(
            self, f, path=None):
        path = path or self.path
        fds = get_folders(path, depth=1)
        for fd in fds:
            _path = self._check_chinese_folders(fd, path)
            self.change_folder_chinese(f, _path)
        return

    def _check_new_folders(self, fd, path):
        _path = '\\'.join([path, fd])
        if re.search('001 Drawing', fd):
            for src in FOLDER_MAP:
                tp = '\\'.join([path, FOLDER_MAP[src]])
                if not path_exists(tp):
                    print 'Create folder: {0}'.format(tp)
                    create_folder(tp)
        return _path
                    
    def create_new_folder(self, f, path=None):
        path = path or self.path
        fds = get_folders(path, depth=1)
        for fd in fds:
            _path = self._check_new_folders(fd, path)
            self.create_new_folder(f, _path)
        return    

    def make_new_folder(
            self, f, src, path=None):
        path = path or self.path
        res = {}
        fds = get_folders(path, depth=1)
        for fd in fds:
            _path = '\\'.join([path, fd])
            #print _path
            if re.search(src, fd):
                fs = get_files(_path)
                for _f in fs:
                    if not re.search('^._', _f) and _f.endswith('.pdf'):
                       #and re.search('.*]A0[0-9]', _f):
                        print _f.strip('.pdf')
                        if res.has_key(_path):
                           res[_path].append(_f.strip('.pdf'))
                        else:
                            res[_path] = [_f.strip('.pdf')]
            _res = self.make_new_folder(f, src, _path)
            res.update(_res)
        return res
        

    def run(self):
        res = get_files(self.path, _format=['PDF'])
        for _f in res['PDF']:
            if u'舊圖檔' in _f or '._' in _f:
                continue
            if u'001  成品圖' in _f:
                #print _f
                b_num = _f.rindex('A')
                index = _f.strip('.pdf')[b_num:b_num+8]
                if not index.strip('A').isdigit():
                    continue
                print index
                #break

def dup(res):
    for k, v in res.iteritems():
        if len(v) > 1:
            print k, v

            
def check_all(res, num=1):
    for k, vs in res.iteritems():
        find = False
        if not len(vs) == num:
            continue
        
        for v in vs:
            if re.search(u'.*A.*', v):
                find = True
                #print v
                break
            elif re.search(u'.*B.*', v):
                find = True
                #print v
                break
        
        #if not find:
        #    print k, vs

            
def check_no_drawing(res, g):
    for k, vs in res.iteritems():
        path = k
        find = False
        if vs:
            continue
        fds = get_folders(path, depth=1)
        for fd in fds:
            _path = '\\'.join([path, fd])
            #print _path
            fs = get_files(_path)
            for _f in fs:
                if not re.search('^._', _f) and _f.endswith('.pdf'):
                    find = True
                    res[path].append(_f.strip('.pdf'))
        if not find:
            #g.writelines([k.encode('utf-8'), '\n'])
            pass
            print 'Not Found: {0}'.format(k.encode('utf-8'))
        else:
            pass
            #print 'Found: {0}, {1}'.format(k.encode('utf-8'), res[path])


if __name__ == '__main__':
    mgr = HosongManager()
    f = open('D:\\res.txt', 'r')
    #g = open('D:\\No_company_code.txt', 'w')
    res = json.load(f)
    #mgr.change_folder_chinese(f)
    #mgr.create_new_folder(f)
    f.close()
    check_all(res, num=1)
    #check_no_drawing(res, g)
    #print res
    #mgr.run()
        
