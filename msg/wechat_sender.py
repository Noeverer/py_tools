#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立的微信推送模块
不依赖项目其他代码，可以直接调用推送功能
"""

import requests
import json
import re
from urllib.parse import quote
from typing import List, Dict, Any, Optional


class WeChatSender:
    """
    微信推送服务类
    支持Bark推送服务
    """
    
    def __init__(self, bark_key: str, group: str = "通知"):
        """
        初始化推送服务
        
        Args:
            bark_key (str): Bark推送服务的密钥
            group (str): 推送分组
        """
        self.bark_key = bark_key
        self.group = group
        self.base_url = "https://api.day.app"
        
    def clean_text(self, text: str) -> str:
        """
        清理文本中的特殊字符，只保留中文、英文和数字
        
        Args:
            text (str): 原始文本
            
        Returns:
            str: 清理后的文本
        """
        if text:
            return re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', str(text))
        return ""
    
    def authenticate(self) -> bool:
        """
        验证推送服务密钥是否有效
        
        Returns:
            bool: 验证是否成功
        """
        if not self.bark_key or self.bark_key == "vWYmRcVLnFKWJP5AJKWADU":
            print("错误: 请提供有效的Bark推送密钥")
            return False
            
        try:
            # 发送测试消息验证密钥
            test_msg = quote("推送服务连接测试")
            url = f"{self.base_url}/{self.bark_key}/{test_msg}?group={self.group}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print("Bark推送服务验证成功")
                return True
            else:
                print(f"Bark推送服务验证失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            print(f"Bark推送服务验证出错: {e}")
            return False
    
    def send_message(self, message: str, title: str = "") -> bool:
        """
        发送单条消息
        
        Args:
            message (str): 消息内容
            title (str): 消息标题（可选）
            
        Returns:
            bool: 是否发送成功
        """
        if not self.bark_key:
            print("错误: 未配置推送密钥")
            return False
            
        try:
            # 清理并编码消息
            clean_msg = self.clean_text(message)
            if title:
                clean_title = self.clean_text(title)
                encoded_title = quote(clean_title)
                encoded_msg = quote(clean_msg)
                url = f"{self.base_url}/{self.bark_key}/{encoded_title}/{encoded_msg}?group={self.group}"
            else:
                encoded_msg = quote(clean_msg)
                url = f"{self.base_url}/{self.bark_key}/{encoded_msg}?group={self.group}"
            
            # 添加请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # 发送请求
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"消息推送成功: {message[:30]}...")
                return True
            else:
                print(f"消息推送失败，状态码: {response.status_code}")
                return False
        except Exception as e:
            print(f"消息推送出错: {e}")
            return False
    
    def send_house_data(self, house_list: List[Dict[str, Any]]) -> bool:
        """
        发送房源信息列表
        
        Args:
            house_list (List[Dict[str, Any]]): 房源信息列表
            
        Returns:
            bool: 是否发送成功
        """
        if not house_list:
            return self.send_message("未查询到房源信息")
        
        # 构造推送消息
        message_lines = [f"【最新房源信息】(共{len(house_list)}条)"]
        for i, house in enumerate(house_list, 1):
            # 构造房源信息
            info_parts = []
            
            # 根据常见的房源字段构造信息
            if house.get('house_name'):
                info_parts.append(str(house['house_name']))
            elif house.get('location'):
                info_parts.append(str(house['location']))
                
            if house.get('house_type'):
                info_parts.append(str(house['house_type']))
            elif house.get('room_info'):
                info_parts.append(str(house['room_info']))
                
            if house.get('rent_monoey'):
                info_parts.append(f"租金:{house['rent_monoey']}")
            elif house.get('rent'):
                info_parts.append(f"租金:{house['rent']}")
                
            if house.get('area'):
                info_parts.append(f"面积:{house['area']}")
                
            if house.get('last_update_date'):
                info_parts.append(f"更新:{str(house['last_update_date'])[:10]}")
            elif house.get('create_time'):
                info_parts.append(f"时间:{str(house['create_time'])[:10]}")
            
            house_info = " | ".join(info_parts)
            clean_house_info = self.clean_text(house_info)
            message_lines.append(f"{i}. {clean_house_info}")
        
        full_message = "\n".join(message_lines)
        return self.send_message(full_message, "房源信息推送")


def main():
    """
    独立使用的示例
    """
    # 配置你的Bark Key
    BARK_KEY = "vWYmRcVLnFKWJP5AJKWADU"
    
    # 创建推送服务实例
    sender = WeChatSender(BARK_KEY, "公租房通知")
    
    # 验证服务
    if not sender.authenticate():
        print("推送服务验证失败")
        return
    
    # 示例1: 发送简单消息
    sender.send_message("这是一条测试消息", "测试标题")
    
    # 示例2: 发送房源数据
    sample_houses = [
        {
            "house_name": "张江公寓A栋",
            "house_type": "1室1厅",
            "rent_monoey": "2500元/月",
            "area": "50平方米",
            "last_update_date": "2023-10-01"
        },
        {
            "house_name": "陆家嘴花园B区",
            "house_type": "2室1厅",
            "rent_monoey": "4500元/月",
            "area": "80平方米",
            "last_update_date": "2023-10-02"
        }
    ]
    
    # 发送房源信息
    sender.send_house_data(sample_houses)


if __name__ == "__main__":
    main()