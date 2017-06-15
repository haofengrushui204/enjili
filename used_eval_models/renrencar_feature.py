# -*- coding:utf-8 -*-
'''
Created on 2017/5/25

@author: kongyangyang
'''
#人人车特征
import time
from src.auto_evaluation_models.utils import  *



class  RRCarFeature(object):
    def __init__(self):
        self.field_name_to_idx = {}
        self.field_idx_to_name = {}
        self.data_raw = []
        self.enum_fields_value_num_dict = {}
        self.fields_num_dict = {}
        self.feature_name = []
        self.xcbj = []

    def loadRawData(self,srcpath):
        with open(srcpath, "r") as file_read:
            for line in file_read:
                items = line.strip("\n").split("\t")
                if line.strip("\n").startswith("rowid"):
                    self.field_name_to_idx = {items[i]:i for i in range(len(items))}
                    self.field_name_to_idx["year"] = self.field_name_to_idx["style_name"]
                    self.field_idx_to_name = {v:k for (k,v) in self.field_name_to_idx.items()}
                elif self.check_raw_data(items):
                    idx = self.field_name_to_idx["style_name"]
                    items[idx] = parse_style(items[idx]) #year
                    idx = self.field_name_to_idx["bsx"]
                    items[idx] = parse_bsx(items[idx])
                    self.data_raw.append(items)
        self.field_name_to_idx.pop("style_name")

    def check_raw_data(self, items):
        for i in range(len(items)):
            if self.field_idx_to_name[i] not in fields_disable:
                if len(items[i]) == 0:
                    return 0
        return 1

    def fields_explore(self):
        for sample in self.data_raw:
            for field in fields_enum_type:
                if field not in self.enum_fields_value_num_dict:
                    self.enum_fields_value_num_dict[field] = set()
                self.enum_fields_value_num_dict[field].add(sample[self.field_name_to_idx[field]])

        fields_value_num_dict_temp = {k:sorted(list(v)) for (k,v) in self.enum_fields_value_num_dict.items()}
        self.fields_num_dict = {k: {v[i]:i for i in range(len(v))} for (k,v) in fields_value_num_dict_temp.items()}

    def one_hot_code(self, num,idx):
        x = [0] * num
        x[idx] = 1.0
        return x

    def generate_samples(self):
        samples = []
        for raw_sample in self.data_raw:
            feature = []

            spsj = raw_sample[self.field_name_to_idx["spsj"]]
            spsj_stamp = time.mktime(time.strptime(spsj, '%Y/%m/%d'))
            jcsj = raw_sample[self.field_name_to_idx["jcsj"]]
            stop_stamp = time.mktime(time.strptime("2017-05-25", '%Y-%m-%d'))
            if jcsj == "":
                jcsj_stamp = stop_stamp
            else:
                jcsj_stamp = time.mktime(time.strptime(jcsj, '%Y/%m/%d'))

            feature.append(int((jcsj_stamp - spsj_stamp) / (3600*24*30))) #上牌时间和检测时间差
            feature.append(int((stop_stamp - jcsj_stamp) / (3600*24*30))) #截止时间和检测时间差
            feature.append(month_to_stop(raw_sample[self.field_name_to_idx["njdq"]]))
            feature.append(month_to_stop(raw_sample[self.field_name_to_idx["jqxdq"]]))
            # feature.append(month_to_stop(raw_sample[self.field_name_to_idx["syxdq"]]))
            self.collect_field_name("diff_spsj_jcsj", "diff_stop_jcsj", "diff_stop_njdq", "diff_spsj_jqxdq")

            fields_disable.add("spsj")
            fields_disable.add("jcsj")
            fields_disable.add("njdq")
            fields_disable.add("jqxdq")
            fields_disable.add("syxdq")
            for field_type in fields_all.keys():
                if field_type in fields_type_disable:
                    continue
                for field in fields_all[field_type]:
                    if field not in fields_disable:
                        if field not in self.feature_name:
                            self.collect_field_name(field)
                        if field not in self.enum_fields_value_num_dict:
                            if field in ["cssj","grjyzdj","grjyzgj","xcbj"]:
                                feature.append(float(raw_sample[self.field_name_to_idx[field]]) / float(raw_sample[self.field_name_to_idx["xcbj"]]))
                            else:
                                feature.append(raw_sample[self.field_name_to_idx[field]])
                            self.collect_field_name(field)
                        else:
                            feature.extend(self.one_hot_code(len(self.enum_fields_value_num_dict[field]),self.fields_num_dict[field][raw_sample[self.field_name_to_idx[field]]]))
                            self.collect_field_name(field + "_" + raw_sample[self.field_name_to_idx[field]])

            feature.append(float(raw_sample[self.field_name_to_idx["czbj"]]) / float(raw_sample[self.field_name_to_idx["xcbj"]]))
            feature.append(float(raw_sample[self.field_name_to_idx["xcbj"]]))
            samples.append(feature)
            self.collect_field_name("czbj", "xcbj_raw")
        return samples

    def save_sampeles_to_disk(self, samples, dstpath):
        with open(dstpath, "w") as file_write:
            for sample in samples:
                file_write.write(",".join([str(s) for s in sample]) + "\n")


    def add_czbj_to_samples(self, samples, czbj_predict):
        pass

    def collect_field_name(self, *args):
        for field_name in args:
            if field_name not in self.feature_name:
                self.feature_name.append(field_name)

    def main(self, rrc_raw_path, sample_save_path, feature_name_save_path):
        self.loadRawData(rrc_raw_path)
        self.fields_explore()
        samples = self.generate_samples()
        self.save_sampeles_to_disk(samples, sample_save_path)
        with open(feature_name_save_path, "w") as file_write:
            for field in self.feature_name:
               file_write.write(field + "\n")


if __name__ == "__main__":
    rrcar_feature = RRCarFeature()
    workdir = "E:/Work/jobs/data/auto-monitor/"
    rrcar_feature.main(workdir + "rrc_feature_raw.txt",
                       workdir + "rrcar_samples",
                       workdir + "feature_name.txt")






















