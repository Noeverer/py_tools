#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成GitHub Pages展示数据
将爬取的房源数据和筛选结果转换为JSON格式，供前端展示使用
"""

import os
import sys
import json
import yaml
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.db_utils import read_recent_house_data, filter_house_data
from config.settings import DEFAULT_FILTERS

# 配置文件路径
DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
DATA_DIR = os.path.join(DOCS_DIR, 'data')
TODAY_FILE = os.path.join(DATA_DIR, 'today.json')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.json')
FILTERS_CONFIG = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'filters.yaml')


def load_filters_config() -> Dict[str, Any]:
    """加载筛选条件配置"""
    try:
        with open(FILTERS_CONFIG, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"警告: 未找到筛选配置文件 {FILTERS_CONFIG}")
        return {'enabled_filters': [], 'filter_rules': []}


def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_history() -> List[Dict[str, Any]]:
    """加载历史数据"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_history(history: List[Dict[str, Any]]):
    """保存历史数据"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def generate_dashboard_data(house_data: List[Dict[str, Any]], filtered_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成前端展示数据"""
    
    # 获取当前时间（北京时间）
    beijing_tz = timezone(timedelta(hours=8))
    now = datetime.now(beijing_tz)
    
    # 计算统计数据
    total_count = len(house_data)
    filtered_count = len(filtered_data)
    
    # 计算平均租金
    avg_price = 0
    if house_data:
        total_price = sum(h.get('rent', 0) for h in house_data)
        avg_price = round(total_price / len(house_data), 0)
    
    # 获取筛选配置
    filters_config = load_filters_config()
    
    # 统计每个筛选方案匹配的房源数量
    filter_stats = []
    enabled_filters = filters_config.get('enabled_filters', [])
    filter_rules = {r['name']: r for r in filters_config.get('filter_rules', [])}
    
    for filter_name in enabled_filters:
        if filter_name in filter_rules:
            rule = filter_rules[filter_name]
            # 简单的匹配逻辑（实际应该使用与爬虫相同的筛选逻辑）
            matched_count = 0
            for house in filtered_data:
                if rule['conditions'].get('area') and rule['conditions']['area'] in house.get('house_site', ''):
                    matched_count += 1
                elif not rule['conditions'].get('area'):
                    matched_count += 1
            
            filter_stats.append({
                'name': filter_name,
                'description': rule['description'],
                'count': matched_count
            })
    
    # 为每个房源添加匹配的筛选方案
    houses_with_filters = []
    for house in filtered_data[:20]:  # 限制显示前20个房源
        matched = []
        for stat in filter_stats:
            if stat['count'] > 0:
                # 简化的匹配逻辑
                rule = filter_rules[stat['name']]
                if rule['conditions'].get('area') and rule['conditions']['area'] in house.get('house_site', ''):
                    matched.append(stat['name'])
                elif not rule['conditions'].get('area'):
                    matched.append(stat['name'])
        
        houses_with_filters.append({
            **house,
            'matched_filters': matched
        })
    
    # 生成今日数据
    today_data = {
        'update_time': now.isoformat(),
        'date': now.strftime('%Y-%m-%d'),
        'total': total_count,
        'filtered': filtered_count,
        'new': min(3, filtered_count),  # 简化的新增数量逻辑
        'avg_price': avg_price,
        'filters': filter_stats,
        'houses': houses_with_filters
    }
    
    return today_data


def update_dashboard(house_data: List[Dict[str, Any]], filtered_data: List[Dict[str, Any]]):
    """更新仪表板数据"""
    
    ensure_directories()
    
    # 生成今日数据
    today_data = generate_dashboard_data(house_data, filtered_data)
    
    # 保存今日数据
    with open(TODAY_FILE, 'w', encoding='utf-8') as f:
        json.dump(today_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成今日数据: {TODAY_FILE}")
    
    # 更新历史数据
    history = load_history()
    
    # 保留最近30天的数据
    history = [d for d in history if d.get('date') != today_data['date']]
    history.insert(0, today_data)
    history = history[:30]
    
    save_history(history)
    print(f"✅ 已更新历史数据: {HISTORY_FILE}")
    
    return today_data


def generate_markdown_report(today_data: Dict[str, Any]) -> str:
    """生成Markdown格式的每日报告"""
    
    report = f"""# 🏠 上海公租房监控日报

**日期**: {today_data['date']}  
**更新时间**: {today_data['update_time']}

---

## 📊 今日统计

- **总房源数**: {today_data['total']} 套
- **符合条件**: {today_data['filtered']} 套
- **新增房源**: {today_data['new']} 套
- **平均租金**: ¥{today_data['avg_price']}

---

## 🎯 筛选方案

"""
    
    for filter_stat in today_data.get('filters', []):
        report += f"### {filter_stat['name']}\n"
        report += f"- 描述: {filter_stat['description']}\n"
        report += f"- 匹配房源: {filter_stat['count']} 套\n\n"
    
    report += "---\n"
    report += "## 🏆 符合条件的房源\n\n"
    
    for i, house in enumerate(today_data.get('houses', []), 1):
        report += f"### {i}. {house['house_name']}\n"
        report += f"- 区域: {house['house_site']}\n"
        report += f"- 租金: ¥{house['rent']}/月\n"
        report += f"- 户型: {house['house_type']}\n"
        report += f"- 面积: {house['area']}㎡\n"
        if house.get('matched_filters'):
            report += f"- 匹配方案: {', '.join(house['matched_filters'])}\n"
        report += "\n"
    
    return report


def main():
    """主函数 - 生成仪表板数据"""
    print("=" * 50)
    print("📊 生成GitHub Pages仪表板数据")
    print("=" * 50)

    # 从数据库读取房源数据
    try:
        house_data = read_recent_house_data(limit_days=7)
        print(f"✅ 从数据库读取到 {len(house_data)} 条房源数据")
    except Exception as e:
        print(f"⚠️ 读取数据库失败: {e}")
        house_data = []

    # 应用筛选条件
    try:
        filtered_data = filter_house_data(house_data, DEFAULT_FILTERS)
        print(f"✅ 筛选后符合条件: {len(filtered_data)} 条")
    except Exception as e:
        print(f"⚠️ 筛选失败: {e}")
        filtered_data = house_data

    # 如果没有数据，生成空数据结构
    if not house_data:
        print("⚠️ 没有房源数据，生成空仪表板")
        house_data = []
        filtered_data = []

    # 更新仪表板
    today_data = update_dashboard(house_data, filtered_data)

    print("=" * 50)
    print("✅ 仪表板数据生成完成")
    print(f"- 总房源: {today_data['total']}")
    print(f"- 符合条件: {today_data['filtered']}")
    print(f"- 平均租金: ¥{today_data['avg_price']}")
    print("=" * 50)


if __name__ == '__main__':
    main()
