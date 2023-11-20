#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import multiprocessing
import os
import traceback

from loguru import logger
from tqdm import tqdm

from app.settings import PROCESSED_FILE_FEATURE_DIR, EXTRACTION_PROCESS_NUM, VERSION_STRING_STATISTIC_DIR

# @Time : 2023/11/20 15:12
# @Author : Liu Chengyue
"""
todo 分析
分析范围。
1. 范围和数量：
    1. 库范围：基于zhiling给出的范围。
    2. 库筛选：增加了一定的规则筛选，去掉了操作系统等方面的非library库，同名库等，最终选择了25000个库。
    3. 版本范围：提取了github 所有的tag(如无tag, 则提取默认分支)
    4. 代码去重：提取时，按照代码块进行了去重。（移除comment, 括号，换行符等之后，进行hash计算，按照commit time进行去重）。同时，也去除了明显是第三方组件的部分，如third_party文件夹下的内容。
    5. 特征处理：根据宏的规则，模拟编译时，宏对源码字符串的处理方法，对字符串进行了尽可能的合并和转换。

2. 库级别字符串情况
    1. 覆盖情况
    2. 均值，极值，四分位值

字符串特征覆盖情况？
    统计了多少个库？多少个库有字符串特征，平均数量多少，极值怎么样？
    统计了多少个版本？多少个版本有字符串特征，平均数量多少，极值怎么样？
"""


def get_processed_version_feature_file_paths():
    feature_file_paths = []
    count = 0
    for root, dirs, files in os.walk(PROCESSED_FILE_FEATURE_DIR):
        for f in files:
            f_path = os.path.join(root, f)
            if f_path.endswith('.json'):
                count += 1
                if count % 1000 == 0:
                    logger.info(f"walk progress: {count}")
                feature_file_paths.append(f_path)
    return feature_file_paths


def generate_version_string_statistics(path):
    try:
        # 加载
        with open(path) as f:
            version_feature = json.load(f)

        # 解析字符串
        string_set = set()
        file_features = version_feature['file_features']
        for file_feature in file_features:
            node_features = file_feature['node_features']
            for node_feature in node_features:
                if node_feature_strings := node_feature.get('strings'):
                    if must_compile_string_group := node_feature_strings['must_compile_string_group']:
                        string_set.update(must_compile_string_group)
                    if conditional_compile_string_groups := node_feature_strings['conditional_compile_string_groups']:
                        for conditional_compile_string_group in conditional_compile_string_groups:
                            string_set.update(conditional_compile_string_group)

        result = {
            "repository_id": version_feature['repository_id'],
            "repository_name": version_feature['repository_name'],
            "version_id": version_feature['version_id'],
            "version_number": version_feature['version_number'],
            "string_num": len(string_set),
            "strings": list(string_set)
        }

        # 保存
        output_dir = os.path.join(VERSION_STRING_STATISTIC_DIR, str(version_feature['repository_id']))
        os.makedirs(output_dir, exist_ok=True)
        result_path = os.path.join(output_dir, f"{version_feature['version_id']}.json")
        with open(result_path, 'w') as f:
            json.dump(result, f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"error occurred when process {path}, error: {e}")
        logger.error(traceback.format_exc())


def multiple_generate_version_string_statistics():
    # 读取文件路径
    logger.info(f"start walk feature_file_paths")
    feature_file_paths = get_processed_version_feature_file_paths()
    logger.info(f"walk feature_file_paths finished, num: {len(feature_file_paths)}")

    # 多进程统计
    logger.info(f"start statistic")
    pool = multiprocessing.Pool(processes=EXTRACTION_PROCESS_NUM)
    logger.info(f"waiting for finishing...")
    results = pool.imap_unordered(generate_version_string_statistics, feature_file_paths)
    for _ in tqdm(results, total=len(feature_file_paths), desc="statistic strings"):
        pass
    logger.info(f"all finished.")

    pool.close()
    pool.join()
