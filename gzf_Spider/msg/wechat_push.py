#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从MySQL数据库查询房屋信息并推送到微信
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import requests
import re
from src.conndb import conn_db, exe_query, conn_close
from datetime import datetime


def clean_text(text):
    """
    清理文本中的特殊字符，只保留中文、英文和数字
    """
    if text:
        return re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', str(text))
    return ""


def get_house_data(limit=10):
    """
    从数据库获取最新的房屋信息
    
    Args:
        limit (int): 获取记录的数量，默认10条
    
    Returns:
        list: 房屋信息列表
    """
    conn, cur = conn_db()
    try:
        # 查询最新的房屋数据
        sql = f"SELECT * FROM HouseData ORDER BY create_time DESC LIMIT {limit}"
        cur = exe_query(cur, sql)
        results = cur.fetchall()
        
        # 获取列名
        columns = [desc[0] for desc in cur.description]
        
        # 将结果转换为字典列表
        house_list = []
        for row in results:
            house_dict = dict(zip(columns, row))
            house_list.append(house_dict)
            
        return house_list
    except Exception as e:
        print(f"查询数据库出错: {e}")
        return []
    finally:
        conn_close(conn, cur)


def push_to_wechat(house_data, key, group="公租房"):
    """
    推送房屋信息到微信
    
    Args:
        house_data (list): 房屋信息列表
        key (str): Bark推送key
        group (str): 分组名称
    """
    if not house_data:
        print("没有房屋数据需要推送")
        return
        
    # 构造推送消息
    message_lines = ["【最新房源信息】"]
    for house in house_data:
        # 根据数据库字段构造信息（字段名可能需要根据实际情况调整）
        info_parts = []
        if house.get('location'):
            info_parts.append(str(house['location']))
        if house.get('room_info'):
            info_parts.append(str(house['room_info']))
        if house.get('rent'):
            info_parts.append(f"租金:{house['rent']}")
        if house.get('create_time'):
            info_parts.append(f"时间:{house['create_time']}")
            
        house_info = "<>".join(info_parts)
        clean_house_info = clean_text(house_info)
        message_lines.append(clean_house_info)
    
    full_message = "\\n".join(message_lines)
    
    # 发送推送请求
    try:
        url = f"https://api.day.app/{key}/{full_message}?group={group}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"推送成功: {len(house_data)} 条房源信息已推送")
        else:
            print(f"推送失败: {response.status_code}")
    except Exception as e:
        print(f"推送过程中出错: {e}")


def push_single_message(message, key, group="公租房通知"):
    """
    推送单条消息到微信
    
    Args:
        message (str): 要推送的消息
        key (str): Bark推送key
        group (str): 分组名称
    """
    try:
        clean_msg = clean_text(message)
        url = f"https://api.day.app/{key}/{clean_msg}?group={group}"
        response = requests.get(url)
        if response.status_code == 200:
            print("消息推送成功")
        else:
            print(f"消息推送失败: {response.status_code}")
    except Exception as e:
        print(f"推送过程中出错: {e}")


if __name__ == "__main__":
    # 示例用法
    print("开始查询房源信息...")
    
    # 获取房屋数据
    houses = get_house_data(5)
    
    if houses:
        print(f"查询到 {len(houses)} 条房源信息")
        # 这里需要替换为你的Bark Key
        BARK_KEY = "your_bark_key_here"
        # push_to_wechat(houses, BARK_KEY)
    else:
        print("未查询到房源信息")
        
    # 测试推送单条消息
    # push_single_message("测试推送消息", BARK_KEY)