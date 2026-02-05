# 🏠 上海公租房信息监控平台

## 📋 功能简介

实时监控上海浦东公租房房源信息，支持自动筛选和iOS推送。

### ✨ 核心功能
- 🕷️ 自动爬取浦东公租房最新房源
- 📱 Bark推送到iOS设备（支持分组显示）
- 🎯 灵活筛选（地区、价格、房型）
- ⏰ 定时推送控制（上海时间8-11点）
- 📊 数据存储和分析

## 🚀 快速开始

### 1. 配置环境
```bash
# 克隆项目
git clone https://github.com/Noeverer/py_tools.git
cd py_tools-master/gzf_Spider

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置推送服务
#### 方法一：修改配置文件
编辑 `config/settings.py`：
```python
BARK_KEY = "your_bark_key_here"  # 替换为你的Bark Key
```

#### 方法二：使用环境变量
```bash
export BARK_KEY=your_bark_key_here
export ENABLED_PRESET_FILTERS=金桥低价,张江低价
```

### 3. 运行爬虫
```bash
# 正常模式
python main.py

# 调试模式
python main.py --mode debug

# 测试模式（仅检查环境）
python main.py --mode test
```

## ⚙️ 配置选项

### 推送时间控制
```bash
# 推送时间段（支持多时间段）
PUSH_TIME_SLOTS=8-11,19-21

# 或单时间段
PUSH_START_HOUR=8
PUSH_END_HOUR=11
```

### 筛选方案
```bash
# 启用的筛选方案
ENABLED_PRESET_FILTERS=金桥低价,张江低价

# 自定义筛选
PRESET_FILTER_我的筛选=area:金桥,max_rent:2500,house_type:1室1厅
```

### Bark推送配置
```bash
BARK_KEY=your_key_here
BARK_DEFAULT_GROUP=公租房通知
BARK_SOUND=telegraph
```

## 📱 iOS推送分组

系统支持以下分组推送：
- 🏠 **默认分组**: 普通房源信息
- 📍 **地区分组**: 金桥、张江、唐镇等
- 💰 **价格分组**: 低价房、高端房等
- 📊 **监控分组**: 特定筛选结果

## 🎯 预设筛选方案

| 方案名称 | 筛选条件 | 说明 |
|---------|---------|------|
| 金桥低价 | 金桥地区 + <3000元 | 金桥地区便宜房源 |
| 张江低价 | 张江地区 + <3000元 | 张江地区便宜房源 |
| 唐镇低价 | 唐镇地区 + <3000元 | 唐镇地区便宜房源 |
| 低价房 | 全区域 + <3000元 | 所有便宜房源 |
| 金桥 | 金桥地区（不限价格） | 金桥地区所有房源 |

## 🐳 Docker部署

```bash
# 构建镜像
docker build -t gzf-monitor .

# 运行容器
docker run -d \
  --name gzf-monitor \
  -e BARK_KEY=your_key_here \
  -e PUSH_TIME_SLOTS=8-11 \
  -v $(pwd)/data:/app/data \
  gzf-monitor
```

## 📋 数据字段

| 字段 | 说明 | 示例 |
|------|------|------|
| house_name | 房源名称 | "张江高科技园人才公寓" |
| house_site | 所属区域 | "张江" |
| rent | 月租金 | "2800元/月" |
| house_type | 户型 | "1室1厅" |
| area | 建筑面积 | "45平方米" |
| applicant_count | 申请人数 | 15 |

## 🔧 高级配置

### 环境变量配置
参考 `.env.example` 文件，支持所有配置通过环境变量设置：

```bash
# 复制示例文件
cp .env.example .env

# 编辑配置
vim .env

# 加载环境变量
export $(cat .env | xargs)
```

### 自定义筛选方案
```bash
# 格式：区域:区域名,max_rent:最高租金,min_rent:最低租金,house_type:房型
PRESET_FILTER_我的方案=area:金桥,max_rent:3000,house_type:1室1厅
```

## 🛠 故障排除

### 常见问题
1. **ChromeDriver版本不匹配**
   ```bash
   # 更新ChromeDriver
   google-chrome --version
   # 下载对应版本的ChromeDriver
   ```

2. **推送失败**
   ```bash
   # 测试Bark服务
   curl "https://api.day.app/your_key/test?group=测试"
   ```

3. **依赖问题**
   ```bash
   # 重新安装依赖
   pip install --force-reinstall -r requirements.txt
   ```

## 📄 许可证

本项目仅供学习交流使用，请遵守相关法律法规。

---

**🏠 持续为您寻找理想的家园**