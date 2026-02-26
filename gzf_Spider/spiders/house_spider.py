import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, re
import datetime
import requests
from utils.db_utils import save_house_data_to_csv
from services.notification_service import send_notification


def start_selenium(url):
    """启动Selenium浏览器实例"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # 确定 chromedriver 路径
    driver_path = "/usr/local/bin/chromedriver"
    if not os.path.exists(driver_path):
        # 检查当前目录
        if os.path.exists("chromedriver"):
            driver_path = "./chromedriver"
        elif os.path.exists("chromedriver.exe"):
            driver_path = "./chromedriver.exe"
        else:
            # 尝试在PATH中查找
            driver_path = "chromedriver"

    from selenium.webdriver.chrome.service import Service  # 导入 Service 类

    service = Service(executable_path=driver_path)

    # 初始化 WebDriver
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.get(url)
    time.sleep(2)
    print("Web握手成功")
    return browser


def get_applicant_count(driver, house_element):
    """
    尝试获取房源的申请人数
    注意：这取决于网站的具体结构，可能需要根据实际情况调整
    """
    try:
        # 尝试查找申请人数元素
        # 这里需要根据实际网站的DOM结构来定位申请人数
        # 以下是一些常见的查找方式，可能需要根据实际情况调整
        applicant_elements = house_element.find_elements(
            By.XPATH,
            ".//span[contains(text(), '申请')] | .//div[contains(@class, 'applicant')] | .//span[contains(@class, 'count')]",
        )

        if applicant_elements:
            # 提取数字
            text = applicant_elements[0].text
            numbers = re.findall(r"\d+", text)
            if numbers:
                return int(numbers[0])

        # 如果没找到，返回0表示未知
        return 0
    except:
        # 如果出错，返回0表示未知
        return 0


def get_house_content(driver):
    """从页面获取房源信息"""
    try:
        # 首先获取总页数
        page_elements = driver.find_elements(By.XPATH, "//ul[@class='el-pager']/li")
        if page_elements:
            total_pages = len(page_elements)
            print(f"检测到总页数: {total_pages}")
        else:
            total_pages = 1
            print("未检测到分页器，只有1页")

        i = 1
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        houselist = []

        for page_num in range(total_pages):
            # 获取当前页的房源
            houses = driver.find_elements(
                By.XPATH, "//ul[@class='village-house-lists']/li"
            )

            if not houses:
                print(f"第{page_num + 1}页未获取到房源")
                continue

            for house in houses:
                househash = {}
                house_text = house.text
                text_parts = house_text.split("\n")

                for idx, part in enumerate(text_parts):
                    part = part.strip()
                    if not part:
                        continue

                    if idx == 0:
                        househash["house_name"] = part
                    elif "所属区域" in part:
                        househash["house_site"] = part.replace("所属区域", "").strip()
                    elif "所属户型" in part:
                        househash["house_type"] = part.replace("所属户型", "").strip()
                    elif "楼层名称" in part:
                        househash["floor"] = part.replace("楼层名称", "").strip()
                    elif "建筑面积" in part:
                        househash["area"] = part.replace("建筑面积", "").strip()
                    elif "租金" in part:
                        househash["rent"] = part.replace("租金", "").strip()
                    else:
                        pass

                applicant_count = get_applicant_count(driver, house)
                househash["applicant_count"] = applicant_count

                print(f"获取到第{i}条房源: {househash}")
                houselist.append(househash)
                i += 1

            # 翻页（如果不是最后一页）
            if page_num < total_pages - 1:
                print(f"成功抓取第{page_num + 1}页，准备翻页...")
                try:
                    next_btn = driver.find_element(
                        By.CSS_SELECTOR, "[class='btn-next']"
                    )
                    next_btn.click()
                    time.sleep(3)
                except Exception as e:
                    print(f"翻页失败: {e}")
                    break

        if len(houselist) != 0:
            print(f"总共获取到 {len(houselist)} 条房源信息")
            save_house_data_to_csv(houselist)
            send_notification(houselist)
        else:
            print("没有抓取到房源信息")
            houselist = []

    except Exception as e:
        print(f"获取房源信息时发生错误: {e}")
        houselist = []
    finally:
        driver.quit()

    return houselist


def main():
    """主函数"""
    print("程序执行开始")

    url = "https://select.pdgzf.com/houseLists"
    driver = start_selenium(url)
    houselist = get_house_content(driver)

    print("程序执行结束")
    return houselist


if __name__ == "__main__":
    main()
