# 📊 上海公租房监控仪表板

## 简介

本仪表板提供上海浦东公租房房源信息的可视化展示，包括：
- 📈 每日房源统计
- 🎯 符合条件的房源列表
- 🔍 自定义筛选方案
- 💰 价格趋势分析

## 访问地址

仪表板通过GitHub Pages部署，访问地址：
```
https://noeverer.github.io/py_tools/
```

## 功能特性

### 1. 实时统计
- 今日房源总数
- 符合筛选条件的房源数
- 新增房源数量
- 平均租金

### 2. 筛选方案展示
自动展示当前启用的筛选方案及匹配房源数，包括：
- 金桥低价（金桥地区，月租<3000元）
- 张江低价（张江地区，月租<3000元）
- 一室户优选（一室一厅，月租<3500元）

### 3. 房源列表
展示所有符合筛选条件的房源，包括：
- 房源名称
- 区域位置
- 月租金
- 户型
- 建筑面积
- 匹配的筛选方案

## 配置筛选条件

### 方式1: 通过YAML文件配置

编辑 `gzf_Spider/config/filters.yaml` 文件：

```yaml
enabled_filters:
  - 金桥低价
  - 张江低价
  - 一室户优选

filter_rules:
  - name: 金桥低价
    description: 金桥地区，月租低于3000元
    conditions:
      area: 金桥
      max_rent: 3000
      min_rent: 0
      house_type: ""
      enabled: true
```

### 方式2: 通过环境变量配置

编辑 `gzf_Spider/.env` 文件：

```bash
# 启用的筛选方案
ENABLED_PRESET_FILTERS=金桥低价,张江低价

# 自定义筛选
PRESET_FILTER_金桥低价=area:金桥,max_rent:3000
PRESET_FILTER_张江低价=area:张江,max_rent:3000
```

## 推送渠道配置

### Bark推送（iOS）

编辑 `.env` 文件：

```bash
# Bark推送配置
BARK_KEY=your_bark_key_here
BARK_DEFAULT_GROUP=公租房通知
BARK_SERVER_URL=https://api.day.app
BARK_SOUND=telegraph
BARK_LEVEL=active
```

推送类型：
- **individual**: 分条推送（每个房源单独推送）
- **summary**: 汇总推送（每天一次汇总）
- **both**: 两种都推送

### 邮件推送

编辑 `.env` 文件：

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_password
RECEIVER_EMAIL=receiver@example.com
```

## 定时任务

### GitHub Actions配置

当前配置：
- **运行时间**: 每天北京时间 8:00、9:00、10:00
- **手动触发**: 可通过GitHub Actions界面手动运行

修改定时任务：
编辑 `.github/workflows/gzf_spider.yml`：

```yaml
schedule:
  - cron: '0 0,1,2 * * *'  # UTC时间
```

### 本地定时运行

使用Linux cron或Windows任务计划程序：

```bash
# Linux crontab
0 8 * * * cd /path/to/py_tools/gzf_Spider && python main.py --mode normal
```

## 数据更新

### 自动更新
- GitHub Actions每天自动运行，自动更新数据
- 数据保留最近30天

### 手动更新
1. 进入GitHub Actions页面
2. 选择 "公租房爬虫定时任务"
3. 点击 "Run workflow"
4. 选择运行模式并执行

### 本地运行
```bash
cd gzf_Spider
python main.py --mode normal
```

## 数据文件结构

```
docs/
├── index.html              # 仪表板前端页面
├── data/
│   ├── today.json         # 今日数据（实时更新）
│   └── history.json       # 历史数据（保留30天）
└── README.md              # 本文档
```

## 数据格式

### today.json
```json
{
  "update_time": "2026-03-11T10:00:00+08:00",
  "date": "2026-03-11",
  "total": 125,
  "filtered": 8,
  "new": 3,
  "avg_price": 2850,
  "filters": [...],
  "houses": [...]
}
```

## 注意事项

1. **GitHub Secrets配置**: 确保在GitHub仓库中配置了`BARK_KEY`
2. **数据延迟**: 数据可能有几分钟的延迟，这是正常现象
3. **隐私保护**: 数据仅供个人查看，请不要公开分享
4. **法律声明**: 仅供学习交流使用，请遵守相关法律法规

## 技术支持

如有问题，请提交Issue到GitHub仓库：
```
https://github.com/Noeverer/py_tools/issues
```

---

*最后更新: 2026-03-11*
