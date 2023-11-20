#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import multiprocessing
import os
import traceback

from loguru import logger
from tqdm import tqdm

from app.settings import VERSION_STRING_STATISTICS_DIR, LIBRARY_STRING_STATISTICS_DIR, PROCESS_NUM


# @Time : 2023/11/20 17:10
# @Author : Liu Chengyue
def get_merged_version_string_statistics_file_paths():
    library_version_string_statistic_file_paths = []
    for d in os.listdir(VERSION_STRING_STATISTICS_DIR):
        d_path = os.path.join(VERSION_STRING_STATISTICS_DIR, d)
        version_file_paths = []
        for f in os.listdir(d_path):
            f_path = os.path.join(d_path, f)
            version_file_paths.append(f_path)
        library_version_string_statistic_file_paths.append(version_file_paths)
    return library_version_string_statistic_file_paths


def summary_version_statistic(version_string_statistic_list):
    version_num = len(version_string_statistic_list)
    string_num_all = 0  # 总数量（不去重，为了计算平均值用）
    string_num_max = 0  # 最大值
    string_num_min = 100000000  # 最小值
    string_intersection = set(version_string_statistic_list[0]['strings'])
    string_union = set()
    for version_string_statistic in version_string_statistic_list:
        strings = version_string_statistic['strings']
        string_num = version_string_statistic['string_num']
        string_num_all += string_num

        if string_num > string_num_max:
            string_num_max = string_num

        if string_num < string_num_min:
            string_num_min = string_num

        string_intersection = string_intersection.intersection(strings)
        string_union = string_union.union(strings)

    return {
        "version_num": version_num,
        "string_num_all": string_num_all,
        "string_num_all(deduplicated)": len(string_union),
        "string_num_avg": round(string_num_all / version_num, 2),
        "string_num_max": string_num_max,
        "string_num_min": string_num_min,
        "string_num_intersection": len(string_intersection),
    }


def merge_version_string_statistics(version_file_paths):
    # 合并所有版本的结果
    string_set = set()
    version_string_statistic_list = []
    for path in version_file_paths:
        try:
            with open(path) as f:
                version_string_statistics = json.load(f)
                version_string_statistics.pop('version_id')
                version_string_statistics.pop('version_number')
                string_set.update(version_string_statistics['strings'])
                version_string_statistic_list.append(version_string_statistics)
        except Exception as e:
            logger.error(f"error occurred when process {path}, error: {e}")
            logger.error(traceback.format_exc())

    version_statistics_summary = summary_version_statistic(version_string_statistic_list)

    result = {
        "repository_id": version_string_statistic_list[0]['repository_id'],
        "repository_name": version_string_statistic_list[0]['repository_name'],
        "string_num": len(string_set),
        "version_statistics_summary": version_statistics_summary,
        "version_statistics_detail": version_string_statistic_list,
        "strings": list(string_set)
    }

    result_path = os.path.join(LIBRARY_STRING_STATISTICS_DIR,
                               f"{version_string_statistic_list[0]['repository_id']}.json")
    with open(result_path, 'w') as f:
        json.dump(result, f, ensure_ascii=False)


def multiple_merge_version_string_statistics():
    # 读取文件路径
    logger.info(f"start walk paths")
    library_version_string_statistic_file_paths = get_merged_version_string_statistics_file_paths()
    logger.info(f"walk paths finished, num: {len(library_version_string_statistic_file_paths)}")

    # 多进程统计
    logger.info(f"start merge statistic")
    pool = multiprocessing.Pool(processes=PROCESS_NUM)
    logger.info(f"waiting for finishing...")
    results = pool.imap_unordered(merge_version_string_statistics, library_version_string_statistic_file_paths)
    for _ in tqdm(results, total=len(library_version_string_statistic_file_paths), desc="merge statistics"):
        pass
    logger.info(f"all finished.")

    pool.close()
    pool.join()
