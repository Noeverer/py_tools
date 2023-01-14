from selenium import webdriver
from selenium.webdriver.common.by import By
import time,os,re
import datetime
import conndb,requests
from sendmail_for_gzf import sendmail


def start_selenium(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--remote-debugging-port=9222")
    driver = os.path.join("/usr/bin/","chromedriver")

    browser = webdriver.Chrome(executable_path=driver,chrome_options=chrome_options)
    
    browser.get(url)
    time.sleep(2)
    print("web握手成功")
    browser.quit
    return browser


def get_house_content(driver):
    try:
        # houses = driver.find_elements(By.CSS_SELECTOR, "[class='c-6  fs26']")  # 通过CSS selector获取对象

        pages = driver.find_elements(By.XPATH, "//ul[@class='el-pager']/li")  # 获取pages
        i = 1
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        global houselist
        houselist = []
        # print(len(pages))
        if len(pages) > 1:
            for p in range(len(pages)):
                houses = driver.find_elements(By.XPATH, "//ul[@class='village-house-lists']/li")  # 获取page_house 上
                for house in houses:
                    househash = {}
                    # 遍历房源列表写入数据库
                    # str(driver.find_elements(By.XPATH, "//ul[@class='village-house-lists']/li")[4].text).split('\n')
                    for ind,one in enumerate(list(str(house.text).split('\n'))):
                        if ind == 0:
                            househash["house_name"] = one if len(one) else 'null'
                        elif one.find("所属区域"):
                            househash["house_site"] = one if len(one) else 'null'
                        elif one.find("所属户型"):
                            househash["house_type"] = one if len(one) else 'null'
                        elif one.find("楼层名称"):
                            househash["flood"] = one if len(one) else 'null'
                        elif one.find("建筑面积"):
                            househash["area"] = one if len(one) else 'null'
                        elif one.find("租金"):
                            househash["rent"] = one if len(one) else 'null'
                        else:
                            print('=== other info === ',one)
                    print("获取到{}条房源".format(i),'==',househash)
                    houselist.append(househash)
                    i += 1
                print("成功抓取第{}页".format(p + 1))
                driver.find_element(By.CSS_SELECTOR, "[class='btn-next']").click()
                time.sleep(5)
                houses = driver.find_elements(By.CSS_SELECTOR, "[class='c-6 fs26']")  # 获取下一页对象
        else:
            # for house in houses:
            #     # 遍历房源列表写入数据库
            #     houselist.append(house.text)
            #     print("获取到{}条房源".format(i),house.text)
            #     i += 1
            pass
        if len(houselist) != 0:
            try:
                conn, cur = conndb.conn_db()  # open database
                print("数据库连接成功")
                process_content(dt, houselist, cur)  # insert data
                print("数据写入完成")
            except Exception as e:
                print("数据库连接失败：", e)
            finally:
                conndb.conn_close(conn, cur)
        else:
            print("没有抓取到房源信息")
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return houselist


# 数据处理函数并写入数据库(获取全部数据入库)
def process_content(time, houses, cur):
    print("准备写入数据……",houses)
    for house in houses:
        # house_name = house.get('house_name') if house.get('house_name') else ''
        # house_site = house.get('house_site') if house.get('house_site') else ''
        # rent_monoey = house.get('rent_monoey') if house.get('rent_monoey') else ''
        # choose_start_time = house.get('choose_start_time') if house.get('choose_start_time') else ''
        # choose_end_time = house.get('choose_end_time') if house.get('choose_end_time') else ''
        # house_type = house.get('house_type') if house.get('house_type') else ''
        # choosed = house.get('choosed') if house.get('choosed') else ''
        # foold = house.get('foold') if house.get('foold') else ''
        # area = house.get('area') if house.get('area') else ''
        keys = ",".join(house.keys())
        values = "','".join([house.get(k) for k in keys.split(",") if house.get(k) or 'null'])
        fill_s = ''.join(["'%s'," for i in range(0,len(house))])[:-2]

        sql = "INSERT INTO HouseData(%s)  values ('%s') " % (keys ,values)  # 插入房源信息
        conndb.exe_update(cur, sql)
        # else:
        #     print("发现新房源[{}]，准备注册入库".format(house))
        #     sql2 = "INSERT INTO HouseData(choose_start_time)values ('%s')" % house  # 注册房源信息
        #     conndb.exe_update(cur, sql2)
        #     sql1 = "SELECT house_id FROM HouseData WHERE choose_start_time='%s'" % house
        #     conndb.exe_query(cur, sql1)
        #     results = cur.fetchone()  # 获取id号
        #     house_id = results[0]
        #     sql = "INSERT INTO HouseData(house_id,get_time,house_source)values (%s,'%s','%s')" % (
        #         house_id, time, house)
        #     conndb.exe_update(cur, sql)  # 插入房源信息
    conndb.exe_commit(cur)


# 判断是否有关注房源，如果有发邮件
def checkbox_houses(houses,need_house,start_time,end_time):
    # 范围时间
    d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start_time, '%Y-%m-%d%H:%M')
    d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + end_time, '%Y-%m-%d%H:%M')
    n_time = datetime.datetime.now()
    # 判断当前时间是否在范围时间内
    if n_time > d_time and n_time < d_time1:
        for one_house in houses:
            for one_need in need_house:
                if one_house.get('house_type').find(one_need) != -1:
                    if int(one_house.get('house_site').replace(' 月租金','')) < 3000:
                        send_info = '<>'.join(one_house.values()) + '<>' +str(n_time)
                        send_info = re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9]','',send_info)
                        receiver = "https://api.day.app/65H5UU3wpmLwSAzxn7PVb6/%s?group=%s" % (send_info, '公租房')
                        resp = requests.get(receiver)
                        print("+++ send to my iphone +++",send_info)


def main():
    print("程序执行开始")
    # url = "https://select.pdgzf.com/villageLists"
    url = "https://select.pdgzf.com/houseLists"
    kill_chrome = os.system("ps -ef | grep chrome | awk -F ' ' '{print $2}' | xargs -i kill {}")
    print(kill_chrome,"frist kill chrome")
    driver = start_selenium(url)
    houselist = get_house_content(driver)
    os.system("ps -ef | grep chrome | awk -F ' ' '{print $2}' | xargs -i kill {}")
    checkbox_houses(houselist,need_house,'08:30','22:55')
    print("程序执行结束")


need_house = ["唐镇","张江","川沙","曹路","合庆"]
main()
