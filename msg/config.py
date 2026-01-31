#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Liu@06027',
    'database': 'gzf',
    'charset': 'utf8'
}

# 微信推送配置
# Bark推送服务的Key，需要在https://github.com/Finb/Bark申请
BARK_KEY = "vWYmRcVLnFKWJP5AJKWADU"

# 推送分组
PUSH_GROUP = "公租房通知"

# 查询设置
QUERY_LIMIT = 10  # 默认查询数量

# 筛选条件设置
DEFAULT_FILTERS = {
    'available_only': True,     # 只推送未被选走的房源
    'min_rent': None,           # 最低租金(None表示不限制)
    'max_rent': None,           # 最高租金(None表示不限制)
    'area': None,               # 区域关键词(None表示不限制)
    'house_type': None          # 房型关键词(None表示不限制)
}