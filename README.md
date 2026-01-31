# 公租房信息爬取与推送系统

这是一个用于监控上海浦东公租房信息的自动化工具，能够定期爬取房源信息并将更新推送到微信。

## 功能特点

- 自动爬取浦东公租房网站的房源信息
- 将数据保存为CSV日志文件，便于后续分析
- 支持通过Bark服务将房源信息推送到微信
- 支持按租金、区域、房型等条件过滤房源
- 可通过GitHub Actions实现定时自动运行

## 项目结构

```
refactored_project/
├── main.py                 # 主入口文件
├── requirements.txt        # 项目依赖
├── README.md              # 项目说明
├── spiders/               # 爬虫模块
│   └── house_spider.py    # 房源爬虫
├── utils/                 # 工具模块
│   └── db_utils.py        # 数据处理工具（CSV存储）
├── services/              # 服务模块
│   └── notification_service.py  # 通知服务
├── config/                # 配置模块
│   └── settings.py        # 配置文件
├── data/                  # 数据存储目录
└── logs/                  # 日志存储目录
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 在 `config/settings.py` 中配置Bark推送服务的Key
2. 设置需要监控的筛选条件

## 使用方法

### 本地运行

```bash
python main.py
```

### GitHub Actions 自动运行

项目配置了GitHub Actions，可以定时自动运行爬虫任务：

1. 在仓库的Settings -> Secrets and variables -> Actions中添加名为`BARK_KEY`的Secret
2. Actions会在每小时自动运行一次爬虫
3. 如需修改运行频率，编辑`.github/workflows/crawl_house_data.yml`文件中的cron表达式

#### 配置GitHub Actions

1. 在GitHub仓库中启用Actions
2. 添加名为`BARK_KEY`的Secret，值为你的Bark推送密钥
3. Actions将在设定的时间自动运行爬虫并将结果提交到仓库

## 数据存储

- 所有房源信息以CSV格式存储在 `data/` 目录下
- 文件按日期命名，如 `house_data_2023-01-01.csv`
- CSV包含以下字段：timestamp, house_name, house_site, rent, house_type, floor, area

## 数据分析

项目包含数据分析功能，可以对收集到的房源数据进行统计分析：

```bash
python -m utils.data_analysis
```

这将生成最近7天的房源数据报告，包括房源总数、每日房源数量、热门区域、热门房型和租金统计等信息。

## 数据展示

项目包含一个静态Web界面，可以直接在仓库中查看收集到的房源数据：

1. 点击仓库中的 `viewer.html` 文件
2. 用浏览器打开该文件
3. 选择日期查看对应的房源数据

Web界面支持：

- 按日期查看房源数据
- 统计信息展示（房源总数、平均租金等）
- 申请人数显示（如果数据中有此信息）
- 租金分布图表

## 配置监控

使用配置向导轻松设置您关心的地点和房型监控：

1. 点击仓库中的 `configurator.html` 文件
2. 用浏览器打开该文件
3. 按照向导添加您关心的地点和房型
4. 复制生成的配置代码到 `config/settings.py` 文件中

或者直接编辑 `config/settings.py` 文件，修改以下配置：

- `MONITORED_LOCATIONS`: 添加您关心的地点，如 "张江"、"唐镇" 等
- `MONITORED_HOUSE_TYPES`: 添加您关心的房型，如 "1室1厅"、"2室1厅" 等

## 运行时间

爬虫每天在 8:00、9:00、10:00 和 11:00 各运行一次，收集最新的房源信息。

## 申请人数功能

爬虫现在尝试获取每个房源的申请人数信息，并将其保存到CSV文件中。如果网站提供了申请人数信息，它将显示在Web界面和推送通知中。

## 特定地点监控

您可以配置监控特定地点或房型的房源，并接收专门的推送通知：

1. 编辑 `config/settings.py` 文件
2. 在 `MONITORED_LOCATIONS` 数组中添加您关心的地点
3. 在 `MONITORED_HOUSE_TYPES` 数组中添加您关心的房型
4. （可选）在 `LOCATION_BARK_KEYS` 中为不同地点设置不同的推送密钥

示例配置：
```python
MONITORED_LOCATIONS = [
    "张江",
    "唐镇",
    "曹路"
]

MONITORED_HOUSE_TYPES = [
    "1室1厅",
    "2室1厅"
]
```

当爬虫发现匹配的房源时，会发送特殊的推送通知，标题为【地点名特别房源】。

## 注意事项

- 请遵守网站的robots.txt协议和相关法律法规
- 合理设置爬取频率，避免对服务器造成过大压力
- 需要自行申请Bark推送服务的Key