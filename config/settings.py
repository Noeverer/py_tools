#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

BARK_KEY = "vWYmRcVLnFKWJP5AJKWADU"
PUSH_GROUP = "公租房通知"
CRAWLER_DELAY = 5
MAX_RETRIES = 3
DATA_DIR = "data/"
LOGS_DIR = "logs/"
DEFAULT_FILTERS = {
    'min_rent': None,
    'max_rent': None,
    'area': None,
    'house_type': None
}

# 特定监控地点设置
MONITORED_LOCATIONS = [
    # 在这里添加您想要监控的特定地点
    # 例如：
    # "张江",
    # "唐镇",
]

# 特定地点推送配置
LOCATION_BARK_KEYS = {
    # 可以为不同的地点设置不同的推送密钥
    # "张江": "your_zhangjiang_bark_key",
    # 如果为空，则使用默认的BARK_KEY
}

# 特定房型监控
MONITORED_HOUSE_TYPES = [
    # 在这里添加您想要监控的特定房型
    # 例如：
    # "1室1厅",
    # "2室1厅"
]
