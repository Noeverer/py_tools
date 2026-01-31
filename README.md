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

## 注意事项

- 请遵守网站的robots.txt协议和相关法律法规
- 合理设置爬取频率，避免对服务器造成过大压力
- 需要自行申请Bark推送服务的Key