#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 - 支持灵活配置
"""

import os
from typing import Dict, List, Optional, Union

# =============================================================================
# 基础配置类
# =============================================================================


class BarkConfig:
    """Bark推送配置"""

    def __init__(self):
        # 主推送密钥
        self.KEY = os.getenv("BARK_KEY", "vWYmRcVLnFKWJP5AJKWADU")

        # 默认分组名称
        self.DEFAULT_GROUP = os.getenv("BARK_DEFAULT_GROUP", "公租房通知")

        # 推送服务URL（支持自定义服务器）
        self.SERVER_URL = os.getenv("BARK_SERVER_URL", "https://api.day.app")

        # 默认推送参数
        self.DEFAULT_PARAMS = {
            "sound": os.getenv("BARK_SOUND", "telegraph"),
            "icon": os.getenv(
                "BARK_ICON",
                "https://raw.githubusercontent.com/Finb/Bark/refs/heads/master/Server/assets/favicon.ico",
            ),
            "level": os.getenv("BARK_LEVEL", "active"),
            "category": os.getenv("BARK_CATEGORY", "house_notification"),
            "automaticallyCopy": os.getenv("BARK_AUTO_COPY", "false").lower() == "true",
        }

        # 测试推送参数
        self.TEST_PARAMS = {
            "sound": os.getenv("BARK_TEST_SOUND", "calypso"),
            "level": os.getenv("BARK_TEST_LEVEL", "passive"),
        }


class PushTimeConfig:
    """推送时间控制配置"""

    def __init__(self):
        self.ENABLED = os.getenv("PUSH_TIME_ENABLED", "true").lower() == "true"
        self.START_HOUR = int(os.getenv("PUSH_START_HOUR", "8"))
        self.END_HOUR = int(os.getenv("PUSH_END_HOUR", "11"))
        self.TIMEZONE = os.getenv("PUSH_TIMEZONE", "Asia/Shanghai")

        # 支持多时间段配置
        self.TIME_SLOTS = self._parse_time_slots(os.getenv("PUSH_TIME_SLOTS", "8-11"))

    def _parse_time_slots(self, slots_str: str) -> List[tuple]:
        """解析时间段配置，格式: '8-11,14-16'"""
        if not slots_str:
            return [(self.START_HOUR, self.END_HOUR)]

        slots = []
        for slot in slots_str.split(","):
            try:
                start, end = map(int, slot.strip().split("-"))
                slots.append((start, end))
            except ValueError:
                continue
        return slots if slots else [(self.START_HOUR, self.END_HOUR)]


class CrawlerConfig:
    """爬虫配置"""

    def __init__(self):
        self.DELAY = int(os.getenv("CRAWLER_DELAY", "5"))
        self.MAX_RETRIES = int(os.getenv("CRAWLER_MAX_RETRIES", "3"))
        self.TIMEOUT = int(os.getenv("CRAWLER_TIMEOUT", "30"))

        # 目标URL配置
        self.TARGET_URL = os.getenv(
            "CRAWLER_TARGET_URL", "https://select.pdgzf.com/houseLists"
        )

        # 浏览器配置
        self.HEADLESS = os.getenv("CRAWLER_HEADLESS", "true").lower() == "true"
        self.NO_SANDBOX = os.getenv("CRAWLER_NO_SANDBOX", "true").lower() == "true"


class DataConfig:
    """数据存储配置"""

    def __init__(self):
        self.DATA_DIR = os.getenv("DATA_DIR", "data/")
        self.LOGS_DIR = os.getenv("LOGS_DIR", "logs/")
        self.BACKUP_DAYS = int(os.getenv("DATA_BACKUP_DAYS", "30"))
        self.MAX_FILE_SIZE = int(os.getenv("DATA_MAX_FILE_SIZE", "10485760"))  # 10MB


class FilterConfig:
    """筛选配置"""

    def __init__(self):
        # 默认筛选条件
        self.DEFAULT_FILTERS = {
            "min_rent": self._parse_number(os.getenv("FILTER_MIN_RENT")),
            "max_rent": self._parse_number(os.getenv("FILTER_MAX_RENT", "5000")),
            "area": os.getenv("FILTER_AREA") if os.getenv("FILTER_AREA") else None,
            "house_type": os.getenv("FILTER_HOUSE_TYPE")
            if os.getenv("FILTER_HOUSE_TYPE")
            else None,
        }

        # 预设筛选方案（支持从环境变量加载）
        self.PRESET_FILTERS = self._load_preset_filters()

        # 启用的筛选方案
        enabled_filters = os.getenv("ENABLED_PRESET_FILTERS", "金桥低价")
        self.ENABLED_PRESET_FILTERS = [
            f.strip() for f in enabled_filters.split(",") if f.strip()
        ]

    def _parse_number(self, value: Optional[str]) -> Optional[float]:
        """解析数字"""
        if value is None or value.lower() == "none":
            return None
        try:
            return float(value)
        except ValueError:
            return None

    def _load_preset_filters(self) -> Dict[str, Dict]:
        """加载预设筛选方案"""
        presets = {
            "金桥低价": {
                "area": "金桥",
                "max_rent": 3000,
                "min_rent": None,
                "house_type": None,
            },
            "张江低价": {
                "area": "张江",
                "max_rent": 3000,
                "min_rent": None,
                "house_type": None,
            },
            "唐镇低价": {
                "area": "唐镇",
                "max_rent": 3000,
                "min_rent": None,
                "house_type": None,
            },
            "金桥": {
                "area": "金桥",
                "max_rent": None,
                "min_rent": None,
                "house_type": None,
            },
            "低价房": {
                "area": None,
                "max_rent": 3000,
                "min_rent": None,
                "house_type": None,
            },
        }

        # 从环境变量加载自定义筛选方案
        # 格式: PRESET_FILTER_金桥=area:金桥,max_rent:3000
        for key, value in os.environ.items():
            if key.startswith("PRESET_FILTER_"):
                filter_name = key[13:]  # 移除 'PRESET_FILTER_' 前缀
                filter_dict = {}
                for pair in value.split(","):
                    if ":" in pair:
                        k, v = pair.strip().split(":", 1)
                        filter_dict[k] = (
                            self._parse_number(v)
                            if k in ["min_rent", "max_rent"]
                            else v
                        )
                presets[filter_name] = filter_dict

        return presets


# =============================================================================
# 配置实例
# =============================================================================

# Bark推送配置
BARK_CONFIG = BarkConfig()

# 向后兼容
BARK_KEY = BARK_CONFIG.KEY
PUSH_GROUP = BARK_CONFIG.DEFAULT_GROUP

# 推送时间控制配置
PUSH_TIME_CONFIG = PushTimeConfig()

# 向后兼容
PUSH_TIME_CONTROL_ENABLED = PUSH_TIME_CONFIG.ENABLED
PUSH_START_HOUR = PUSH_TIME_CONFIG.START_HOUR
PUSH_END_HOUR = PUSH_TIME_CONFIG.END_HOUR
SHANGHAI_TIMEZONE = PUSH_TIME_CONFIG.TIMEZONE

# 爬虫配置
CRAWLER_CONFIG = CrawlerConfig()

# 向后兼容
CRAWLER_DELAY = CRAWLER_CONFIG.DELAY
MAX_RETRIES = CRAWLER_CONFIG.MAX_RETRIES

# 数据配置
DATA_CONFIG = DataConfig()

# 向后兼容
DATA_DIR = DATA_CONFIG.DATA_DIR
LOGS_DIR = DATA_CONFIG.LOGS_DIR

# 筛选配置
FILTER_CONFIG = FilterConfig()

# 向后兼容
DEFAULT_FILTERS = FILTER_CONFIG.DEFAULT_FILTERS
PRESET_FILTERS = FILTER_CONFIG.PRESET_FILTERS
ENABLED_PRESET_FILTERS = FILTER_CONFIG.ENABLED_PRESET_FILTERS

# =============================================================================
# 其他配置（保持向后兼容）
# =============================================================================

# 测试推送配置
TEST_PUSH_ENABLED = os.getenv("TEST_PUSH_ENABLED", "true").lower() == "true"
TEST_PUSH_INTERVAL = int(os.getenv("TEST_PUSH_INTERVAL", "3600"))

# 特定监控地点设置
MONITORED_LOCATIONS = os.getenv(
    "MONITORED_LOCATIONS", "张江,唐镇,曹路,合庆,金桥,陆家嘴,金杨新村,洋泾,花木,康桥"
).split(",")

# 特定地点推送配置
LOCATION_BARK_KEYS = {}  # 可以通过环境变量配置

# 特定房型监控
MONITORED_HOUSE_TYPES = []  # 可以通过环境变量配置

# 推送分组配置
PUSH_GROUPS = {
    "default": PUSH_GROUP,
    "金桥": f"{PUSH_GROUP}-金桥",
    "张江": f"{PUSH_GROUP}-张江",
    "唐镇": f"{PUSH_GROUP}-唐镇",
    "低价房": f"{PUSH_GROUP}-低价",
    "监控": f"{PUSH_GROUP}-监控",
    "测试": f"{PUSH_GROUP}-测试",
}

# 测试推送配置
TEST_PUSH_ENABLED = True  # 是否启用测试推送
TEST_PUSH_INTERVAL = 3600  # 测试推送间隔（秒），默认1小时

# 推送时间控制（上海时间）
PUSH_TIME_CONTROL_ENABLED = True  # 是否启用推送时间控制
PUSH_START_HOUR = 8  # 推送开始时间（24小时制）
PUSH_END_HOUR = 11  # 推送结束时间（24小时制）
SHANGHAI_TIMEZONE = "Asia/Shanghai"  # 上海时区

# 爬虫设置
CRAWLER_DELAY = 5  # 页面加载延迟（秒）
MAX_RETRIES = 3  # 最大重试次数

# 数据存储设置
DATA_DIR = "data/"
LOGS_DIR = "logs/"

# 筛选条件设置
DEFAULT_FILTERS = {
    "min_rent": None,  # 最低租金(None表示不限制)
    "max_rent": 5000,  # 最高租金(None表示不限制)
    "area": None,  # 区域关键词(None表示不限制)
    "house_type": None,  # 房型关键词(None表示不限制)
}

# 预设筛选方案
PRESET_FILTERS = {
    "金桥低价": {
        "area": "金桥",
        "max_rent": 3000,
        "min_rent": None,
        "house_type": None,
    },
    "张江低价": {
        "area": "张江",
        "max_rent": 3000,
        "min_rent": None,
        "house_type": None,
    },
    "唐镇低价": {
        "area": "唐镇",
        "max_rent": 3000,
        "min_rent": None,
        "house_type": None,
    },
    "金桥": {"area": "金桥", "max_rent": None, "min_rent": None, "house_type": None},
    "低价房": {"area": None, "max_rent": 3000, "min_rent": None, "house_type": None},
}

# 启用的筛选方案（支持多个，用逗号分隔）
ENABLED_PRESET_FILTERS = ["金桥低价"]

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
    "康桥",
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
