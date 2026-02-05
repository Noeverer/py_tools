import requests
import re
from datetime import datetime
import pytz
from config.settings import (
    BARK_CONFIG,
    PUSH_TIME_CONFIG,
    FILTER_CONFIG,
    MONITORED_LOCATIONS,
    LOCATION_BARK_KEYS,
    MONITORED_HOUSE_TYPES,
    TEST_PUSH_ENABLED,
    PUSH_GROUPS,
    # 向后兼容
    BARK_KEY,
    PUSH_GROUP,
    PUSH_TIME_CONTROL_ENABLED,
    PUSH_START_HOUR,
    PUSH_END_HOUR,
    SHANGHAI_TIMEZONE,
    DEFAULT_FILTERS,
    PRESET_FILTERS,
    ENABLED_PRESET_FILTERS,
)
from utils.db_utils import filter_house_data


def clean_text(text):
    """
    清理文本中的特殊字符，只保留中文、英文和数字
    """
    if text:
        return re.sub(r"[^\u4e00-\u9fa5^a-z^A-Z^0-9]", "", str(text))
    return ""


def send_test_push():
    """
    发送测试推送
    """
    if not TEST_PUSH_ENABLED:
        return

    test_message = (
        f"【测试推送】服务运行正常 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    push_single_message(test_message, is_test=True)


def get_optimal_group(input_group, message, is_test):
    """
    根据消息内容和类型选择最优的推送分组

    Args:
        input_group (str): 输入的分组名称
        message (str): 消息内容
        is_test (bool): 是否为测试消息

    Returns:
        str: 优化后的分组名称
    """
    # 如果是测试消息，使用测试分组
    if is_test:
        return PUSH_GROUPS.get("测试", input_group)

    # 检查是否包含特定关键词，自动分配到相应分组
    message_lower = message.lower()

    # 地区关键词分组
    for location in ["金桥", "张江", "唐镇", "曹路", "陆家嘴", "康桥"]:
        if location in message:
            return PUSH_GROUPS.get(location, input_group)

    # 房型或价格分组
    if "低价" in message_lower or any(
        keyword in message for keyword in ["2000", "3000"]
    ):
        return PUSH_GROUPS.get("低价房", input_group)

    # 监控相关的特殊推送
    if any(keyword in message for keyword in ["监控", "特定", "🚨"]):
        return PUSH_GROUPS.get("监控", input_group)

    # 默认分组
    return PUSH_GROUPS.get("default", input_group)


def is_push_time_enabled():
    """
    检查当前时间是否在允许的推送时间内（上海时间）

    Returns:
        bool: 是否在推送时间内
    """
    if not PUSH_TIME_CONFIG.ENABLED:
        return True

    try:
        # 获取上海时区
        shanghai_tz = pytz.timezone(PUSH_TIME_CONFIG.TIMEZONE)
        current_time = datetime.now(shanghai_tz)
        current_hour = current_time.hour

        # 检查是否在任一时间范围内
        for start_hour, end_hour in PUSH_TIME_CONFIG.TIME_SLOTS:
            if start_hour <= current_hour <= end_hour:
                time_slots_str = ", ".join(
                    [f"{s}-{e}" for s, e in PUSH_TIME_CONFIG.TIME_SLOTS]
                )
                print(
                    f"当前上海时间 {current_time.strftime('%H:%M')} 在推送时间范围内 ({time_slots_str})"
                )
                return True

        time_slots_str = ", ".join([f"{s}-{e}" for s, e in PUSH_TIME_CONFIG.TIME_SLOTS])
        print(
            f"当前上海时间 {current_time.strftime('%H:%M')} 不在推送时间范围内 ({time_slots_str})，跳过推送"
        )
        return False
    except Exception as e:
        print(f"检查推送时间时出错: {e}")
        return True  # 出错时默认允许推送


def send_notification(house_data):
    """
    推送房屋信息到微信

    Args:
        house_data (list): 房屋信息列表
    """
    # 检查推送时间
    if not is_push_time_enabled():
        print("不在推送时间范围内，跳过推送")
        return

    # 先发送测试推送
    send_test_push()

    if not house_data:
        print("没有房屋数据需要推送")
        # 只有在推送时间内才发送无房源消息
        if is_push_time_enabled():
            push_single_message("未查询到符合条件的房源信息")
        return

    # 应用预设筛选方案
    filtered_results = apply_preset_filters(house_data)

    # 推送各个筛选方案的结果
    for filter_name, filtered_data in filtered_results.items():
        if filtered_data:
            print(f"筛选方案 '{filter_name}' 找到 {len(filtered_data)} 条房源")
            send_preset_notification(filter_name, filtered_data)
        else:
            print(f"筛选方案 '{filter_name}' 未找到符合条件的房源")

    # 如果没有启用预设筛选，则使用原有逻辑
    if not FILTER_CONFIG.ENABLED_PRESET_FILTERS:
        # 分别处理普通推送和特定地点推送
        regular_houses = []
        special_location_houses = []

        for house in house_data:
            # 检查是否是监控的特定地点
            is_monitored_location = False
            if MONITORED_LOCATIONS:
                for location in MONITORED_LOCATIONS:
                    if location in house.get("house_site", "") or location in house.get(
                        "house_name", ""
                    ):
                        is_monitored_location = True
                        special_location_houses.append(house)
                        break

            # 检查是否是监控的特定房型
            is_monitored_type = False
            if MONITORED_HOUSE_TYPES:
                for house_type in MONITORED_HOUSE_TYPES:
                    if house_type in house.get("house_type", ""):
                        is_monitored_type = True
                        if not is_monitored_location:  # 避免重复添加
                            special_location_houses.append(house)
                        break

            # 如果不是特殊监控的，则加入普通列表
            if not is_monitored_location and not is_monitored_type:
                regular_houses.append(house)

        # 推送普通房源信息
        if regular_houses:
            send_regular_notification(regular_houses)

        # 推送特定地点房源信息
        if special_location_houses:
            send_special_location_notification(special_location_houses)


def apply_preset_filters(house_data):
    """
    应用预设筛选方案

    Args:
        house_data (list): 房源数据列表

    Returns:
        dict: 筛选方案名称到筛选结果的映射
    """
    results = {}

    for filter_name in FILTER_CONFIG.ENABLED_PRESET_FILTERS:
        if filter_name in FILTER_CONFIG.PRESET_FILTERS:
            filter_config = FILTER_CONFIG.PRESET_FILTERS[filter_name]
            filtered_data = filter_house_data(house_data, filter_config)
            results[filter_name] = filtered_data
            print(f"筛选方案 '{filter_name}': {len(filtered_data)} 条房源")
        else:
            print(f"警告: 未找到筛选方案 '{filter_name}'")

    return results


def send_preset_notification(filter_name, house_data):
    """
    发送预设筛选方案的结果

    Args:
        filter_name (str): 筛选方案名称
        house_data (list): 筛选后的房源数据
    """
    # 构造推送消息
    message_lines = [f"🎯【{filter_name}({len(house_data)}套)】"]
    for i, house in enumerate(house_data, 1):
        # 构造房源信息
        parts = []
        if house.get("house_name"):
            name = (
                str(house["house_name"])[:15] + "..."
                if len(str(house["house_name"])) > 15
                else str(house["house_name"])
            )
            parts.append(name)
        if house.get("house_type"):
            house_type = str(house["house_type"])[:6]
            parts.append(f"户型:{house_type}")
        if house.get("rent"):
            parts.append(f"💰{house['rent']}")
        if house.get("area"):
            parts.append(f"📊{house['area']}")
        if house.get("floor"):
            floor_info = str(house["floor"])
            if len(floor_info) <= 8:
                parts.append(f".Floor:{floor_info}")
            else:
                parts.append(f"楼")

        if "applicant_count" in house and house.get("applicant_count", 0) > 0:
            parts.append(f"👥{house['applicant_count']}")

        house_info = " | ".join(parts)
        if len(house_info) > 40:
            short_parts = []
            if house.get("house_name"):
                name = (
                    str(house["house_name"])[:10] + "..."
                    if len(str(house["house_name"])) > 10
                    else str(house["house_name"])
                )
                short_parts.append(name)
            if house.get("rent"):
                short_parts.append(f"💰{house['rent']}")
            if house.get("area"):
                short_parts.append(f"{house['area']}")
            house_info = " | ".join(short_parts)

        message_lines.append(f"{i}.{house_info}")

    full_message = "\\n".join(message_lines)

    # 使用特定分组推送
    group_name = f"{PUSH_GROUP}-{filter_name}"
    push_single_message(full_message, group=group_name)


def send_regular_notification(house_data):
    """
    推送普通房屋信息到默认分组

    Args:
        house_data (list): 房屋信息列表
    """
    # 构造推送消息 - 优化iOS显示效果
    message_lines = [f"🏠【最新房源({len(house_data)}套)】"]
    for i, house in enumerate(house_data, 1):
        # 构造房源信息，使用更简洁的格式，适合iOS推送
        parts = []
        if house.get("house_name"):
            # 只保留小区名称的关键部分，限制长度以适应iOS推送
            name = (
                str(house["house_name"])[:15] + "..."
                if len(str(house["house_name"])) > 15
                else str(house["house_name"])
            )
            parts.append(name)
        if house.get("house_type"):
            # 简化户型描述
            house_type = str(house["house_type"])[:6]  # 限制户型长度
            parts.append(f"户型:{house_type}")
        if house.get("rent"):
            # 使用更紧凑的租金格式
            parts.append(f"💰{house['rent']}")
        if house.get("area"):
            # 面积信息
            parts.append(f"📊{house['area']}")
        if house.get("floor"):
            # 楼层信息，简化显示
            floor_info = str(house["floor"])
            if len(floor_info) <= 8:  # 如果楼层信息不长，直接显示
                parts.append(f".Floor:{floor_info}")
            else:  # 否则只显示关键信息
                parts.append(f"楼")

        # 添加申请人数信息（如果大于0）
        if "applicant_count" in house and house.get("applicant_count", 0) > 0:
            parts.append(f"👥{house['applicant_count']}")

        # 确保整条消息不会太长，适合iOS推送显示
        house_info = " | ".join(parts)
        if len(house_info) > 40:  # 如果信息太长，进一步精简
            # 只保留最重要的信息：名称、租金
            short_parts = []
            if house.get("house_name"):
                name = (
                    str(house["house_name"])[:10] + "..."
                    if len(str(house["house_name"])) > 10
                    else str(house["house_name"])
                )
                short_parts.append(name)
            if house.get("rent"):
                short_parts.append(f"💰{house['rent']}")
            if house.get("area"):
                short_parts.append(f"{house['area']}")
            house_info = " | ".join(short_parts)

        message_lines.append(f"{i}.{house_info}")

    full_message = "\\n".join(message_lines)

    # 发送推送请求
    push_single_message(full_message)


def send_special_location_notification(house_data):
    """
    推送特定地点房屋信息到指定分组或使用特定密钥

    Args:
        house_data (list): 房屋信息列表
    """
    # 按地点分组
    location_groups = {}
    for house in house_data:
        matched_location = None
        # 检查是否匹配监控地点
        for location in MONITORED_LOCATIONS:
            if location in house.get("house_site", "") or location in house.get(
                "house_name", ""
            ):
                matched_location = location
                break

        # 如果没有匹配地点，检查房型
        if not matched_location:
            for house_type in MONITORED_HOUSE_TYPES:
                if house_type in house.get("house_type", ""):
                    matched_location = f"房型:{house_type}"
                    break

        if matched_location:
            if matched_location not in location_groups:
                location_groups[matched_location] = []
            location_groups[matched_location].append(house)

    # 为每个地点分别推送
    for location, houses in location_groups.items():
        # 构造推送消息 - 优化iOS显示效果
        message_lines = [f"🚨【{location}({len(houses)}套)】"]
        for i, house in enumerate(houses, 1):
            # 构造房源信息，使用更简洁的格式，适合iOS推送
            parts = []
            if house.get("house_name"):
                # 只保留小区名称的关键部分，限制长度以适应iOS推送
                name = (
                    str(house["house_name"])[:15] + "..."
                    if len(str(house["house_name"])) > 15
                    else str(house["house_name"])
                )
                parts.append(name)
            if house.get("house_type"):
                # 简化户型描述
                house_type = str(house["house_type"])[:6]  # 限制户型长度
                parts.append(f"户型:{house_type}")
            if house.get("rent"):
                # 使用更紧凑的租金格式
                parts.append(f"💰{house['rent']}")
            if house.get("area"):
                # 面积信息
                parts.append(f"📊{house['area']}")
            if house.get("floor"):
                # 楼层信息，简化显示
                floor_info = str(house["floor"])
                if len(floor_info) <= 8:  # 如果楼层信息不长，直接显示
                    parts.append(f".Floor:{floor_info}")
                else:  # 否则只显示关键信息
                    parts.append(f"楼")

            # 添加申请人数信息（如果大于0）
            if "applicant_count" in house and house.get("applicant_count", 0) > 0:
                parts.append(f"👥{house['applicant_count']}")

            # 确保整条消息不会太长，适合iOS推送显示
            house_info = " | ".join(parts)
            if len(house_info) > 40:  # 如果信息太长，进一步精简
                # 只保留最重要的信息：名称、租金
                short_parts = []
                if house.get("house_name"):
                    name = (
                        str(house["house_name"])[:10] + "..."
                        if len(str(house["house_name"])) > 10
                        else str(house["house_name"])
                    )
                    short_parts.append(name)
                if house.get("rent"):
                    short_parts.append(f"💰{house['rent']}")
                if house.get("area"):
                    short_parts.append(f"{house['area']}")
                house_info = " | ".join(short_parts)

            message_lines.append(f"{i}.{house_info}")

        full_message = "\\n".join(message_lines)

        # 根据地点选择推送密钥
        location_key = LOCATION_BARK_KEYS.get(location, BARK_KEY)
        location_group = f"{PUSH_GROUP}-{location}"

        # 发送推送请求
        push_single_message(full_message, key=location_key, group=location_group)


def push_single_message(message, key=None, group=None, is_test=False, auto_group=True):
    """
    推送单条消息到微信

    Args:
        message (str): 要推送的消息
        key (str): Bark推送key，默认使用配置文件中的key
        group (str): 分组名称，默认使用默认分组
        is_test (bool): 是否为测试消息
        auto_group (bool): 是否自动使用分组配置
    """
    # 使用配置文件的默认值
    if key is None:
        key = BARK_CONFIG.KEY
    if group is None:
        group = BARK_CONFIG.DEFAULT_GROUP

    if not key or key == "your_bark_key_here":
        print("请先配置BARK_KEY（可在环境变量中设置）")
        return

    # 自动选择合适的分组
    if auto_group:
        group = get_optimal_group(group, message, is_test)

    try:
        clean_msg = clean_text(message)
        # URL编码 - 确保分组名称也正确编码
        encoded_msg = requests.utils.quote(clean_msg)
        encoded_group = requests.utils.quote(group)

        # 构建基础URL
        base_url = f"{BARK_CONFIG.SERVER_URL}/{key}/{encoded_msg}"

        # 构建参数
        params = {"group": encoded_group}

        # 根据是否为测试消息选择不同的参数
        if is_test:
            params.update(BARK_CONFIG.TEST_PARAMS)
            params["subtitle"] = "测试消息"
        else:
            params.update(BARK_CONFIG.DEFAULT_PARAMS)
            params["badge"] = "+1"
            params["subtitle"] = "房源推送"

        # 构建完整URL
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{base_url}?{param_str}"

        # 添加headers模拟真实请求
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            if is_test:
                print(f"测试消息推送成功: {message}")
            else:
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
        url = f"https://api.day.app/{key}/{test_msg}?group=测试&sound=calypso"

        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
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
