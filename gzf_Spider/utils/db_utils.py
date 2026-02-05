import csv
import os
from datetime import datetime, timedelta
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def save_house_data_to_csv(house_data, filename=None):
    """
    将房源数据保存到CSV文件

    Args:
        house_data (list): 房源数据列表
        filename (str): CSV文件名，默认使用日期命名
    """
    if not house_data:
        logger.info("没有房源数据需要保存")
        return

    # 如果没有提供文件名，则使用当前日期作为文件名
    if filename is None:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"../data/house_data_{today}.csv"

    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # 检查文件是否存在，决定是否需要写入表头
    write_header = not os.path.exists(filename)

    try:
        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "timestamp",
                "house_name",
                "house_site",
                "rent",
                "house_type",
                "floor",
                "area",
                "applicant_count",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if write_header:
                writer.writeheader()

            for house in house_data:
                # 添加时间戳
                house_record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "house_name": house.get("house_name", ""),
                    "house_site": house.get("house_site", ""),
                    "rent": house.get("rent", ""),
                    "house_type": house.get("house_type", ""),
                    "floor": house.get("floor", ""),
                    "area": house.get("area", ""),
                    "applicant_count": house.get("applicant_count", 0),  # 添加申请人数
                }
                writer.writerow(house_record)

        logger.info(f"成功将 {len(house_data)} 条房源数据保存到 {filename}")

    except Exception as e:
        logger.error(f"保存房源数据到CSV时发生错误: {e}")


def read_recent_house_data(days=1, filename=None):
    """
    读取最近几天的房源数据

    Args:
        days (int): 天数
        filename (str): CSV文件名

    Returns:
        list: 房源数据列表
    """
    if filename is None:
        # 读取最近几天的数据文件
        house_data = []
        for i in range(days):
            date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            file_path = f"data/house_data_{date_str}.csv"

            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            house_data.append(row)
                except Exception as e:
                    logger.error(f"读取文件 {file_path} 时发生错误: {e}")

        return house_data
    else:
        # 读取指定文件
        house_data = []
        try:
            with open(filename, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    house_data.append(row)
        except Exception as e:
            logger.error(f"读取文件 {filename} 时发生错误: {e}")

        return house_data


def filter_house_data(house_data, filters=None):
    """
    根据条件过滤房源数据

    Args:
        house_data (list): 房源数据列表
        filters (dict): 过滤条件

    Returns:
        list: 过滤后的房源数据列表
    """
    if not filters or not house_data:
        return house_data

    filtered_data = []

    for house in house_data:
        match = True

        # 按租金范围过滤
        if "min_rent" in filters and filters["min_rent"] is not None:
            rent_str = (
                house.get("rent", "")
                .replace("元/月", "")
                .replace(",", "")
                .replace("元", "")
            )
            try:
                rent_value = float(rent_str)
                if rent_value < filters["min_rent"]:
                    match = False
            except ValueError:
                # 如果租金无法转换为数字，则跳过
                pass

        if "max_rent" in filters and filters["max_rent"] is not None:
            rent_str = (
                house.get("rent", "")
                .replace("元/月", "")
                .replace(",", "")
                .replace("元", "")
            )
            try:
                rent_value = float(rent_str)
                if rent_value > filters["max_rent"]:
                    match = False
            except ValueError:
                # 如果租金无法转换为数字，则跳过
                pass

        # 按区域过滤
        if "area" in filters and filters["area"]:
            if filters["area"] not in house.get("house_site", "") and filters[
                "area"
            ] not in house.get("house_name", ""):
                match = False

        # 按房型过滤
        if "house_type" in filters and filters["house_type"]:
            if filters["house_type"] not in house.get("house_type", ""):
                match = False

        if match:
            filtered_data.append(house)

    return filtered_data


def get_latest_house_data(limit=10, days=1):
    """
    获取最新的房源数据

    Args:
        limit (int): 返回记录数量限制
        days (int): 查询最近几天的数据

    Returns:
        list: 最新的房源数据列表
    """
    all_data = read_recent_house_data(days=days)
    # 按时间戳排序，获取最新的记录
    sorted_data = sorted(all_data, key=lambda x: x["timestamp"], reverse=True)
    return sorted_data[:limit]
