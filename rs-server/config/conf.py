# -*- coding: utf-8 -*-
"""
Author : Hongbo Huang
Contact: huang_hb138@163.com
Date   : 2020/7/13 14:48
Desc   : 读取配置文件的类
"""

from configparser import ConfigParser


class Conf(object):
    def __init__(self, conf_file):
        self.conf_obj = ConfigParser(comment_prefixes=";")
        self.conf_obj.read(conf_file)

    def getstring(self, section, key, default=""):
        try:
            return self.conf_obj.get(section, key)
        except:
            return default

    def getboolean(self, section, key, default=False):
        try:
            return self.conf_obj.getboolean(section, key)
        except:
            return default

    def getint(self, section, key, default=0):
        try:
            return self.conf_obj.getint(section, key)
        except:
            return default

    def getfloat(self, section, key, default=0.0):
        try:
            return self.conf_obj.getfloat(section, key)
        except:
            return default

    def set(self, section, key, value="", default=0):
        try:
            return self.conf_obj.set(section, key, value)
        except:
            return default

    def write(self, conf_file):
        with open(conf_file, 'w+') as wf:
            self.conf_obj.write(wf)
