# -*- coding:utf-8 -*-
'''
Created on 2017/6/7

@author: kongyangyang
'''
import re 
fields_enum_type = ["ys", "czzy","ghcs","pfbz","bsx","cs","jb","qdfs","csjg","jqxs","rllx","rybh","city","brand","jccs", "pl", "year"] # style_name -> year
fields_disable = {"fdjxh","jcr","model","czbj","long","width","height","jccs","cssj","grjyzdj","grjyzgj","syxdq","cms","zws","cs"}
fields_type_disable = {"owner","platform","detect"}

fields_all = {"base":["year","model","brand","city","czbj","xcbj"],# style_name -> year
               "price":["cssj","grjyzdj",'grjyzgj','sfjj'],
               "owner":["czmc","czzy","czdz"],
               "usedcar":["lcs","ys","ghcs","njdq","jqxdq","sf4sdby","gcfp","sfgz","pfbz","pl","bsx","jb","cs","qdfs"],
               "configuration":["long","width","height","csjg","cms","zws","fdjxh","jqxs","rllx","rybh",'zjszddtj',
                                'qjtc','zpzy','czld','wysqd','zyjr','dcyx','gps','czdh','ddzdhsj','dsxh','zcld',
                                'fxphd','spfz','zdbc'],
               'detect':['tyjc','jcsj','jcr','jccs','zdzjsg','hsc','spc','fdjc','dp','xgxt','ctfgj','csfzjgj','cnymsbw',
                         'dzkzxt','cygnkg','dgxt','blhsj','ltlg','scfj','jss','fdj','zxxt'],
               "platform":["fwf"]
               }

style_desc_param_regexp = {
    "year": re.compile(u"[0-9]{4}款"),
    "biansuxiang": re.compile(u"手动[挡]*|自动[挡]*|AT|MT|DSG|双离合|手自一体|CVT无级变速|无级|CVT|DCT"),
    "volume": re.compile(
        u"[0-9]+[\.]*[0-9]+GL[SX]*"
        u"|[0-9]+[\.]*[0-9]+[LTI]+"
        u"|[0-9]+[\.]*[0-9]+TCI"
        u"|[0-9]+\.[0-9]+"
    ),
    "ranyhouleixing": re.compile(u"柴油|汽油"),
    "box": re.compile(u"两厢|三厢"),
    "qudongxingshi": re.compile(u"四驱|两驱|[A24]+WD"),
    "seat": re.compile(u"[0-9]+座|[一二三四五六七八九十]+座")
}

workdir = "E:/Work/jobs/data/auto-monitor/"
