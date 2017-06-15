# -*- coding:utf-8 -*-
'''
Created on 2017/5/26

@author: kongyangyang
'''
import time
from src.auto_evaluation_models.config import *


def strdecode(namestr):
    if not isinstance(namestr, unicode):
        try:
            namestr = namestr.decode('utf-8')
        except UnicodeDecodeError:
            namestr = namestr.decode('gbk', 'ignore')
    return namestr

def parse_style(stylename):
    stylename = strdecode(stylename)
    year,volume = '',''
    year_find = style_desc_param_regexp["year"].findall(stylename)
    if len(year_find) == 1:
        year = year_find[0].encode("utf-8")
    return year

def parse_bsx(bsx_desc):
    p = re.compile(u"[（）()]+")
    bsx_desc = p.sub(u"", bsx_desc.decode("utf-8")).upper().encode("utf-8")
    return bsx_desc

def month_to_stop(dt_str):
    dt_stamp = time.mktime(time.strptime(dt_str, '%Y/%m/%d'))
    stop_stamp = time.mktime(time.strptime("2017-05-25", '%Y-%m-%d'))
    return max(0,int((dt_stamp - stop_stamp) / (3600*24*30)))


if __name__ == "__main__":
    print parse_style("2010款 2.0L".decode("utf-8"))

