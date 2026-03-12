#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
筛选条件管理API
提供筛选条件的CRUD操作
"""

import os
import json
import yaml
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 配置文件路径
FILTERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'filters.yaml')
USER_FILTERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'user_filters.json')


def load_filters():
    """加载筛选条件"""
    try:
        with open(FILTERS_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"加载筛选配置失败: {e}")
        return {}


def save_filters(filters):
    """保存筛选条件"""
    try:
        with open(FILTERS_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(filters, f, allow_unicode=True, default_flow_style=False)
        return True
    except Exception as e:
        print(f"保存筛选配置失败: {e}")
        return False


def load_user_filters():
    """加载用户自定义筛选"""
    try:
        with open(USER_FILTERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"加载用户筛选失败: {e}")
        return {}


def save_user_filters(user_filters):
    """保存用户自定义筛选"""
    try:
        os.makedirs(os.path.dirname(USER_FILTERS_FILE), exist_ok=True)
        with open(USER_FILTERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_filters, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存用户筛选失败: {e}")
        return False


@app.route('/api/filters', methods=['GET'])
def get_filters():
    """获取所有筛选条件"""
    filters = load_filters()
    user_filters = load_user_filters()
    
    # 合并系统筛选和用户自定义筛选
    result = {
        'enabled': filters.get('enabled_filters', []),
        'system_filters': filters.get('filter_rules', []),
        'user_filters': user_filters.get('filters', []),
        'last_updated': datetime.now().isoformat()
    }
    
    return jsonify(result)


@app.route('/api/filters', methods=['POST'])
def update_filters():
    """更新筛选条件"""
    data = request.json
    
    # 验证数据
    if not data or 'enabled' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    # 加载现有配置
    filters = load_filters()
    
    # 更新启用的筛选方案
    filters['enabled_filters'] = data['enabled']
    
    # 如果有用户自定义筛选，保存到用户配置
    if 'user_filters' in data:
        user_filters = load_user_filters()
        user_filters['filters'] = data['user_filters']
        user_filters['last_updated'] = datetime.now().isoformat()
        save_user_filters(user_filters)
    
    # 保存系统配置
    if save_filters(filters):
        return jsonify({
            'success': True,
            'message': '筛选条件已更新',
            'last_updated': datetime.now().isoformat()
        })
    else:
        return jsonify({'error': '保存失败'}), 500


@app.route('/api/filters/user', methods=['POST'])
def add_user_filter():
    """添加用户自定义筛选"""
    data = request.json
    
    # 验证数据
    required_fields = ['name', 'conditions']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要参数'}), 400
    
    conditions = data['conditions']
    if not all(key in conditions for key in ['max_rent']):
        return jsonify({'error': '缺少必要条件参数'}), 400
    
    # 加载并更新用户筛选
    user_filters = load_user_filters()
    if 'filters' not in user_filters:
        user_filters['filters'] = []
    
    # 创建新筛选
    new_filter = {
        'id': f"user_{datetime.now().timestamp()}",
        'name': data['name'],
        'description': data.get('description', ''),
        'conditions': conditions,
        'enabled': data.get('enabled', True),
        'created_at': datetime.now().isoformat()
    }
    
    user_filters['filters'].append(new_filter)
    user_filters['last_updated'] = datetime.now().isoformat()
    
    if save_user_filters(user_filters):
        return jsonify({
            'success': True,
            'filter': new_filter,
            'message': '自定义筛选已添加'
        })
    else:
        return jsonify({'error': '保存失败'}), 500


@app.route('/api/filters/user/<filter_id>', methods=['DELETE'])
def delete_user_filter(filter_id):
    """删除用户自定义筛选"""
    user_filters = load_user_filters()
    
    if 'filters' not in user_filters:
        return jsonify({'error': '未找到筛选'}), 404
    
    # 查找并删除筛选
    original_length = len(user_filters['filters'])
    user_filters['filters'] = [f for f in user_filters['filters'] if f['id'] != filter_id]
    
    if len(user_filters['filters']) == original_length:
        return jsonify({'error': '未找到指定的筛选'}), 404
    
    user_filters['last_updated'] = datetime.now().isoformat()
    
    if save_user_filters(user_filters):
        return jsonify({
            'success': True,
            'message': '筛选已删除'
        })
    else:
        return jsonify({'error': '保存失败'}), 500


@app.route('/api/filters/toggle', methods=['POST'])
def toggle_filter():
    """切换筛选方案的启用状态"""
    data = request.json
    
    if not data or 'filter_id' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    filter_id = data['filter_id']
    
    # 加载现有配置
    filters = load_filters()
    enabled_filters = filters.get('enabled_filters', [])
    
    # 切换状态
    if filter_id in enabled_filters:
        enabled_filters.remove(filter_id)
    else:
        enabled_filters.append(filter_id)
    
    filters['enabled_filters'] = enabled_filters
    
    if save_filters(filters):
        return jsonify({
            'success': True,
            'enabled': filter_id in enabled_filters,
            'enabled_filters': enabled_filters,
            'message': '状态已更新'
        })
    else:
        return jsonify({'error': '保存失败'}), 500


@app.route('/api/filters/preview', methods=['POST'])
def preview_filters():
    """预览筛选结果"""
    data = request.json
    
    if not data or 'houses' not in data:
        return jsonify({'error': '缺少房源数据'}), 400
    
    houses = data['houses']
    filter_conditions = data.get('filter_conditions', {})
    
    # 应用筛选条件
    filtered_houses = []
    for house in houses:
        match = True
        
        # 区域筛选
        if filter_conditions.get('area'):
            if filter_conditions['area'] not in house.get('house_site', '') and \
               filter_conditions['area'] not in house.get('house_name', ''):
                match = False
        
        # 租金筛选
        if match and filter_conditions.get('max_rent'):
            try:
                rent = float(house.get('rent', 0))
                if rent > filter_conditions['max_rent']:
                    match = False
            except:
                match = False
        
        # 最低租金
        if match and filter_conditions.get('min_rent'):
            try:
                rent = float(house.get('rent', 0))
                if rent < filter_conditions['min_rent']:
                    match = False
            except:
                match = False
        
        # 户型筛选
        if match and filter_conditions.get('house_type'):
            if filter_conditions['house_type'] not in house.get('house_type', ''):
                match = False
        
        if match:
            filtered_houses.append(house)
    
    return jsonify({
        'success': True,
        'total': len(houses),
        'filtered': len(filtered_houses),
        'houses': filtered_houses[:10]  # 只返回前10个预览
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


if __name__ == '__main__':
    print("🚀 筛选条件管理API启动中...")
    print(f"📁 筛选配置文件: {FILTERS_FILE}")
    print(f"📁 用户配置文件: {USER_FILTERS_FILE}")
    print("🌐 访问地址: http://localhost:5000")
    print("📊 API文档: http://localhost:5000/api/health")
    app.run(host='0.0.0.0', port=5000, debug=True)
