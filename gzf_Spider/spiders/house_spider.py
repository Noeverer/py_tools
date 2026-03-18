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
        # 获取总页数 - 查找分页器中的最大页码数字
        total_pages = 1
        try:
            pager_text = driver.find_element(By.XPATH, "//ul[@class='el-pager']").text
            page_numbers = [int(x) for x in pager_text.split() if x.isdigit()]
            if page_numbers:
                total_pages = max(page_numbers)
                print(f"检测到总页数: {total_pages}")
        except:
            print("未检测到分页器，尝试逐页抓取")

        i = 1
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        houselist = []
        current_page = 1
        max_pages = 50  # 最大抓取页数，防止无限循环
        consecutive_empty_pages = 0  # 连续空页数计数
        seen_house_ids = set()  # 记录已抓取的房源ID，防止重复

        while current_page <= total_pages and current_page <= max_pages:
            # 获取当前页的房源
            houses = driver.find_elements(
                By.XPATH, "//ul[@class='village-house-lists']/li"
            )

            if not houses:
                print(f"⚠️ 第{current_page}页未获取到房源")
                print(f"检查页面URL: {driver.current_url}")
                print(f"尝试重新获取房源...")
                time.sleep(2)
                houses = driver.find_elements(
                    By.XPATH, "//ul[@class='village-house-lists']/li"
                )
                if not houses:
                    print(f"❌ 第{current_page}页确实无房源，停止抓取")
                    break

            consecutive_empty_pages = 0  # 重置连续空页计数

            for house in houses:
                househash = {}
                house_text = house.text
                text_parts = house_text.split("\n")

                for idx, part in enumerate(text_parts):
                    part = part.strip()
                    if not part:
                        continue

                    # 使用关键词匹配而不是索引，避免顺序问题
                    if "所属区域" in part:
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
                        # 第一行通常是房源名称
                        if not househash.get("house_name"):
                            househash["house_name"] = part

                applicant_count = get_applicant_count(driver, house)
                househash["applicant_count"] = applicant_count

                # 检查房源是否重复
                house_id = househash.get('house_name', '') + str(househash.get('floor', ''))
                if house_id in seen_house_ids:
                    print(f"⚠️ 发现重复房源，跳过: {househash.get('house_name', '未知')}")
                    continue
                seen_house_ids.add(house_id)

                print(f"获取到第{i}条房源: 名称={househash.get('house_name', '未知')}, 区域={househash.get('house_site', '未知')}, 租金={househash.get('rent', '未知')}")
                houselist.append(househash)
                i += 1

            # 翻页
            print(f"成功抓取第{current_page}页，准备翻页...")
            if current_page < total_pages:
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC

                    # 等待并检查翻页按钮
                    try:
                        next_btn = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-next"))
                        )
                    except:
                        print("未找到翻页按钮，可能已到最后一页")
                        break

                    # 检查按钮是否禁用
                    if "disabled" in next_btn.get_attribute("class"):
                        print("已到最后一页")
                        break

                    # 先滚动到按钮位置，避免被遮挡
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                    time.sleep(0.5)

                    # 使用JavaScript点击，避免元素遮挡问题
                    driver.execute_script("arguments[0].click();", next_btn)
                    time.sleep(3)
                    current_page += 1
                except Exception as e:
                    print(f"翻页失败: {e}")
                    break
            else:
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
