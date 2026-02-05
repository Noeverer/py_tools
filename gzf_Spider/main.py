#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公租房信息爬取与推送系统 - 主入口
"""

import os
import sys
from datetime import datetime
from spiders.house_spider import main as spider_main
from utils.db_utils import read_recent_house_data, filter_house_data
from config.settings import DEFAULT_FILTERS
from services.notification_service import authenticate_bark, push_single_message
from config.settings import BARK_KEY


def main():
    """
    主函数
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行房源信息爬取任务...")

    # 验证推送服务
    if not authenticate_bark(BARK_KEY):
        print("推送服务验证失败，但继续执行爬虫任务")

    # 执行爬虫
    print("开始爬取房源信息...")
    house_data = spider_main()

    if house_data:
        print(f"成功获取到 {len(house_data)} 条房源信息")

        # 可以选择应用过滤器
        # filtered_data = filter_house_data(house_data, DEFAULT_FILTERS)
        # print(f"过滤后剩余 {len(filtered_data)} 条房源信息")
    else:
        print("未获取到房源信息")
        push_single_message("未获取到新的房源信息")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 任务执行完成")


if __name__ == "__main__":
    main()