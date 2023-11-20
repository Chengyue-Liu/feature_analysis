#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from app.analyzers.string_analysis.analysis import analyze_library_string_statistics
from app.analyzers.string_analysis.draw_picture import draw
from app.analyzers.string_analysis.generate_version_string_statistic_file import \
    multiple_generate_version_string_statistics
from app.analyzers.string_analysis.merge_version_string_statistic_file import multiple_merge_version_string_statistics


# @Time : 2023/11/20 16:06
# @Author : Liu Chengyue


def main():
    # 根据每个processed_feature 产生 string_statistic
    # multiple_generate_version_string_statistics()

    # 合并每个库的文件，方便后续的处理
    # multiple_merge_version_string_statistics()

    # 分布统计
    # analyze_library_string_statistics()

    # 绘图
    draw()


if __name__ == '__main__':
    main()
