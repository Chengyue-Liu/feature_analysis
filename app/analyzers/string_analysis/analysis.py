#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import traceback

from loguru import logger

from app.settings import LIBRARY_STRING_STATISTIC_DIR


# @Time : 2023/11/20 17:43
# @Author : Liu Chengyue
def load_all_library_string_statistics():
    library_string_statistics_list = []
    for root, dirs, files in os.walk(LIBRARY_STRING_STATISTIC_DIR):
        for f in files:
            f_path = os.path.join(root, f)
            try:
                with open(f_path) as f:
                    library_string_statistics_list.append(json.load(f))
            except Exception as e:
                logger.error(f"error occurred when process {f_path}, error: {e}")
                logger.error(traceback.format_exc())

    return library_string_statistics_list


def statistic(library_string_statistics_list):
    library_num = len(library_string_statistics_list)
    string_num_all = 0  # 总数量（不去重，为了计算平均值用）
    string_num_avg = 0  # 平均值
    string_num_max = 0  # 最大值
    string_num_min = 100000000  # 最小值
    string_intersection = set(library_string_statistics_list[0]['strings'])
    for library_string_statistics in library_string_statistics_list:
        pass


def analyze_library_string_statistics():
    # 加载所有的文件统计
    library_string_statistics_list = load_all_library_string_statistics()

    # 分析这些统计结果
