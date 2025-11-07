import urllib.request
import zipfile
import platform
import subprocess
import os,re,sys
import json

def download_chrome():
    """
    根据操作系统下载对应的Chrome浏览器
    """
    system = platform.system().lower()
    print(f"正在为 {system} 系统下载Chrome浏览器...")
    
    try:
        if system == "linux":
            # Ubuntu/Debian
            subprocess.run(["wget", "-q", "-O", "google-chrome.deb", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
            subprocess.run(["sudo", "dpkg", "-i", "google-chrome.deb"])
            subprocess.run(["sudo", "apt", "install", "-f", "-y"])
            os.remove("google-chrome.deb")
        elif system == "darwin":  # macOS
            urllib.request.urlretrieve("https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg", "googlechrome.dmg")
            print("请手动安装下载的Chrome浏览器: googlechrome.dmg")
        elif system == "windows":
            urllib.request.urlretrieve("https://dl.google.com/chrome/install/latest/chrome_installer.exe", "chrome_installer.exe")
            subprocess.run(["chrome_installer.exe"])
            os.remove("chrome_installer.exe")
        print("Chrome浏览器下载安装完成")
        return True
    except Exception as e:
        print(f"Chrome浏览器下载安装失败: {e}")
        return False


def get_chrome_version():
    """
    获取Chrome浏览器版本号
    """
    try:
        # 尝试多种Chrome命令
        chrome_commands = ['google-chrome', 'chrome', 'chromium-browser', 'chromium']
        for cmd in chrome_commands:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    version_line = result.stdout.strip()
                    # 提取版本号 (格式如: Google Chrome 125.0.6422.142)
                    version_match = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', version_line)
                    if version_match:
                        return version_match.group(1)  # 返回主版本号
            except:
                continue
        return None
    except Exception as e:
        print(f"获取Chrome版本失败: {e}")
        return None


def get_chromedriver_version():
    """
    获取已安装的chromedriver版本号
    """
    try:
        system = platform.system().lower()
        if system == "windows":
            driver_path = "chromedriver.exe"
        else:
            driver_path = "/usr/local/bin/chromedriver"
            
        # 检查指定路径
        if not os.path.exists(driver_path):
            # 检查当前目录
            if os.path.exists("chromedriver"):
                driver_path = "./chromedriver"
            elif os.path.exists("chromedriver.exe"):
                driver_path = "./chromedriver.exe"
            else:
                # 尝试在PATH中查找
                driver_path = "chromedriver"
        
        result = subprocess.run([driver_path, '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.strip()
            # 提取版本号 (格式如: ChromeDriver 125.0.6422.142)
            version_match = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)', version_line)
            if version_match:
                return version_match.group(1)  # 返回主版本号
        return None
    except Exception as e:
        print(f"获取chromedriver版本失败: {e}")
        return None



def get_chromedriver_version_for_chrome(chrome_version):
    """
    根据Chrome版本获取对应的chromedriver版本
    """
    try:
        # 对于Chrome 115及更高版本，使用新的API
        if int(chrome_version) >= 115:
            api_url = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{chrome_version}"
            response = urllib.request.urlopen(api_url)
            chromedriver_version = response.read().decode('utf-8').strip()
            return chromedriver_version
        else:
            # 对于较旧版本，直接使用Chrome版本
            return chrome_version
    except Exception as e:
        print(f"获取chromedriver版本失败: {e}")
        return None


def download_chromedriver():
    """
    下载匹配的chromedriver
    """
    # 根据操作系统确定chromedriver路径
    system = platform.system().lower()
    if system == "windows":
        driver_path = "chromedriver.exe"
        zip_name = "chromedriver_win32.zip"
        if platform.machine().endswith('64'):
            zip_name = "chromedriver_win64.zip"
    elif system == "darwin":  # macOS
        driver_path = "/usr/local/bin/chromedriver"
        if platform.machine() == 'arm64':
            zip_name = "chromedriver_mac_arm64.zip"
        else:
            zip_name = "chromedriver_mac64.zip"
    else:  # Linux
        driver_path = "/usr/local/bin/chromedriver"
        if platform.machine().endswith('64'):
            zip_name = "chromedriver_linux64.zip"
        else:
            zip_name = "chromedriver_linux32.zip"
        
    print("正在下载chromedriver...")
    
    try:
        # 获取Chrome版本
        chrome_version = get_chrome_version()
        if not chrome_version:
            print("无法获取Chrome版本，将尝试下载最新版本的chromedriver")
        
        print(f"Chrome浏览器版本: {chrome_version}")
        
        # 获取对应的chromedriver版本
        chromedriver_version = None
        if chrome_version:
            chromedriver_version = get_chromedriver_version_for_chrome(chrome_version)
        
        # 构建下载链接列表（按优先级排序）
        download_urls = []
        
        if chrome_version and chromedriver_version:
            # 首选：使用准确的版本匹配
            if int(chrome_version) >= 115:
                # 新的下载地址结构
                base_url = "https://edgedl.measurementlab.net/chrome-for-testing"
                download_urls.append(f"{base_url}/{chromedriver_version}/{zip_name.replace('.zip', '')}/{zip_name}")
                
                # 备用地址
                download_urls.append(f"https://storage.googleapis.com/chrome-for-testing-public/{chromedriver_version}/{zip_name.replace('.zip', '')}/{zip_name}")
            else:
                # 旧版本地址
                download_urls.append(f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/{zip_name}")
        
        # 添加备选方案
        download_urls.extend([
            "https://chromedriver.storage.googleapis.com/LATEST_RELEASE/chromedriver_linux64.zip",
            "https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip"
        ])
        
        # 尝试下载
        downloaded = False
        for download_url in download_urls:
            try:
                print(f"正在从 {download_url} 下载chromedriver...")
                urllib.request.urlretrieve(download_url, "chromedriver.zip")
                downloaded = True
                break
            except Exception as e:
                print(f"从 {download_url} 下载失败: {e}")
                continue
        
        if not downloaded:
            print("所有下载源都不可用")
            return False
            
        # 解压文件
        with zipfile.ZipFile("chromedriver.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # 查找解压后的chromedriver文件并移动到目标位置
        chromedriver_file = None
        search_files = []
        
        if system == "windows":
            search_files = ["chromedriver.exe"]
        else:
            search_files = ["chromedriver"]
            
        # 如果直接文件未找到，遍历解压目录查找
        if not chromedriver_file:
            for root, dirs, files in os.walk("."):
                for file in search_files:
                    if file in files:
                        chromedriver_file = os.path.join(root, file)
                        break
                if chromedriver_file:
                    break
        
        if chromedriver_file:
            # 移动文件到目标位置
            target_path = driver_path if system != "windows" else "chromedriver.exe"
            if os.path.exists(target_path):
                os.remove(target_path)
            os.rename(chromedriver_file, target_path)
            
            # 设置执行权限 (非Windows系统)
            if system != "windows":
                os.chmod(target_path, 0o755)
        else:
            print("错误: 未在下载的压缩包中找到chromedriver文件")
            os.remove("chromedriver.zip")
            return False
        
        # 清理下载的压缩包
        if os.path.exists("chromedriver.zip"):
            os.remove("chromedriver.zip")
        
        print("chromedriver下载安装完成")
        return True
    except Exception as e:
        print(f"chromedriver下载安装失败: {e}")
        return False


def check_environment(auto_install=False):
    """
    检查运行环境是否满足要求
    """
    print("开始检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("错误: Python版本过低，需要3.6及以上版本")
        return False
    
    # 检查必要模块
    required_modules = ['selenium', 'requests']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"错误: 缺少必要的Python模块 {module}")
            return False
    
    # 检查Chrome浏览器
    chrome_found = False
    try:
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            chrome_found = True
            print(f"Chrome浏览器版本: {result.stdout.strip()}")
        else:
            # 尝试其他可能的Chrome命令
            result = subprocess.run(['chrome', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                chrome_found = True
                print(f"Chrome浏览器版本: {result.stdout.strip()}")
    except FileNotFoundError:
        pass
    
    if not chrome_found:
        print("未检测到Google Chrome浏览器")
        if auto_install:
            if download_chrome():
                chrome_found = True
            else:
                print("警告: Chrome浏览器下载安装失败，将在无头模式下运行")
        else:
            print("警告: 未检测到Google Chrome浏览器，将在无头模式下运行")
    
    # 检查chromedriver
    system = platform.system().lower()
    if system == "windows":
        driver_path = "chromedriver.exe"
    else:
        driver_path = "/usr/local/bin/chromedriver"
        
    driver_found = False
    if os.path.exists(driver_path):
        try:
            result = subprocess.run([driver_path, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                driver_found = True
                print(f"chromedriver版本: {result.stdout.strip()}")
        except Exception as e:
            print(f"chromedriver无法正常运行: {e}")
    else:
        # 检查是否在当前目录或其他PATH路径中
        try:
            result = subprocess.run(['chromedriver', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                driver_found = True
                print(f"chromedriver版本: {result.stdout.strip()}")
        except FileNotFoundError:
            pass
    
    if not driver_found:
        print(f"未找到可用的chromedriver")
        if auto_install:
            if download_chromedriver():
                driver_found = True
            else:
                print("chromedriver下载安装失败")
                return False
        else:
            return False
        
    # 检查chromedriver可执行权限
    if driver_found and system != "windows" and not os.access(driver_path, os.X_OK):
        print(f"错误: {driver_path} 没有执行权限")
        if auto_install:
            try:
                os.chmod(driver_path, 0o755)
                print("已修复chromedriver执行权限")
            except Exception as e:
                print(f"修复chromedriver执行权限失败: {e}")
                return False
        else:
            return False
    
    print("环境检查通过")
    return True

if __name__ == "__main__":
    # download_chrome()
    download_chromedriver()
    check_environment()
