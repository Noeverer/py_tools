#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

# 微信推送配置
# Bark推送服务的Key，需要在https://github.com/Finb/Bark申请
BARK_KEY = "vWYmRcVLnFKWJP5AJKWADU"  # 替换为你的Bark Key

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
    'max_rent': 5000,           # 最高租金(None表示不限制)
    'area': None,               # 区域关键词(None表示不限制)
    'house_type': None          # 房型关键词(None表示不限制)
}

# 特定监控地点设置
MONITORED_LOCATIONS = [
    "张江",
    "唐镇",
    "曹路",
    "合庆",
    "金桥",
    "陆家嘴",
    "金杨新村",
    "洋泾",
    "花木",
    "康桥"
]

# 特定地点推送配置
LOCATION_BARK_KEYS = {
    # 可以为不同的地点设置不同的推送密钥
    # "张江": "your_zhangjiang_bark_key",
    # "唐镇": "your_tangzhen_bark_key",
    # 如果为空，则使用默认的BARK_KEY
}

# 特定房型监控
MONITORED_HOUSE_TYPES = [
    # 在这里添加您想要监控的特定房型
    # 例如：
    # "1室1厅",
    # "2室1厅",
    # "1室0厅"
]
