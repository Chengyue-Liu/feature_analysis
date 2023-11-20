#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
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
                    if len(library_string_statistics_list) % 1000 == 0:
                        logger.info(f"load progress: {len(library_string_statistics_list)}")
            except Exception as e:
                logger.error(f"error occurred when process {f_path}, error: {e}")
                logger.error(traceback.format_exc())

    return library_string_statistics_list


def string_view_statistics(library_string_statistics_list, string_dict):
    # 字符串视角的统计
    string_num = len(string_dict)
    seen_library_num_all = 0  # 总数量（不去重，为了计算平均值用）
    library_num_list = []
    seen_library_num_max = 0
    seen_library_num_min = 100000000
    for s, library_id_set in string_dict.items():
        library_num = len(library_id_set)
        seen_library_num_all += library_num
        library_num_list.append(library_num)

        if library_num > seen_library_num_max:
            seen_library_num_max = library_num

        if library_num < seen_library_num_min:
            seen_library_num_min = library_num
    seen_library_avg = round(seen_library_num_all / string_num, 2)
    counter = collections.Counter(library_num_list)

    string_view = {
        "string_num_all(deduplicated)": string_num,
        "seen_library_num": len(library_string_statistics_list),
        "seen_library_num_max": seen_library_num_max,
        "seen_library_num_min": seen_library_num_min,
        "seen_library_avg": seen_library_avg,
        "seen_library_num:count": dict(counter.items()),
        # "seen_library_num_list": library_num_list
    }
    return string_view


def library_view_statistics(library_string_statistics_list):
    library_num = len(library_string_statistics_list)
    string_num_all = 0  # 总数量（不去重，为了计算平均值用）
    string_num_list = []  # 所有库的字符串数量统计，用于生成分布图
    string_num_max = 0  # 最大值
    string_num_min = 100000000  # 最小值
    string_intersection = set(library_string_statistics_list[0]['strings'])
    string_dict = dict()
    # library 视角的统计
    for library_string_statistics in tqdm(library_string_statistics_list, total=len(library_string_statistics_list),
                                          desc="statistic"):
        # 库级别总体统计
        repository_id = library_string_statistics['repository_id']
        strings = library_string_statistics['strings']
        string_num = library_string_statistics['string_num']
        # 字符串数量列表
        string_num_list.append(string_num)
        # 字符串总数量
        string_num_all += string_num
        # 最大数量
        if string_num > string_num_max:
            string_num_max = string_num
        # 最小数量
        if string_num < string_num_min:
            string_num_min = string_num
        # 交集
        string_intersection = string_intersection.intersection(strings)

        # 用于字符串视角统计的dict, library 的信息
        for s in strings:
            if not (library_id_set := string_dict.get(s)):
                string_dict[s] = library_id_set = set()
            library_id_set.add(repository_id)

    counter = collections.Counter(string_num_list)

    library_view = {
        "library_num": library_num,
        "string_num_all": string_num_all,
        "string_num_all(deduplicated)": len(string_dict),
        "string_num_avg": round(string_num_all / library_num, 2),
        "string_num_max": string_num_max,
        "string_num_min": string_num_min,
        "string_num_intersection": len(string_intersection),
        "library_string_num:count": dict(counter.items()),
        # "library_string_num_list": string_num_list,
    }
    return library_view, string_dict


def statistic(library_string_statistics_list):
    library_view, string_dict = library_view_statistics(library_string_statistics_list)
    string_view = string_view_statistics(library_string_statistics_list, string_dict)
    return {
        "library_view": library_view,
        "string_view": string_view

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
