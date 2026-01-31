import requests
import re
from datetime import datetime
from config.settings import BARK_KEY, PUSH_GROUP


def clean_text(text):
    """
    清理文本中的特殊字符，只保留中文、英文和数字
    """
    if text:
        return re.sub(r'[^\u4e00-\u9fa5^a-z^A-Z^0-9]', '', str(text))
    return ""


def send_notification(house_data):
    """
    推送房屋信息到微信

    Args:
        house_data (list): 房屋信息列表
    """
    if not house_data:
        print("没有房屋数据需要推送")
        push_single_message("未查询到符合条件的房源信息")
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
        if house.get('rent'):
            info_parts.append(f"租金:{house['rent']}")
        if house.get('area'):
            info_parts.append(f"面积:{house['area']}")
        if house.get('floor'):
            info_parts.append(f"楼层:{house['floor']}")

        house_info = " | ".join(info_parts)
        clean_house_info = clean_text(house_info)
        message_lines.append(f"{i}. {clean_house_info}")

    full_message = "\\n".join(message_lines)

    # 发送推送请求
    push_single_message(full_message)


def push_single_message(message, key=BARK_KEY, group=PUSH_GROUP):
    """
    推送单条消息到微信

    Args:
        message (str): 要推送的消息
        key (str): Bark推送key
        group (str): 分组名称
    """
    if not key or key == "your_bark_key_here":
        print("请先在config/settings.py中配置BARK_KEY")
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