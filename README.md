# 🏠 上海公租房信息监控平台

实时监控上海浦东公租房房源信息，自动推送最新房源到您的手机。

## ⚡ 功能特性

- **自动爬取**: 每日定时自动爬取最新房源信息
- **即时推送**: 通过Bark服务推送房源信息到iOS设备
- **分条通知**: 每条房源单独推送，方便查看
- **灵活筛选**: 支持按区域、租金、房型筛选

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/Noeverer/py_tools.git
cd py_tools/gzf_Spider
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置您的BARK_KEY
```

### 4. 运行
```bash
python main.py
```

---

## 📝 配置说明

所有配置通过 `.env` 文件管理，复制 `.env.example` 为 `.env` 后修改。

### Bark推送配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `BARK_KEY` | **必填** Bark推送密钥，从Bark App获取 | - |
| `BARK_DEFAULT_GROUP` | 默认分组名称 | `公租房通知` |
| `BARK_SERVER_URL` | Bark服务器地址 | `https://api.day.app` |
| `BARK_SOUND` | 推送声音 | `telegraph` |
| `BARK_LEVEL` | 推送级别 | `active` |

### 推送时间控制

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PUSH_TIME_ENABLED` | 是否启用时间控制 | `true` |
| `PUSH_TIME_SLOTS` | 推送时间段(多时段用逗号分隔) | `8-11` |
| `PUSH_TIMEZONE` | 时区 | `Asia/Shanghai` |

**示例**:
```bash
# 单时间段：早上8点到11点
PUSH_TIME_SLOTS=8-11

# 多时间段：早上8-11点，晚上19-21点
PUSH_TIME_SLOTS=8-11,19-21
```

### 筛选配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FILTER_MIN_RENT` | 最低租金(元) | - |
| `FILTER_MAX_RENT` | 最高租金(元) | `5000` |
| `FILTER_AREA` | 区域关键词 | - |
| `FILTER_HOUSE_TYPE` | 房型关键词 | - |
| `ENABLED_PRESET_FILTERS` | 启用的预设筛选方案(逗号分隔) | `金桥低价` |

### 预设筛选方案

通过环境变量自定义筛选方案：

```bash
# 格式：PRESET_FILTER_方案名=area:区域,max_rent:最高租金,min_rent:最低租金,house_type:房型

# 示例：创建"金桥低价"筛选
PRESET_FILTER_金桥低价=area:金桥,max_rent:3000

# 示例：创建"张江一室户"筛选
PRESET_FILTER_张江一室户=area:张江,house_type:1室1厅,max_rent:3500

# 启用多个筛选方案
ENABLED_PRESET_FILTERS=金桥低价,张江一室户,低价房
```

**内置预设筛选**:
- `金桥低价`: 区域=金桥，租金≤3000
- `张江低价`: 区域=张江，租金≤3000
- `唐镇低价`: 区域=唐镇，租金≤3000
- `低价房`: 租金≤3000

### 监控地点配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `MONITORED_LOCATIONS` | 监控的地点(逗号分隔) | `张江,唐镇,曹路,合庆,金桥,陆家嘴,金杨新村,洋泾,花木,康桥` |

### 其他配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `CRAWLER_DELAY` | 页面加载延迟(秒) | `5` |
| `CRAWLER_MAX_RETRIES` | 最大重试次数 | `3` |
| `DATA_DIR` | 数据存储目录 | `data/` |
| `LOGS_DIR` | 日志存储目录 | `logs/` |
| `TEST_PUSH_ENABLED` | 是否启用测试推送 | `true` |

---

## 📋 .env 配置示例

```bash
# ========== Bark推送(必填) ==========
BARK_KEY=your_bark_key_here

# ========== 推送时间 ==========
PUSH_TIME_ENABLED=true
PUSH_TIME_SLOTS=8-11

# ========== 筛选配置 ==========
ENABLED_PRESET_FILTERS=金桥低价,张江低价

# 自定义筛选
PRESET_FILTER_金桥低价=area:金桥,max_rent:3000
PRESET_FILTER_张江低价=area:张江,max_rent:3000
PRESET_FILTER_一室户=house_type:1室1厅,max_rent:3500

# ========== 监控地点 ==========
MONITORED_LOCATIONS=张江,唐镇,曹路,合庆,金桥,陆家嘴,金杨新村,洋泾,花木,康桥

# ========== 其他 ==========
TEST_PUSH_ENABLED=true
CRAWLER_DELAY=5
```

---

## 🔧 GitHub Actions 部署

1. 在GitHub仓库设置中添加Secrets:
   - `BARK_KEY`: 您的Bark推送密钥

2. workflow会自动定时运行（每天9:00和15:00）

3. 也可手动触发：点击Actions -> 工作流 -> Run workflow

---

## 📊 数据字段说明

| 字段 | 说明 |
|------|------|
| `house_name` | 房源名称/小区名 |
| `house_site` | 所属区域 |
| `rent` | 租金（元/月） |
| `house_type` | 户型 |
| `floor` | 楼层信息 |
| `area` | 建筑面积（㎡） |
| `applicant_count` | 申请人数 |

---

## 📄 许可证

本项目仅供学习交流使用，请遵守相关网站的robots.txt协议和法律法规。
