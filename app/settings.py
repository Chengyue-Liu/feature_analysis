#!/usr/bin/env python
# -*- coding: utf-8 -*-


# @Time : 2023/11/20 16:06
# @Author : Liu Chengyue
import multiprocessing

from environs import Env

env = Env()
env.read_env()

# 处理过的特征文件夹路径
PROCESSED_FILE_FEATURE_DIR = env.str("PROCESSED_FILE_FEATURE_DIR",
    "/Users/liuchengyue/Desktop/works/feature_analysis/feature-analysis/processed_feature_dir")

# 存放字符串统计结果的文件夹路径
STRING_STATISTIC_DIR = env.str("STRING_STATISTIC_DIR",
    "/Users/liuchengyue/Desktop/works/feature_analysis/feature-analysis/string_statistic_dir")

# 并发数量
EXTRACTION_PROCESS_NUM = multiprocessing.cpu_count()
