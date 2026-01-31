#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立的房源数据查询和推送脚本
不依赖项目其他代码，可独立运行
"""

import pymysql
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from wechat_sender import WeChatSender


# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Liu@06027',
    'database': 'gzf',
    'charset': 'utf8'
}

# 微信推送配置
BARK_KEY = "your_bark_key_here"  # 请替换为你的Bark推送密钥
PUSH_GROUP = "公租房通知"


def connect_database():
    """
    连接数据库
    
    Returns:
        tuple: (connection, cursor) 数据库连接和游标
    """
    try:
        conn = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            db=DB_CONFIG['database'],
            charset=DB_CONFIG['charset']
        )
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None, None


def get_house_data(limit: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    从数据库获取房源信息
    
    Args:
        limit (int): 获取记录数量
        filters (dict): 筛选条件
        
    Returns:
        List[Dict[str, Any]]: 房源信息列表
    """
    conn, cur = connect_database()
    if not conn or not cur:
        return []
    
    try:
        # 基础查询SQL
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
            # 只推送未被选走的房源
            if filters.get('available_only', True):
                conditions += " AND choosed != '已选'"
                
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


def main():
    """
    主函数
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行房源信息推送任务...")
    
    # 创建推送服务实例
    sender = WeChatSender(BARK_KEY, PUSH_GROUP)
    
    # 验证推送服务
    if not sender.authenticate():
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
    houses = get_house_data(10, filters)
    
    if houses:
        print(f"查询到 {len(houses)} 条符合条件的房源信息")
        # 推送房源信息
        success = sender.send_house_data(houses)
        if success:
            print("房源信息推送成功")
        else:
            print("房源信息推送失败")
    else:
        print("未查询到符合条件的房源信息")
        sender.send_message("未查询到符合条件的房源信息")
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 任务执行完成")


if __name__ == "__main__":
    main()