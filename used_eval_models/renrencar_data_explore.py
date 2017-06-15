# -*- coding:utf-8 -*-
'''
Created on 2017/5/25

@author: kongyangyang
'''
#人人车数据探索
from utils import *


class ExploreRawData(object):
    def __init__(self):
        self.raw_data = []
        self.field_name_to_idx = {}

    def load_raw_data(self, srcpath):
        self.raw_data = []
        with open(srcpath, "r") as file_read:
            for line in file_read:
                items = line.strip("\n").split(",")
                if line.strip("\n").startswith("rowid"):
                    self.field_name_to_idx = {items[i]:i for i in range(len(items))}
                else:
                    self.raw_data.append(items)


    def explore_enum_fields(self):
        fieldslist = ["ys", "czzy","ghcs","pfbz","bsx","cs","jb","qdfs","csjg","fdjxh","jqxs","rllx","rybh","city","brand","jccs",'stylename']
        fields_value_num_dict = {}

        for sample in self.raw_data:
            for field in fieldslist:
                if field != 'stylename':
                    if field not in fields_value_num_dict:
                        fields_value_num_dict[field] = set()
                    fields_value_num_dict[field].add(sample[self.field_name_to_idx[field]])
                else:
                    stylename = sample[self.field_name_to_idx[field]]
                    year, volume = parse_style(stylename)
                    if year not in fields_value_num_dict:
                        fields_value_num_dict["year"] = set()
                    # fields_value_num_dict[year].add(year.replace("款",""))
                    fields_value_num_dict["year"].add(year)
                    if volume not in fields_value_num_dict:
                        fields_value_num_dict["volume"] = set()
                    # fields_value_num_dict[volume].add(re.sub("GL|L|T","",volume))
                    fields_value_num_dict["volume"].add(volume)

        fields_value_num_dict_temp = {k:sorted(list(v)) for (k,v) in fields_value_num_dict.items()}
        fields_value_num_dict = {k: {v[i]:i for i in range(len(v))} for (k,v) in fields_value_num_dict_temp.items()}
        for k,v in fields_value_num_dict.items():
            print k,v

