#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

# 微信推送配置
# Bark推送服务的Key，需要在https://github.com/Finb/Bark申请
BARK_KEY = "your_bark_key_here"  # 替换为你的Bark Key

# 推送分组
PUSH_GROUP = "公租房通知"

# 爬虫设置
CRAWLER_DELAY = 5  # 页面加载延迟（秒）
MAX_RETRIES = 3    # 最大重试次数

# 数据存储设置
DATA_DIR = "data/"
LOGS_DIR = "logs/"

# 筛选条件设置
DEFAULT_FILTERS = {
    'min_rent': None,           # 最低租金(None表示不限制)
    'max_rent': None,           # 最高租金(None表示不限制)
    'area': None,               # 区域关键词(None表示不限制)
    'house_type': None          # 房型关键词(None表示不限制)
}