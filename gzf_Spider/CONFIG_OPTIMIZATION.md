# 配置优化说明

## 1. iOS推送分组修复 ✅

### 修复内容：
- **URL编码修复**：确保分组名称正确编码，避免iOS中显示乱码
- **参数优化**：添加subtitle参数，提升iOS推送显示效果
- **分组逻辑改进**：自动根据房源内容选择合适的推送分组

### 效果：
- iOS设备中可以正确显示推送分组
- 支持按地区（金桥、张江等）和类型（低价房、监控等）分组
- 推送标题更清晰，包含副标题信息

---

## 2. 配置灵活性优化 ✅

### 新增功能：

#### 环境变量支持
所有配置都可以通过环境变量设置，支持：
- **Docker容器化部署**
- **CI/CD自动化配置**
- **多环境配置切换**

#### 配置类结构
```python
# 新的配置结构
BARK_CONFIG = BarkConfig()      # Bark推送配置
PUSH_TIME_CONFIG = PushTimeConfig()  # 推送时间控制
CRAWLER_CONFIG = CrawlerConfig()      # 爬虫配置
DATA_CONFIG = DataConfig()            # 数据存储配置
FILTER_CONFIG = FilterConfig()        # 筛选配置
```

#### 多时间段推送支持
```bash
# 支持多个推送时间段
PUSH_TIME_SLOTS=8-11,19-21  # 早上8-11点，晚上7-9点
```

#### 自定义筛选方案
```bash
# 通过环境变量定义筛选方案
PRESET_FILTER_金桥低价=area:金桥,max_rent:3000
PRESET_FILTER_我的筛选=area:张江,house_type:1室1厅,max_rent:2500
```

---

## 3. 使用方法

### 方法一：修改配置文件
继续使用 `config/settings.py` 文件配置，保持向后兼容。

### 方法二：使用环境变量
1. 复制环境变量示例文件：
   ```bash
   cp .env.example .env
   ```

2. 修改 `.env` 文件中的配置

3. 加载环境变量并运行：
   ```bash
   export $(cat .env | xargs)
   python main.py
   ```

### 方法三：Docker部署
```bash
# 设置环境变量
docker run -e BARK_KEY=your_key_here \
           -e ENABLED_PRESET_FILTERS=金桥低价 \
           -e PUSH_TIME_SLOTS=8-11,19-21 \
           your-image
```

---

## 4. 配置示例

### 基础配置
```bash
# Bark推送配置
BARK_KEY=your_actual_key_here
BARK_DEFAULT_GROUP=公租房通知

# 启用金桥地区低价筛选
ENABLED_PRESET_FILTERS=金桥低价
```

### 高级配置
```bash
# 多时间段推送
PUSH_TIME_SLOTS=8-11,19-21

# 自定义筛选方案
PRESET_FILTER_金桥低价=area:金桥,max_rent:3000
PRESET_FILTER_张江一室=area:张江,house_type:1室1厅,max_rent:3500
ENABLED_PRESET_FILTERS=金桥低价,张江一室

# 自定义推送服务器
BARK_SERVER_URL=https://your-bark-server.com
```

---

## 5. 向后兼容性

所有原有配置方式保持兼容，可以：
- 继续使用 `config/settings.py` 文件
- 逐步迁移到环境变量
- 混合使用两种方式（环境变量优先）

---

## 6. 推荐配置

### 生产环境
```bash
BARK_KEY=your_production_key
PUSH_TIME_ENABLED=true
PUSH_TIME_SLOTS=8-11,19-21
ENABLED_PRESET_FILTERS=金桥低价,张江低价
TEST_PUSH_ENABLED=false
```

### 开发环境
```bash
BARK_KEY=your_development_key
PUSH_TIME_ENABLED=false
TEST_PUSH_ENABLED=true
CRAWLER_DELAY=2
```

现在系统支持更加灵活和强大的配置管理，满足不同部署环境的需求！