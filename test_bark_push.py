#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Bark推送功能
"""

from services.notification_service import send_test_push, send_notification

def test_bark_push():
    """测试Bark推送功能"""
    print("开始测试Bark推送功能...")
    
    # 发送测试推送
    print("\n1. 发送测试推送...")
    send_test_push()
    
    # 模拟一些房源数据用于测试
    print("\n2. 发送模拟房源数据推送...")
    mock_house_data = [
        {
            'house_name': '唐镇新苑',
            'house_type': '2室1厅',
            'rent': '3500元/月',
            'area': '80㎡',
            'floor': '15/18层',
            'house_site': '浦东新区唐镇',
            'applicant_count': 245
        },
        {
            'house_name': '金桥国际公寓',
            'house_type': '1室0厅',
            'rent': '2800元/月',
            'area': '55㎡',
            'floor': '8/20层',
            'house_site': '浦东新区金桥',
            'applicant_count': 189
        }
    ]
    
    # 发送房源信息推送
    send_notification(mock_house_data)
    
    print("\nBark推送功能测试完成！")

if __name__ == "__main__":
    test_bark_push()