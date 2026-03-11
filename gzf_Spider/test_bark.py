#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Bark推送功能
"""

import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

BARK_KEY = os.getenv("BARK_KEY")
BARK_SERVER_URL = os.getenv("BARK_SERVER_URL", "https://api.day.app")

print("=" * 50)
print("🧪 测试Bark推送功能")
print("=" * 50)
print(f"BARK_KEY: {BARK_KEY}")
print(f"BARK_SERVER_URL: {BARK_SERVER_URL}")
print()

if not BARK_KEY:
    print("❌ BARK_KEY未配置！")
    print("请在.env文件中设置BARK_KEY")
    exit(1)

# 测试推送1: 基本推送
print("📤 发送测试推送1...")
test_url1 = f"{BARK_SERVER_URL}/{BARK_KEY}/公租房监控测试"
try:
    response1 = requests.get(test_url1, timeout=10)
    print(f"✅ 推送1成功! Status: {response1.status_code}")
    print(f"   响应: {response1.text[:200]}")
except Exception as e:
    print(f"❌ 推送1失败: {e}")

print()

# 测试推送2: 带分组的推送
print("📤 发送测试推送2（带分组）...")
test_url2 = f"{BARK_SERVER_URL}/{BARK_KEY}/公租房监控测试2?group=公租房通知&sound=telegraph"
try:
    response2 = requests.get(test_url2, timeout=10)
    print(f"✅ 推送2成功! Status: {response2.status_code}")
    print(f"   响应: {response2.text[:200]}")
except Exception as e:
    print(f"❌ 推送2失败: {e}")

print()
print("=" * 50)
print("✅ 测试完成！请检查你的iPhone是否收到推送通知")
print("=" * 50)
