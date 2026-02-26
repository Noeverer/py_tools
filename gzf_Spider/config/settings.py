#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件 - 从环境变量读取配置
详细配置说明请参考 .env.example 或项目 README
"""

import os
from typing import Dict, List, Optional


class BarkConfig:
    """Bark推送配置"""

    def __init__(self):
        self.KEY = os.getenv("BARK_KEY", "your_bark_key_here")
        self.DEFAULT_GROUP = os.getenv("BARK_DEFAULT_GROUP", "公租房通知")
        self.SERVER_URL = os.getenv("BARK_SERVER_URL", "https://api.day.app")
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
        self.TIME_SLOTS = self._parse_time_slots(os.getenv("PUSH_TIME_SLOTS", "8-11"))

    def _parse_time_slots(self, slots_str: str) -> List[tuple]:
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
        self.TARGET_URL = os.getenv(
            "CRAWLER_TARGET_URL", "https://select.pdgzf.com/houseLists"
        )
        self.HEADLESS = os.getenv("CRAWLER_HEADLESS", "true").lower() == "true"
        self.NO_SANDBOX = os.getenv("CRAWLER_NO_SANDBOX", "true").lower() == "true"


class DataConfig:
    """数据存储配置"""

    def __init__(self):
        self.DATA_DIR = os.getenv("DATA_DIR", "data/")
        self.LOGS_DIR = os.getenv("LOGS_DIR", "logs/")
        self.BACKUP_DAYS = int(os.getenv("DATA_BACKUP_DAYS", "30"))
        self.MAX_FILE_SIZE = int(os.getenv("DATA_MAX_FILE_SIZE", "10485760"))


class FilterConfig:
    """筛选配置"""

    def __init__(self):
        self.DEFAULT_FILTERS = {
            "min_rent": self._parse_number(os.getenv("FILTER_MIN_RENT")),
            "max_rent": self._parse_number(os.getenv("FILTER_MAX_RENT", "5000")),
            "area": os.getenv("FILTER_AREA") or None,
            "house_type": os.getenv("FILTER_HOUSE_TYPE") or None,
        }
        self.PRESET_FILTERS = self._load_preset_filters()
        enabled_filters = os.getenv("ENABLED_PRESET_FILTERS", "金桥低价")
        self.ENABLED_PRESET_FILTERS = [
            f.strip() for f in enabled_filters.split(",") if f.strip()
        ]

    def _parse_number(self, value: Optional[str]) -> Optional[float]:
        if value is None or value.lower() == "none":
            return None
        try:
            return float(value)
        except ValueError:
            return None

    def _load_preset_filters(self) -> Dict[str, Dict]:
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
        for key, value in os.environ.items():
            if key.startswith("PRESET_FILTER_"):
                filter_name = key[14:]
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


BARK_CONFIG = BarkConfig()
BARK_KEY = BARK_CONFIG.KEY
PUSH_GROUP = BARK_CONFIG.DEFAULT_GROUP

PUSH_TIME_CONFIG = PushTimeConfig()
PUSH_TIME_CONTROL_ENABLED = PUSH_TIME_CONFIG.ENABLED
PUSH_START_HOUR = PUSH_TIME_CONFIG.START_HOUR
PUSH_END_HOUR = PUSH_TIME_CONFIG.END_HOUR
SHANGHAI_TIMEZONE = PUSH_TIME_CONFIG.TIMEZONE

CRAWLER_CONFIG = CrawlerConfig()
CRAWLER_DELAY = CRAWLER_CONFIG.DELAY
MAX_RETRIES = CRAWLER_CONFIG.MAX_RETRIES

DATA_CONFIG = DataConfig()
DATA_DIR = DATA_CONFIG.DATA_DIR
LOGS_DIR = DATA_CONFIG.LOGS_DIR

FILTER_CONFIG = FilterConfig()
DEFAULT_FILTERS = FILTER_CONFIG.DEFAULT_FILTERS
PRESET_FILTERS = FILTER_CONFIG.PRESET_FILTERS
ENABLED_PRESET_FILTERS = FILTER_CONFIG.ENABLED_PRESET_FILTERS

TEST_PUSH_ENABLED = os.getenv("TEST_PUSH_ENABLED", "true").lower() == "true"
TEST_PUSH_INTERVAL = int(os.getenv("TEST_PUSH_INTERVAL", "3600"))

MONITORED_LOCATIONS = os.getenv(
    "MONITORED_LOCATIONS", "张江,唐镇,曹路,合庆,金桥,陆家嘴,金杨新村,洋泾,花木,康桥"
).split(",")

LOCATION_BARK_KEYS = {}
MONITORED_HOUSE_TYPES = (
    os.getenv("MONITORED_HOUSE_TYPES", "").split(",")
    if os.getenv("MONITORED_HOUSE_TYPES")
    else []
)

PUSH_GROUPS = {
    "default": PUSH_GROUP,
    "金桥": f"{PUSH_GROUP}-金桥",
    "张江": f"{PUSH_GROUP}-张江",
    "唐镇": f"{PUSH_GROUP}-唐镇",
    "低价房": f"{PUSH_GROUP}-低价",
    "监控": f"{PUSH_GROUP}-监控",
    "测试": f"{PUSH_GROUP}-测试",
}
