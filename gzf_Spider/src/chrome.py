import os
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--remote-debugging-port=9222")
# chrome_options.add_argument("disable-infobars")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('window-size=1200x600')
# chrome_options.binary_location = '/usr/bin/google-chrome-stable'



# if browser == 'chromium':
#         browser_path = '/usr/bin/chromium'

# if browser == 'chrome':
#     browser_path = '/usr/bin/google-chrome-stable'
driver = os.path.join("/usr/bin/","chromedriver")


browser = webdriver.Chrome(executable_path=driver,chrome_options=chrome_options)
browser.get("https://www.baidu.com")
print(browser.title)

