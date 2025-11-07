# 将mysql中部分信息推送到指定微信或者群里面

## 功能说明

该模块实现了从MySQL数据库中查询房屋信息，并将信息推送到指定微信或微信群的功能。

## 文件说明

- [main.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/main.py) - 主程序文件，负责执行查询和推送任务
- [config.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/config.py) - 配置文件，包含数据库和推送服务配置
- [requirements.txt](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/requirements.txt) - 项目依赖文件
- [wechat_sender.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/wechat_sender.py) - 独立的微信推送模块（不依赖项目其他代码）
- [push_housedata.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/push_housedata.py) - 独立的房源数据查询和推送脚本

## 使用方法

### 方法一：使用原有项目代码
1. 配置数据库连接信息和推送服务密钥：
   在 [config.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/config.py) 中修改相应配置

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行主程序：
   ```bash
   python main.py
   ```

### 方法二：使用独立推送模块（推荐）
1. 安装依赖：
   ```bash
   pip install requests pymysql
   ```

2. 修改 [wechat_sender.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/wechat_sender.py) 中的 `BARK_KEY`

3. 直接运行：
   ```bash
   python wechat_sender.py
   ```

### 方法三：使用独立查询推送脚本
1. 安装依赖：
   ```bash
   pip install requests pymysql
   ```

2. 修改 [push_housedata.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/push_housedata.py) 中的配置信息

3. 运行：
   ```bash
   python push_housedata.py
   ```

## 推送服务

目前使用 [Bark](https://github.com/Finb/Bark) 推送服务实现消息推送功能。
需要配置 `BARK_KEY`。

### 身份验证

程序会自动验证Bark推送服务密钥的有效性，确保推送功能正常工作。

## 数据筛选

支持多种筛选条件：
- 按租金范围筛选
- 按区域关键词筛选
- 按房型筛选
- 只推送未被选走的房源（默认开启）

在 [main.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/main.py) 或 [push_housedata.py](file:///home/ante/02-code/02-gzf/py_tools-master/gzf_Spider/msg/push_housedata.py) 的 `main()` 函数中修改 `filters` 变量来设置筛选条件。

## 定时任务

可通过 Linux crontab 设置定时执行：

```bash
# 每天上午9点执行一次
0 9 * * * cd /path/to/project/gzf_Spider/msg && python push_housedata.py

# 每小时执行一次
0 * * * * cd /path/to/project/gzf_Spider/msg && python push_housedata.py
```