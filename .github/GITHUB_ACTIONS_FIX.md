# GitHub Actions 定时任务修复说明

## 修复日期
2026-03-11

## 问题描述
GitHub Actions 每日定时任务运行时出现错误，需要修正。

## 发现的问题

### 1. **Bark推送测试代码格式问题** (第150行)
**问题**: 测试代码压缩在一行，可读性差且容易出错
```yaml
# 修复前
python -c "import os,requests; k=os.getenv('BARK_KEY',''); print('BARK_KEY:',k); t1='https://api.day.app/'+k+'/Test1'; r1=requests.get(t1,timeout=10); print('Test1 Status:',r1.status_code,'Response:',r1.text[:200]); t2='https://api.day.app/'+k+'/Test2?group=Test'; r2=requests.get(t2,timeout=10); print('Test2 Status:',r2.status_code,'Response:',r2.text[:200])"
```

**修复**: 改为多行格式，增加错误处理
```yaml
# 修复后
python -c "
import os
import requests

BARK_KEY = os.getenv('BARK_KEY', '')
print(f'BARK_KEY configured: {bool(BARK_KEY)}')

if BARK_KEY:
    test_url1 = f'https://api.day.app/{BARK_KEY}/GitHub_Action_Test'
    try:
        response1 = requests.get(test_url1, timeout=10)
        print(f'Test 1 - Status: {response1.status_code}, Response: {response1.text[:200]}')
    except Exception as e:
        print(f'Test 1 - Error: {str(e)}')
else:
    print('⚠️ BARK_KEY not configured, skipping push test')
"
```

### 2. **Bark环境变量配置不完整**
**问题**: workflow中引用了 `BARK_URL` 但未提供默认值，可能导致错误

**修复**: 添加完整的Bark配置环境变量，包括默认值
```yaml
# 修复后
BARK_KEY: ${{ secrets.BARK_KEY }}
BARK_DEFAULT_GROUP: ${{ secrets.BARK_DEFAULT_GROUP || '公租房通知' }}
BARK_SERVER_URL: ${{ secrets.BARK_SERVER_URL || 'https://api.day.app' }}
BARK_SOUND: ${{ secrets.BARK_SOUND || 'telegraph' }}
BARK_LEVEL: ${{ secrets.BARK_LEVEL || 'active' }}
```

### 3. **BARK_KEY检查过于严格**
**问题**: 当BARK_KEY未配置时直接报错退出，但实际上爬虫任务应该可以继续执行（仅推送功能不可用）

**修复**: 改为警告提示，不影响任务执行
```yaml
# 修复前
else
  echo "❌ BARK_KEY未配置"
fi

# 修复后
else
  echo "⚠️ BARK_KEY未配置 - 推送功能将不可用"
fi
```

### 4. **ChromeDriver下载URL失效**
**问题**: 使用的ChromeDriver下载URL可能已失效或不稳定

**修复**: 使用官方Chrome for Testing API
```yaml
# 修复前
wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CDM_VERSION}/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip

# 修复后
DRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${CDM_VERSION}/linux64/chromedriver-linux64.zip"
wget -q "$DRIVER_URL" -O /tmp/chromedriver.zip
```

### 5. **日志文件路径不一致**
**问题**: 错误通知中检查的日志文件路径与实际不匹配

**修复**: 检查多个可能的日志路径
```yaml
# 修复前
if [ -f gzf_spider.log ]; then
  tail -50 gzf_spider.log
fi

# 修复后
if [ -f "gzf_Spider/gzf_spider.log" ]; then
  echo "从 gzf_Spider/gzf_spider.log 读取日志:"
  tail -50 gzf_Spider/gzf_spider.log
elif [ -f "gzf_Spider/src/*.log" ]; then
  echo "从 gzf_Spider/src/ 目录读取日志:"
  tail -50 gzf_Spider/src/*.log
else
  echo "未找到日志文件"
fi
```

## 定时任务配置

当前配置：
- **UTC时间**: 每天 1:00 和 7:00
- **北京时间**: 每天 9:00 和 15:00
- **cron表达式**: `0 1,7 * * *`

```yaml
schedule:
  - cron: '0 1,7 * * *'  # 每天两次，UTC时间1点和7点，即北京时间9点和15点
```

## 需要配置的GitHub Secrets

在GitHub仓库设置中添加以下Secrets：

### 必填项
- `BARK_KEY`: Bark推送密钥（从Bark App获取）

### 可选项（有默认值）
- `BARK_DEFAULT_GROUP`: 默认分组名称（默认: 公租房通知）
- `BARK_SERVER_URL`: Bark服务器地址（默认: https://api.day.app）
- `BARK_SOUND`: 推送声音（默认: telegraph）
- `BARK_LEVEL`: 推送级别（默认: active）

## 测试方法

1. **手动触发**:
   - 进入GitHub仓库的 Actions 页面
   - 选择 "公租房爬虫定时任务" 工作流
   - 点击 "Run workflow"
   - 选择运行模式（normal/debug/test）

2. **查看日志**:
   - 进入 Actions 页面
   - 点击对应的工作流运行记录
   - 查看各个步骤的详细日志

3. **下载日志文件**:
   - 运行完成后，可在 "Artifacts" 部分下载日志文件
   - 日志保留30天

## 预期改进

修复后的workflow将：
- ✅ 更稳定的ChromeDriver安装
- ✅ 更清晰的Bark推送测试
- ✅ 即使BARK_KEY未配置也能继续执行爬虫
- ✅ 更准确的日志文件路径定位
- ✅ 更完整的错误提示信息

## 注意事项

1. **时区**: GitHub Actions使用UTC时间，设置定时任务时注意转换为UTC
2. **并发控制**: 同一时间只运行一个爬虫任务，避免冲突
3. **超时限制**: 单次任务超时时间为30分钟
4. **权限**: 确保workflow有足够的权限运行（actions/checkout@v4）
