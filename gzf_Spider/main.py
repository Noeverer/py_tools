#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公租房信息爬取与推送系统 - 主入口
支持多种运行模式和配置选项
"""

import os
import sys
import argparse
from datetime import datetime

# 确保模块路径正确
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from spiders.house_spider import main as spider_main
from utils.db_utils import read_recent_house_data, filter_house_data
from config.settings import DEFAULT_FILTERS
from services.notification_service import authenticate_bark, push_single_message, send_notification
from config.settings import BARK_KEY, ENABLED_PRESET_FILTERS
import subprocess


def main():
    """
    主函数 - 支持命令行参数控制运行模式
    """
    parser = argparse.ArgumentParser(description="公租房信息爬取与推送系统")
    parser.add_argument(
        "--mode",
        choices=["normal", "debug", "test"],
        default="normal",
        help="运行模式: normal(正常), debug(调试), test(测试)",
    )
    args = parser.parse_args()

    print("=" * 50)
    print("🏠 上海公租房信息监控平台")
    print(f"运行模式: {args.mode}")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 测试模式：仅检查环境和服务
    if args.mode == "test":
        print("🧪 测试模式：检查环境和服务...")
        if authenticate_bark(BARK_KEY):
            print("✅ Bark推送服务正常")
        else:
            print("❌ Bark推送服务异常")
        print("🔧 环境检查完成")
        return

    # 验证推送服务
    print("🔍 验证推送服务...")
    if not authenticate_bark(BARK_KEY):
        print("⚠️ 推送服务验证失败，但继续执行爬虫任务")

    # 执行爬虫
    print("🕷️ 开始爬取房源信息...")
    house_data = spider_main()

    if house_data:
        print(f"✅ 成功获取到 {len(house_data)} 条房源信息")

        # 显示启用的筛选方案
        print(f"📋 启用的筛选方案: {', '.join(ENABLED_PRESET_FILTERS)}")

        # 生成仪表板数据（包含所有筛选结果）
        print("📊 生成仪表板数据...")
        try:
            subprocess.run([sys.executable, 'scripts/generate_dashboard.py'], check=True, cwd=current_dir)
            print("✅ 仪表板数据生成成功")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ 生成仪表板数据失败: {e}")

        # 发送推送通知（使用预设筛选方案）
        print("📤 发送推送通知...")
        send_notification(house_data)
        print("✅ 推送通知发送完成")
    else:
        print("❌ 未获取到房源信息")
        if args.mode != "debug":
            push_single_message("未获取到新的房源信息")

    print(f"🏁 任务执行完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
