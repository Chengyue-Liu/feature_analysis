#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from math import log10

# @Time : 2023/11/20 19:35
# @Author : Liu Chengyue
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from app.settings import FINAL_STATISTICS_JSON_PATH


def plot_distribution_library_view(data_dict: dict):
    # data_dict = {log10(int(k)) if int(k) != 0 else 0: data_dict[k] for k in sorted(data_dict, key=lambda x: int(x))}
    data_dict = {int(k): data_dict[k] for k in sorted(data_dict, key=lambda x: int(x))}
    print(data_dict)
    # 提取字典中的键和值
    x_values = list(data_dict.keys())[1:]
    y_values = list(data_dict.values())[1:]

    # 自定义 x 轴和 y 轴的刻度
    # x_ticks = [0, 1, 2, 3, 4, 5, 6]  # 自定义 x 轴刻度
    plt.xscale('log')
    y_ticks = [0, 5, 10, 20, 50, 100, 200, 300]  # 自定义 y 轴刻度

    # 绘制折线图
    plt.plot(x_values, y_values, label='折线图')

    # 设置 x 轴和 y 轴的刻度
    # plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    # 添加标签和标题
    plt.xlabel('string num(10^n)')
    plt.ylabel('library num')
    plt.title('library string num')

    # 显示图例
    plt.legend()

    # 显示图形
    plt.show()

    # 显示图形
    plt.show()


def plot_distribution_string_view(data_dict: dict):
    # data_dict = {log10(int(k)) if int(k) != 0 else 0: data_dict[k] for k in sorted(data_dict, key=lambda x: int(x))}
    data_dict = {int(k): data_dict[k] for k in sorted(data_dict, key=lambda x: int(x))}
    print(data_dict)
    # 提取字典中的键和值
    x_values = list(data_dict.keys())[1:]
    y_values = list(data_dict.values())[1:]

    # 自定义 x 轴和 y 轴的刻度
    # x_ticks = [0, 1, 2, 3, 4, 5, 6]  # 自定义 x 轴刻度
    # y_ticks = [0, 5, 10, 20, 50, 100, 200, 300]  # 自定义 y 轴刻度
    plt.xscale('log')
    plt.xscale('log')

    # 绘制折线图
    plt.plot(x_values, y_values, label='折线图')

    # 设置 x 轴和 y 轴的刻度
    # plt.xticks(x_ticks)
    # plt.yticks(y_ticks)

    # 添加标签和标题
    plt.xlabel('seen library num(10^n)')
    plt.ylabel('string num(10^n)')
    plt.title('library string num')

    # 显示图例
    plt.legend()

    # 显示图形
    plt.show()

    # 显示图形
    plt.show()


def draw():
    with open(FINAL_STATISTICS_JSON_PATH) as f:
        library_string_statistics = json.load(f)
    library_view = library_string_statistics['library_view']
    category_count = library_view['library_string_num:count']
    plot_distribution_library_view(category_count)

    string_view = library_string_statistics['string_view']
    category_count = string_view['seen_library_num:count']
    plot_distribution_string_view(category_count)
