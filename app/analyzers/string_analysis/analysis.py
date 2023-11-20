#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import traceback

from loguru import logger
from tqdm import tqdm

from app.settings import LIBRARY_STRING_STATISTICS_DIR, FINAL_STATISTICS_JSON_PATH


# @Time : 2023/11/20 17:43
# @Author : Liu Chengyue
def load_all_library_string_statistics():
    library_string_statistics_list = []
    for root, dirs, files in os.walk(LIBRARY_STRING_STATISTICS_DIR):
        for file_name in files:
            f_path = os.path.join(root, file_name)
            try:
                with open(f_path) as file_obj:
                    library_string_statistics_list.append(json.load(file_obj))
            except Exception as e:
                logger.error(f"error occurred when process {f_path}, error: {e}")
                logger.error(traceback.format_exc())

    return library_string_statistics_list


def statistic(library_string_statistics_list):
    library_num = len(library_string_statistics_list)
    string_num_all = 0  # 总数量（不去重，为了计算平均值用）
    string_num_list = []  # 所有库的字符串数量统计，用于生成分布图
    string_num_max = 0  # 最大值
    string_num_min = 100000000  # 最小值
    string_intersection = set(library_string_statistics_list[0]['strings'])
    string_union = set()
    for library_string_statistics in tqdm(library_string_statistics_list, total=len(library_string_statistics_list),
                                          desc="statistic"):
        strings = library_string_statistics['strings']
        string_num = library_string_statistics['string_num']
        string_num_list.append(string_num)
        string_num_all += string_num

        if string_num > string_num_max:
            string_num_max = string_num

        if string_num < string_num_min:
            string_num_min = string_num

        string_intersection = string_intersection.intersection(strings)
        string_union = string_union.union(strings)

    return {
        "library_num": library_num,
        "string_num_all": string_num_all,
        "string_num_all(deduplicated)": len(string_union),
        "string_num_avg": round(string_num_all / library_num, 2),
        "string_num_max": string_num_max,
        "string_num_min": string_num_min,
        "string_num_intersection": len(string_intersection),
    }


def analyze_library_string_statistics():
    # 加载所有的文件统计
    logger.info(f"load_all_library_string_statistics...")
    library_string_statistics_list = load_all_library_string_statistics()
    logger.info(f"load_all_library_string_statistics finished")
    # 分析这些统计结果

    library_string_statistics = statistic(library_string_statistics_list)

    with open(FINAL_STATISTICS_JSON_PATH, 'w') as f:
        json.dump(library_string_statistics, f, ensure_ascii=False, indent=4)
    logger.info(f"all finished")
