# 公租房爬虫通知脚本

此目录包含用于发送通知的Python脚本。

## 脚本列表

- `send_bark_notification.py`: 用于发送Bark通知
- `send_notification_email.py`: 用于发送邮件通知

## 功能说明

### send_bark_notification.py
- 发送任务执行状态到Bark推送服务
- 包含错误处理和URL格式验证
- 自动编码URL参数以确保正确传输

### send_notification_email.py
- 发送HTML格式的邮件通知
- 包含任务执行状态详情
- 使用环境变量进行配置

## 使用方式

这些脚本由GitHub Actions工作流自动调用，不需要手动执行。