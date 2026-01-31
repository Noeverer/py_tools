from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from datetime import datetime, timedelta
import glob
import re

app = Flask(__name__)

# 数据目录
DATA_DIR = "../data/"

def get_available_dates():
    """获取可用的数据日期"""
    csv_files = glob.glob(os.path.join(DATA_DIR, "house_data_*.csv"))
    dates = []
    for file in csv_files:
        # 从文件名提取日期，例如 house_data_2023-01-01.csv
        match = re.search(r'house_data_(\d{4}-\d{2}-\d{2})\.csv', os.path.basename(file))
        if match:
            dates.append(match.group(1))
    return sorted(dates, reverse=True)  # 按日期降序排列

def load_data_for_date(date):
    """加载指定日期的数据"""
    file_path = os.path.join(DATA_DIR, f"house_data_{date}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # 确保时间戳列是datetime类型
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    else:
        return pd.DataFrame()

@app.route('/')
def index():
    """主页，显示所有可用日期"""
    dates = get_available_dates()
    selected_date = request.args.get('date', dates[0] if dates else None)
    
    if selected_date:
        df = load_data_for_date(selected_date)
        if not df.empty:
            # 按时间戳排序，最新的在前面
            if 'timestamp' in df.columns:
                df = df.sort_values(by='timestamp', ascending=False)
            # 转换为字典列表以便在模板中使用
            house_list = df.to_dict('records')
        else:
            house_list = []
    else:
        house_list = []
    
    return render_template('index.html', dates=dates, selected_date=selected_date, house_list=house_list)

@app.route('/api/house_data/<date>')
def api_house_data(date):
    """API端点，返回指定日期的房源数据"""
    df = load_data_for_date(date)
    if not df.empty:
        # 转换为字典列表
        house_list = df.to_dict('records')
        # 将时间戳转换为字符串格式
        for house in house_list:
            if 'timestamp' in house and pd.notna(house['timestamp']):
                house['timestamp'] = house['timestamp'].isoformat()
        return jsonify(house_list)
    else:
        return jsonify([])

@app.route('/api/dates')
def api_dates():
    """API端点，返回所有可用日期"""
    dates = get_available_dates()
    return jsonify(dates)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)