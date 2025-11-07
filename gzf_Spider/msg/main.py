#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序文件 - 从MySQL数据库查询房屋信息并推送到微信
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pymysql
import requests
import re
from datetime import datetime
from config import DB_CONFIG, BARK_KEY, PUSH_GROUP, QUERY_LIMIT


def clean_text(text):
    """
    清理文本中的特殊字符，只保留中文、英文和数字
    """
    if text:
        return re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', str(text))
    return ""


def get_house_data(limit=QUERY_LIMIT, filters=None):
    """
    从数据库获取最新的房屋信息，支持筛选条件
    
    Args:
        limit (int): 获取记录的数量
        filters (dict): 筛选条件，例如:
            {
                'min_rent': 1000,     # 最低租金
                'max_rent': 3000,     # 最高租金
                'area': '张江镇',      # 区域关键词
                'house_type': '1室1厅' # 房型
            }
    
    Returns:
        list: 房屋信息列表
    """
    # 建立数据库连接
    conn = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        passwd=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        charset=DB_CONFIG['charset']
    )
    cur = conn.cursor()
    
    try:
        # 构建查询SQL
        base_sql = """
        SELECT house_id, house_name, house_site, rent_monoey, 
               choose_start_time, choose_end_time, house_type, 
               choosed, foold, area, last_update_date
        FROM HouseData 
        WHERE 1=1
        """
        
        conditions = ""
        params = []
        
        # 添加筛选条件
        if filters:
            # 租金范围筛选
            if 'min_rent' in filters and filters['min_rent']:
                conditions += " AND CAST(rent_monoey AS DECIMAL) >= %s"
                params.append(filters['min_rent'])
                
            if 'max_rent' in filters and filters['max_rent']:
                conditions += " AND CAST(rent_monoey AS DECIMAL) <= %s"
                params.append(filters['max_rent'])
                
            # 区域关键词筛选
            if 'area' in filters and filters['area']:
                conditions += " AND (house_name LIKE %s OR house_site LIKE %s)"
                params.extend([f"%{filters['area']}%", f"%{filters['area']}%"])
                
            # 房型筛选
            if 'house_type' in filters and filters['house_type']:
                conditions += " AND house_type LIKE %s"
                params.append(f"%{filters['house_type']}%")
                
            # 可选房源筛选（未被选走的）
            if filters.get('available_only', True):
                conditions += " AND choosed != '已选'"
        
        # 按时间倒序排列
        order_by = " ORDER BY last_update_date DESC "
        
        # 限制返回数量
        limit_clause = " LIMIT %s"
        params.append(limit)
        
        # 组合完整SQL
        sql = base_sql + conditions + order_by + limit_clause
        
        # 执行查询
        cur.execute(sql, params)
        results = cur.fetchall()
        
        # 获取列名
        columns = [desc[0] for desc in cur.description]
        
        # 将结果转换为字典列表
        house_list = []
        for row in results:
            house_dict = dict(zip(columns, row))
            # 处理时间格式
            if isinstance(house_dict.get('last_update_date'), datetime):
                house_dict['last_update_date'] = house_dict['last_update_date'].strftime('%Y-%m-%d %H:%M:%S')
            house_list.append(house_dict)
            
        return house_list
    except Exception as e:
        print(f"查询数据库出错: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def push_to_wechat(house_data, key=BARK_KEY, group=PUSH_GROUP):
    """
    推送房屋信息到微信
    
    Args:
        house_data (list): 房屋信息列表
        key (str): Bark推送key
        group (str): 分组名称
    """
    if not house_data:
        print("没有房屋数据需要推送")
        push_single_message("未查询到符合条件的房源信息", key, group)
        return
        
    # 构造推送消息
    message_lines = [f"【最新房源信息】(共{len(house_data)}条)"]
    for i, house in enumerate(house_data, 1):
        # 构造房源信息
        info_parts = []
        if house.get('house_name'):
            info_parts.append(str(house['house_name']))
        if house.get('house_type'):
            info_parts.append(str(house['house_type']))
        if house.get('rent_monoey'):
            info_parts.append(f"租金:{house['rent_monoey']}")
        if house.get('area'):
            info_parts.append(f"面积:{house['area']}")
        if house.get('last_update_date'):
            info_parts.append(f"更新:{house['last_update_date'][:10]}")
            
        house_info = " | ".join(info_parts)
        clean_house_info = clean_text(house_info)
        message_lines.append(f"{i}. {clean_house_info}")
    
    full_message = "\\n".join(message_lines)
    
    # 发送推送请求
    push_single_message(full_message, key, group)


def push_single_message(message, key=BARK_KEY, group=PUSH_GROUP):
    """
    推送单条消息到微信
    
    Args:
        message (str): 要推送的消息
        key (str): Bark推送key
        group (str): 分组名称
    """
    if not key or key == "your_bark_key_here":
        print("请先在config.py中配置BARK_KEY")
        return
        
    try:
        clean_msg = clean_text(message)
        # URL编码
        encoded_msg = requests.utils.quote(clean_msg)
        url = f"https://api.day.app/{key}/{encoded_msg}?group={group}"
        
        # 添加headers模拟真实请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"消息推送成功: {message[:50]}...")
        else:
            print(f"消息推送失败: {response.status_code}")
    except Exception as e:
        print(f"推送过程中出错: {e}")


def authenticate_bark(key):
    """
    验证Bark推送服务密钥是否有效
    
    Args:
        key (str): Bark推送key
        
    Returns:
        bool: 验证是否成功
    """
    if not key or key == "your_bark_key_here":
        print("错误: 请先配置有效的BARK_KEY")
        return False
        
    try:
        # 发送测试消息验证密钥
        test_msg = requests.utils.quote("推送服务连接测试")
        url = f"https://api.day.app/{key}/{test_msg}?group=测试"
        
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


def main():
    """
    主函数
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行房源信息推送任务...")
    
    # 验证推送服务
    if not authenticate_bark(BARK_KEY):
        print("推送服务验证失败，终止执行")
        return
    
    # 定义筛选条件
    filters = {
        'available_only': True,  # 只推送未被选走的房源
        # 'min_rent': 1000,      # 最低租金（可选）
        # 'max_rent': 3000,      # 最高租金（可选）
        # 'area': '张江',         # 区域关键词（可选）
        # 'house_type': '1室'     # 房型关键词（可选）
    }
    
    # 获取房屋数据
    houses = get_house_data(QUERY_LIMIT, filters)
    
    if houses:
        print(f"查询到 {len(houses)} 条符合条件的房源信息")
        push_to_wechat(houses)
    else:
        print("未查询到符合条件的房源信息")
        push_single_message("未查询到符合条件的房源信息")
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 任务执行完成")


if __name__ == "__main__":
    main()