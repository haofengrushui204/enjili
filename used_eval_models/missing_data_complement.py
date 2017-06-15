# -*- coding:utf-8 -*-
'''
Created on 2017/6/14

@author: kongyangyang
'''
import urllib2
from lxml import etree


class MissingDataComplement(object):
    def __init__(self):
        pass

    def complement_jcsj(self, url_path):
        url_jcsj = {}
        with open(url_path, "r") as file_read:
            for url in file_read:
                html = urllib2.urlopen(url.strip()).read()
                page = etree.HTML(html.lower().decode('utf-8'))
                hrefs = page.xpath(u"//a")


