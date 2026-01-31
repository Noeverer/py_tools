import pandas as pd
import os
from datetime import datetime, timedelta
from collections import Counter
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_house_data_from_csv(date_range_days=7):
    """
    从CSV文件加载房源数据

    Args:
        date_range_days (int): 加载最近多少天的数据

    Returns:
        pandas.DataFrame: 房源数据DataFrame
    """
    all_data = []
    base_dir = "data/"

    # 获取最近几天的数据文件
    for i in range(date_range_days):
        date_str = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        file_path = os.path.join(base_dir, f"house_data_{date_str}.csv")

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                all_data.append(df)
                logger.info(f"成功加载文件: {file_path}")
            except Exception as e:
                logger.error(f"加载文件 {file_path} 时发生错误: {e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        # 转换时间戳列为datetime类型
        combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
        return combined_df
    else:
        logger.warning("没有找到任何数据文件")
        return pd.DataFrame()


def analyze_house_data(df):
    """
    分析房源数据

    Args:
        df (pandas.DataFrame): 房源数据DataFrame

    Returns:
        dict: 分析结果
    """
    if df.empty:
        return {"error": "没有数据可供分析"}

    analysis_result = {}

    # 总房源数
    analysis_result["total_count"] = len(df)

    # 按日期统计
    df['date'] = df['timestamp'].dt.date
    daily_counts = df.groupby('date').size().to_dict()
    analysis_result["daily_counts"] = daily_counts

    # 按区域统计
    area_counts = df['house_site'].value_counts().to_dict()
    analysis_result["area_counts"] = area_counts

    # 按房型统计
    type_counts = df['house_type'].value_counts().to_dict()
    analysis_result["type_counts"] = type_counts

    # 租金分析
    # 清理租金数据并转换为数值
    df['rent_clean'] = df['rent'].str.extract(r'(\d+)').astype(float)
    if not df['rent_clean'].dropna().empty:
        analysis_result["rent_stats"] = {
            "mean": round(df['rent_clean'].mean(), 2),
            "median": df['rent_clean'].median(),
            "min": df['rent_clean'].min(),
            "max": df['rent_clean'].max()
        }

    return analysis_result


def generate_report(date_range_days=7):
    """
    生成房源数据报告

    Args:
        date_range_days (int): 分析最近多少天的数据

    Returns:
        str: 分析报告
    """
    df = load_house_data_from_csv(date_range_days)
    analysis = analyze_house_data(df)

    if "error" in analysis:
        return "没有数据可供分析"

    report = f"""
房源数据分析报告 ({date_range_days}天内)
================================

总房源数: {analysis['total_count']}

每日房源数量:
"""
    for date, count in analysis['daily_counts'].items():
        report += f"  {date}: {count}\n"

    report += "\n热门区域:\n"
    for area, count in list(analysis['area_counts'].items())[:10]:  # 显示前10个
        report += f"  {area}: {count}\n"

    report += "\n热门房型:\n"
    for house_type, count in list(analysis['type_counts'].items())[:10]:  # 显示前10个
        report += f"  {house_type}: {count}\n"

    if 'rent_stats' in analysis:
        rent_stats = analysis['rent_stats']
        report += f"\n租金统计:\n"
        report += f"  平均租金: {rent_stats['mean']}元\n"
        report += f"  中位数租金: {rent_stats['median']}元\n"
        report += f"  最低租金: {rent_stats['min']}元\n"
        report += f"  最高租金: {rent_stats['max']}元\n"

    return report


if __name__ == "__main__":
    # 示例：生成最近7天的报告
    report = generate_report(7)
    print(report)