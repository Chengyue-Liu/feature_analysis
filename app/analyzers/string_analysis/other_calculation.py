#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from app.settings import FINAL_STATISTICS_JSON_PATH
# @Time : 2023/11/20 23:27
# @Author : Liu Chengyue

import numpy as np


def calculate():
    with open(FINAL_STATISTICS_JSON_PATH) as f:
        library_string_statistics = json.load(f)

    # 数量列表
    library_view = library_string_statistics['library_view']
    category_count = library_view['library_string_num:count']
    library_string_num_list = []
    for library_string_num, count in category_count.items():
        library_string_num_list.extend([int(library_string_num)] * count)

    # 倒序排列
    q_10 = np.percentile(library_string_num_list, 10)
    q1 = np.percentile(library_string_num_list, 25)
    q2 = np.percentile(library_string_num_list, 50)
    q3 = np.percentile(library_string_num_list, 75)
    q_90 = np.percentile(library_string_num_list, 90)

    print(q_10, q1, q2, q3, q_90)

    string_view = library_string_statistics['string_view']
    category_count = string_view['seen_library_num:count']
    category_count = {int(k): category_count[k] for k in sorted(category_count, key=lambda x: int(x))}
    string_seen_library_num_list = []
    count_2 = 0
    for seen_library_num, count in category_count.items():
        if count == 1:
            print(seen_library_num, count)
            count_2 += 1

        string_seen_library_num_list.extend([int(seen_library_num)] * count)
    print(count_2)
    q_85 = np.percentile(string_seen_library_num_list, 85)
    q_90 = np.percentile(string_seen_library_num_list, 90)
    q_95 = np.percentile(string_seen_library_num_list, 95)
    q_98 = np.percentile(string_seen_library_num_list, 99)
    q_99_98 = np.percentile(string_seen_library_num_list, 99.98)
    q_99_99 = np.percentile(string_seen_library_num_list, 99.99)
    print(q_85, q_90, q_95, q_98, q_99_98, q_99_99)
