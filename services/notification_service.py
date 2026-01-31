import requests
import re
from datetime import datetime
from config.settings import BARK_KEY, PUSH_GROUP, MONITORED_LOCATIONS, LOCATION_BARK_KEYS, MONITORED_HOUSE_TYPES, TEST_PUSH_ENABLED


def clean_text(text):
    """
    清理文本中的特殊字符，只保留中文、英文和数字
    """
    if text:
        return re.sub(r'[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', str(text))
    return ""


def send_test_push():
    """
    发送测试推送
    """
    if not TEST_PUSH_ENABLED:
        return

    test_message = f"【测试推送】服务运行正常 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    push_single_message(test_message, is_test=True)


def send_notification(house_data):
    """
    推送房屋信息到微信

    Args:
        house_data (list): 房屋信息列表
    """
    # 先发送测试推送
    send_test_push()

    if not house_data:
        print("没有房屋数据需要推送")
        push_single_message("未查询到符合条件的房源信息")
        return

    # 分别处理普通推送和特定地点推送
    regular_houses = []
    special_location_houses = []

    for house in house_data:
        # 检查是否是监控的特定地点
        is_monitored_location = False
        if MONITORED_LOCATIONS:
            for location in MONITORED_LOCATIONS:
                if location in house.get('house_site', '') or location in house.get('house_name', ''):
                    is_monitored_location = True
                    special_location_houses.append(house)
                    break

        # 检查是否是监控的特定房型
        is_monitored_type = False
        if MONITORED_HOUSE_TYPES:
            for house_type in MONITORED_HOUSE_TYPES:
                if house_type in house.get('house_type', ''):
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


def send_regular_notification(house_data):
    """
    推送普通房屋信息到默认分组

    Args:
        house_data (list): 房屋信息列表
    """
    # 构造推送消息 - 优化iOS显示效果
    message_lines = [f"🏠【最新房源({len(house_data)}套)】"]
    for i, house in enumerate(house_data, 1):
        # 构造房源信息，使用更简洁的格式
        parts = []
        if house.get('house_name'):
            # 只保留小区名称的关键部分
            name = str(house['house_name'])
            # 如果名称过长，截取关键部分
            if len(name) > 20:
                name = name[:20] + "..."
            parts.append(name)
        if house.get('house_type'):
            parts.append(f"户型:{house['house_type']}")
        if house.get('rent'):
            parts.append(f"💰{house['rent']}")
        if house.get('area'):
            parts.append(f"📊{house['area']}")
        if house.get('floor'):
            parts.append(f"🏢{house['floor']}")
        # 添加申请人数信息
        if 'applicant_count' in house and house.get('applicant_count', 0) > 0:
            parts.append(f"👥{house['applicant_count']}人")

        house_info = " | ".join(parts)
        message_lines.append(f"{i}️⃣ {house_info}")

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
            if location in house.get('house_site', '') or location in house.get('house_name', ''):
                matched_location = location
                break

        # 如果没有匹配地点，检查房型
        if not matched_location:
            for house_type in MONITORED_HOUSE_TYPES:
                if house_type in house.get('house_type', ''):
                    matched_location = f"房型:{house_type}"
                    break

        if matched_location:
            if matched_location not in location_groups:
                location_groups[matched_location] = []
            location_groups[matched_location].append(house)

    # 为每个地点分别推送
    for location, houses in location_groups.items():
        # 构造推送消息 - 优化iOS显示效果
        message_lines = [f"🚨【{location}特惠({len(houses)}套)】"]
        for i, house in enumerate(houses, 1):
            # 构造房源信息，使用更简洁的格式
            parts = []
            if house.get('house_name'):
                # 只保留小区名称的关键部分
                name = str(house['house_name'])
                # 如果名称过长，截取关键部分
                if len(name) > 20:
                    name = name[:20] + "..."
                parts.append(name)
            if house.get('house_type'):
                parts.append(f"户型:{house['house_type']}")
            if house.get('rent'):
                parts.append(f"💰{house['rent']}")
            if house.get('area'):
                parts.append(f"📊{house['area']}")
            if house.get('floor'):
                parts.append(f"🏢{house['floor']}")
            # 添加申请人数信息
            if 'applicant_count' in house and house.get('applicant_count', 0) > 0:
                parts.append(f"👥{house['applicant_count']}人")

            house_info = " | ".join(parts)
            message_lines.append(f"{i}️⃣ {house_info}")

        full_message = "\\n".join(message_lines)

        # 根据地点选择推送密钥
        location_key = LOCATION_BARK_KEYS.get(location, BARK_KEY)
        location_group = f"{PUSH_GROUP}-{location}"

        # 发送推送请求
        push_single_message(full_message, key=location_key, group=location_group)


def push_single_message(message, key=BARK_KEY, group=PUSH_GROUP, is_test=False):
    """
    推送单条消息到微信

    Args:
        message (str): 要推送的消息
        key (str): Bark推送key
        group (str): 分组名称
        is_test (bool): 是否为测试消息
    """
    if not key or key == "your_bark_key_here":
        print("请先在config/settings.py中配置BARK_KEY")
        return

    try:
        clean_msg = clean_text(message)
        # URL编码
        encoded_msg = requests.utils.quote(clean_msg)

        # 为iOS优化推送参数
        if is_test:
            # 测试消息使用不同参数
            url = f"https://api.day.app/{key}/{encoded_msg}?group={group}&icon=https://raw.githubusercontent.com/Finb/Bark/refs/heads/master/Server/assets/favicon.ico&level=passive"
        else:
            # 正常房源消息使用更醒目的参数
            url = f"https://api.day.app/{key}/{encoded_msg}?group={group}&icon=https://raw.githubusercontent.com/Finb/Bark/refs/heads/master/Server/assets/favicon.ico&sound=telegraph&badge=+1&level=active"

        # 添加headers模拟真实请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
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
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
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