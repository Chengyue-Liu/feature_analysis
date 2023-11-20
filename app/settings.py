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
                                     "/Users/liuchengyue/Desktop/works/feature_analysis/feature_analysis/files/processed_feature_dir")

# 存放每个版本字符串统计结果的文件夹路径
VERSION_STRING_STATISTICS_DIR = env.str("VERSION_STRING_STATISTICS_DIR",
                                        "/Users/liuchengyue/Desktop/works/feature_analysis/feature_analysis/files/version_string_statitstics")

# 存放每个库（把所有版本版本合并后）字符串统计结果的文件夹路径
LIBRARY_STRING_STATISTICS_DIR = env.str("LIBRARY_STRING_STATISTICS_DIR",
                                        "/Users/liuchengyue/Desktop/works/feature_analysis/feature_analysis/files/library_string_statistics")

# 最终统计结果文件
FINAL_STATISTICS_JSON_PATH = env.str("FINAL_STATISTICS_JSON_PATH", "library_string_statistics.json")

# 并发数量
PROCESS_NUM = multiprocessing.cpu_count()
