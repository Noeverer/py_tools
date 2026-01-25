# 公租房爬虫自动化任务配置指南

## 概述

本指南介绍如何配置公租房爬虫（mySpider_gongzufang.py）的自动化执行，通过GitHub Actions实现定时运行爬虫任务，并配置Bark和邮件通知功能。

## 功能特性

- 定时自动运行爬虫
- 多种运行模式（正常、调试、测试）
- Bark移动推送通知
- 邮件通知
- 日志存档
- 并发控制

## 目录结构

```
py_tools/
├── gzf_Spider/
│   ├── src/
│   │   ├── mySpider_gongzufang.py
│   │   ├── conndb.py
│   │   └── check_gzf.py
│   └── requirement.txt
├── .github/
│   └── workflows/
│       └── gzf_spider.yml  # 自动化工作流配置
├── GZF_SPIDER_AUTOMATION.md  # 本指南
└── README.md
```

## 快速开始

### 1. 工作流配置

自动化任务的配置文件位于 `.github/workflows/gzf_spider.yml`，包含以下功能：

- **定时执行**: 每天北京时间 9:00 和 15:00 执行
- **手动触发**: 支持三种运行模式
- **环境配置**: 自动安装Chrome浏览器和驱动
- **通知机制**: 支持Bark和邮件通知

### 2. 配置GitHub Secrets

要启用通知功能，需要在GitHub仓库设置中配置Secrets：

#### 2.1 邮件通知配置

进入仓库 Settings → Secrets and variables → Actions，添加以下Secrets：

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-app-password
RECEIVER_EMAIL=recipient@example.com
```

#### 2.2 Bark通知配置

获取Bark应用的推送密钥，添加到Secrets：

```
BARK_URL=https://api.day.app/your_bark_key
```

#### 2.3 数据库配置（可选）

如果需要连接数据库，可以配置：

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=house_data
```

### 3. 运行模式

工作流支持三种运行模式：

- **normal**: 正常执行爬虫任务
- **debug**: 启用详细日志输出
- **test**: 模拟执行，不实际访问网站

## 详细配置说明

### 3.1 Cron表达式

当前配置的定时任务使用以下cron表达式：
```
0 1,7 * * *  # UTC时间1:00和7:00，对应北京时间9:00和15:00
```

您可以根据需要修改执行时间。

### 3.2 并发控制

工作流配置了并发控制，确保同一时间只运行一个爬虫实例：

```yaml
concurrency:
  group: gzf-spider
  cancel-in-progress: false
```

### 3.3 超时设置

工作流设置了30分钟的超时限制，防止任务无限挂起：

```yaml
timeout-minutes: 30
```

## 安全考虑

- 所有敏感信息（如密码、API密钥）必须通过GitHub Secrets管理
- 不要在代码或日志中暴露敏感信息
- 限制工作流的权限，仅授予必要权限

## 维护指南

### 1. 监控任务执行

定期检查GitHub Actions的执行日志，确保任务正常运行。

### 2. 通知验证

验证Bark和邮件通知是否正常接收。

### 3. 日志管理

工作流会自动保存日志文件作为artifacts，保留30天。

### 4. 版本更新

定期更新浏览器和驱动版本以保持兼容性。

## 故障排除

### 常见问题

1. **Chrome或ChromeDriver安装失败**
   - 检查版本兼容性
   - 确认网络连接正常

2. **邮件发送失败**
   - 验证SMTP配置和凭据
   - 检查是否启用了应用专用密码

3. **爬虫被反爬机制阻止**
   - 调整请求频率
   - 更换IP或使用代理

### 调试步骤

1. 查看工作流日志
2. 检查环境配置
3. 验证依赖安装
4. 测试网络连接
5. 手动触发测试模式

## 扩展性

该设计允许未来扩展：

- 添加其他通知渠道
- 增加更多的爬虫任务
- 集成监控和告警系统
- 增加数据质量检查机制

## 附录：Bark应用获取方法

1. 在iOS设备上安装Bark应用（App Store）
2. 启动应用，复制提供的URL
3. 或使用公共服务器：`https://api.day.app/your_custom_key`
4. 将完整URL设置到GitHub Secrets中

## 附录：邮件服务配置

### Gmail配置
1. 启用两步验证
2. 生成应用专用密码
3. 将应用密码设置为EMAIL_PASS

### 其他邮箱服务
1. 获取SMTP服务器地址
2. 确认端口号（通常是587或465）
3. 提供账户凭据