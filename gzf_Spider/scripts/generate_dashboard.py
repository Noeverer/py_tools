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

    # 计算平均租金（需要从租金字符串中提取数字）
    avg_price = 0
    if house_data:
        total_price = 0
        count = 0
        for h in house_data:
            rent_str = str(h.get('rent', '0'))
            # 提取租金数字
            import re
            match = re.search(r'(\d+)', rent_str)
            if match:
                total_price += int(match.group(1))
                count += 1
        if count > 0:
            avg_price = round(total_price / count, 0)

    # 获取筛选配置
    filters_config = load_filters_config()

    # 统计每个筛选方案匹配的房源数量
    filter_stats = []
    enabled_filters = filters_config.get('enabled_filters', [])
    filter_rules = {r['name']: r for r in filters_config.get('filter_rules', [])}

    for filter_name in enabled_filters:
        if filter_name in filter_rules:
            rule = filter_rules[filter_name]
            # 使用正确的筛选逻辑
            matched_houses = filter_house_data(house_data, rule['conditions'])
            matched_count = len(matched_houses)

            filter_stats.append({
                'name': filter_name,
                'description': rule['description'],
                'count': matched_count,
                'enabled': rule.get('enabled', True)
            })

    # 为每个房源添加匹配的筛选方案
    houses_with_filters = []
    for house in house_data[:50]:  # 显示前50个房源
        matched = []
        for stat in filter_stats:
            if stat['count'] > 0:
                rule = filter_rules[stat['name']]
                matched_houses = filter_house_data([house], rule['conditions'])
                if matched_houses:
                    matched.append(stat['name'])

        # 提取租金数字
        rent_str = str(house.get('rent', '0'))
        import re
        rent_match = re.search(r'(\d+)', rent_str)
        rent_value = int(rent_match.group(1)) if rent_match else 0

        houses_with_filters.append({
            **house,
            'matched_filters': matched,
            'rent_value': rent_value  # 添加数字化的租金，方便排序
        })

    # 按租金排序
    houses_with_filters.sort(key=lambda x: x.get('rent_value', 0))

    # 生成今日数据
    today_data = {
        'update_time': now.isoformat(),
        'date': now.strftime('%Y-%m-%d'),
        'time': now.strftime('%H:%M:%S'),
        'total_count': total_count,
        'filtered_count': filtered_count,
        'new_count': len(house_data) if house_data else 0,  # 新增数量 = 总数量
        'avg_price': avg_price,
        'filters': filter_stats,
        'houses': houses_with_filters,
        'enabled_filters': enabled_filters,
        'all_filters': filter_rules
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
    print(f"   - 总房源: {today_data['total_count']}")
    print(f"   - 筛选结果: {today_data['filtered_count']}")
    print(f"   - 平均租金: ¥{today_data['avg_price']}")

    # 保存筛选配置供前端使用
    filters_data = {
        'enabled_filters': today_data['enabled_filters'],
        'all_filters': today_data['all_filters'],
        'filter_stats': today_data['filters']
    }
    filters_file = os.path.join(DATA_DIR, 'filters.json')
    with open(filters_file, 'w', encoding='utf-8') as f:
        json.dump(filters_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已生成筛选配置: {filters_file}")

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

    # 从CSV文件读取房源数据
    try:
        house_data = read_recent_house_data(days=1)
        print(f"✅ 从CSV文件读取到 {len(house_data)} 条房源数据")

        # 如果有数据，显示前几条
        if house_data:
            print(f"   示例数据: {house_data[0].get('house_name', 'N/A')} - {house_data[0].get('rent', 'N/A')}")
    except Exception as e:
        print(f"⚠️ 读取CSV文件失败: {e}")
        import traceback
        traceback.print_exc()
        house_data = []

    # 如果没有数据，生成空数据结构
    if not house_data:
        print("⚠️ 没有房源数据，生成空仪表板")

    # 更新仪表板（使用所有数据，不应用额外筛选）
    today_data = update_dashboard(house_data, house_data)

    print("=" * 50)
    print("✅ 仪表板数据生成完成")
    print(f"- 总房源: {today_data['total_count']}")
    print(f"- 启用筛选: {', '.join(today_data['enabled_filters'])}")
    print(f"- 平均租金: ¥{today_data['avg_price']}")
    print("=" * 50)


if __name__ == '__main__':
    main()
