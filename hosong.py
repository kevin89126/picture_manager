#!/usr/bin/python
# -*- coding: UTF-8 -*-
from utils import get_files, get_folders, copy, rename, create_folder, \
     path_exists, has_chinese, collect_chinese
import re
import json
import shutil

FOLDER_MAP = {
    u'001.*成品圖': '001 Drawing',
    u'002.*製程管制計畫': '002 QC_Plan',
    u'003.*標準作業程序': '003 SOP',
    u'004.*SIP.*標準檢驗程序': '004 SIP',
    u'005.*成品檢驗報告': '005 FQC',
    u'006.*客訴資料': '006 Claim_Report',
    u'007.*客訴品質通報': '007 Claim_Information',
    u'008.*NC': '008 NC',
    u'009.*MC': '009 MC',
    u'010.*成本分析': '010 Cost',
    u'011.*開發': '011 RD',
    u'012.*其他': '012 Misc'
    }

FILE_MAP = {
    u'A.*進料檢驗記錄表': 'A IQC',
    u'B.*自主巡迴檢查表': 'B IPQC',
    u'C.*成品檢查紀錄表': 'C FQC'
    }

class HosongManager(object):

    def __init__(self, listbox=None):
        self.input_path = None
        self.output_path = None
        self.listbox = listbox
        
    def rm_chinese(self):
        fds = get_folders(self.input_path)
        for fd in fds:
            path = '\\'.join([self.input_path, fd])
            print path
            target_path = '\\'.join([self.input_path, fd.split()[0]])
            print target_path
            rename(path, target_path)

    def _check_chinese_folders(self, fd, path):
        for src in FOLDER_MAP:
            _path = '\\'.join([path, fd])
            if re.search(src, fd):
                msg = _path.strip(self.input_path)
                #print msg
                #f.writelines([msg.encode('utf-8'), '\n'])
                tp = '\\'.join([path, FOLDER_MAP[src]])
                rename(_path, tp)
        return _path

    def change_folder_chinese(
            self, path=None):
        path = path or self.input_path
        fds = get_folders(path, depth=1)
        for fd in fds:
            _path = self._check_chinese_folders(fd, path)
            self.change_folder_chinese(_path)
        return

    def _check_new_folders(self, fd, path):
        _path = '\\'.join([path, fd])
        if re.search('001 Drawing', fd):
            for src in FOLDER_MAP:
                tp = '\\'.join([path, FOLDER_MAP[src]])
                if not path_exists(tp):
                    create_folder(tp)
        return _path
                    
    def create_new_folder(self, path=None):
        path = path or self.input_path
        fds = get_folders(path, depth=1)
        for fd in fds:
            _path = self._check_new_folders(fd, path)
            self.create_new_folder(f, _path)
        return    

    def get_drawing_pdf_name(
            self, src, path=None):
        path = path or self.input_path
        res = {}
        fds = get_folders(path, depth=1)
        for fd in fds:
            _path = '\\'.join([path, fd])
            #print _path
            if re.search(src, fd):
                fs = get_files(_path)
                if not res.has_key(_path):
                    res[_path] = []
                for _f in fs:
                    if not re.search('^._', _f) and _f.endswith('.pdf'):
                       #and re.search('.*]A0[0-9]', _f):
                        res[_path].append(_f.strip('.pdf'))
            _res = self.get_drawing_pdf_name(src, _path)
            res.update(_res)
        return res

    def get_no_drwing_name_again(self, res):
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
                    if not re.search('^._', _f) and _f.endswith('.pdf') \
                           and re.search('.*A.*', _f):
                        find = True
                        res[path].append(_f.strip('.pdf'))
            if not find:
                pass
                #print 'Not Found: {0}'.format(k.encode('utf-8'))
            else:
                print 'Found: {0}, {1}'.format(k.encode('utf-8'), res[path])


    def find_chinese_file(self, f, path=None):
        path = path or self.input_path
        fds = get_folders(path, depth=1)
        for fd in fds:
            #print fd
            _path = '\\'.join([path, fd])
            #print _path
            if not re.search('^._', fd):
                if has_chinese(fd):
                    f.writelines([_path.encode('utf-8'), '\n'])
            fs = get_files(_path)
            for _f in fs:
                if not re.search('^._', _f):
                   #and re.search('.*]A0[0-9]', _f):
                    if has_chinese(_f):
                        f_path = '\\'.join([_path, _f])
                        f.writelines([f_path.encode('utf-8'), '\n'])
            self.find_chinese_file(f, _path)
            #res.update(_res)
        return

    def find_chinese_string(self, f, path=None):
        path = path or self.input_path
        fds = get_folders(path, depth=1)
        for fd in fds:
            #print fd
            _path = '\\'.join([path, fd])
            #print _path
            if not re.search('^._', fd):
                ch = collect_chinese(fd)
                if ch:
                    self.chinese.add(ch.encode('utf-8') + '\n')
            fs = get_files(_path)
            for _f in fs:
                if not re.search('^._', _f):
                   #and re.search('.*]A0[0-9]', _f):
                    ch = collect_chinese(_f)
                    if ch:
                        self.chinese.add(ch.encode('utf-8') + '\n')
            self.find_chinese_string(f, _path)
            #res.update(_res)
        return

    
    def check_no_drawing(self, res, g):
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
                g.writelines([k.strip(self.input_path).encode('utf-8'), '\n'])
                pass
                #print 'Not Found: {0}'.format(k.encode('utf-8'))
            else:
                pass
                #print 'Found: {0}, {1}'.format(k.encode('utf-8'), res[path])
        return res

    def create_hosong_folder(self):
        fds = get_folders(self.input_path)
        for fd in fds:
            fd_path = '\\'.join([self.output_path, fd])
            if path_exists(fd_path):
                continue
            create_folder(fd_path)

    def get_cp_code(self, cp, pre_fix):
        tmps = cp.split(pre_fix)
        if tmps:
            tmps = tmps[1:]
        for tmp in tmps:
            try:
                if int(tmp[0:7]) and len(tmp)>=6:
                    return tmp[0:7]
            except ValueError:
                pass
        return None

    def create_company_code_folder(self, res):
        for k, vs in res.iteritems():
            for v in vs:
                if not re.search(u'.*A.*', v) and re.search(u'.*B.*', v):
                    continue
                cp = k[len(self.input_path)+1:].split('\\')[0]
                org = k.split('\\')[:-1]
                org_fds_path = '\\'.join(org)
                #print org_fds_path
                if len(cp) not in [5,4]:
                    continue
                #print cp, k
                cp_code = self.get_cp_code(v, cp.strip('0123456789'))
                #print v, cp_code
                if not cp_code:
                    continue
                path = '\\'.join([self.output_path, unicode(cp), unicode(
                    'A'+cp_code)])
                if path_exists(path):
                    self.listbox(u'圖片代碼已存在:')
                    self.listbox(u'{0}'.format(path))
                    continue
                shutil.copytree(org_fds_path, path)
                break

    def copy_company_code_file(self, res):
        for k, vs in res.iteritems():
            for v in vs:
                if re.search(u'.*A.*', v) or re.search(u'.*B.*', v):
                    cp = k[len(self.input_path)+1:].split('\\')[0]
                    if len(cp) not in [5,4]:
                        print 'aaa',cp, k[len(self.input_path):]
                        continue
                    #print cp, k
                    cp_code = self.get_cp_code(v, cp.strip('0123456789'))
                    #print v, cp_code
                    if cp_code:
                        path = '\\'.join([self.output_path, unicode(cp), unicode(
                            'A'+cp_code)])
                        #print path, type(path.encode('utf-8'))
                        if not path_exists(path):
                            create_folder(path.encode('utf-8'))
                        break
                    else:
                        pass
                        #print v, cp
        
    def run(self):
        self.listbox(u'改變原始名稱至英文')
        self.change_folder_chinese()
        self.listbox(u'建立公司資料夾')
        self.create_hosong_folder()
        self.listbox(u'取得圖片代碼')
        res = self.get_drawing_pdf_name(u'001 Drawing')
        self.listbox(u'建立圖片代碼')
        self.create_company_code_folder(res)
        self.listbox(u'移轉完成')        
