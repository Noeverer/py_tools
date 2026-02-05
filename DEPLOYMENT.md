# GitHub Actions 部署文档

## 概述

本项目使用 GitHub Actions 实现自动修正部署流程，包括代码质量检查、自动修复、依赖管理和部署通知。

## 工作流说明

### 1. auto-fix-deploy.yml - 主部署工作流

**触发条件**:
- Push 到 `main` 或 `develop` 分支
- 手动触发 (workflow_dispatch)

**包含的 Jobs**:
- `lint-and-fix`: 代码质量检查和自动修复
- `dependency-check`: 依赖检查和修复
- `build`: 构建和验证
- `deploy`: 部署执行

**手动触发选项**:
```bash
# 通过 GitHub UI 触发
# Repository -> Actions -> Auto Fix & Deploy -> Run workflow
```

### 2. auto-fix-lint.yml - 代码质量检查

**触发条件**:
- Pull Request
- Push 到 main/develop 分支

**包含的 Jobs**:
- `python-lint`: Python 代码检查和修复 (black, isort, autoflake, flake8)
- `javascript-lint`: JavaScript/TypeScript 代码检查和修复 (eslint, prettier)

### 3. notification.yml - 部署通知

**触发条件**:
- auto-fix-deploy 工作流完成

**支持的通知渠道**:
- Slack
- 钉钉机器人
- 企业微信机器人
- GitHub Issues (部署失败时自动创建)

## 配置说明

### 环境变量

在 Repository Secrets 中配置以下变量：

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `SLACK_WEBHOOK_URL` | Slack 机器人 Webhook URL | 否 |
| `DINGTALK_WEBHOOK_URL` | 钉钉机器人 Webhook URL | 否 |
| `WECHAT_WORK_WEBHOOK_URL` | 企业微信机器人 Webhook URL | 否 |

### 配置 Webhook

#### Slack
1. 进入 Slack App Settings
2. 创建 Incoming Webhook
3. 复制 Webhook URL 到 Repository Secrets

#### 钉钉
1. 在钉钉群设置中添加"自定义机器人"
2. 选择"加签"安全设置
3. 复制 Webhook URL 到 Repository Secrets

#### 企业微信
1. 在企业微信群设置中添加"机器人"
2. 复制 Webhook URL 到 Repository Secrets

## 使用说明

### 本地运行自动修复脚本

```bash
# 进入项目目录
cd /mnt/workspace/03-apps/py_tools

# 运行自动修复脚本
./scripts/auto-fix.sh
```

### 手动触发部署

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "Auto Fix & Deploy" 工作流
4. 点击 "Run workflow" 按钮
5. 选择分支和环境参数
6. 点击 "Run workflow" 确认

### 查看部署日志

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择对应的工作流运行记录
4. 点击具体的 Job 查看详细日志

## 工作流程

```
代码提交
  ↓
触发工作流
  ↓
lint-and-fix (代码检查和修复)
  ↓
dependency-check (依赖检查和修复)
  ↓
build (构建验证)
  ↓
deploy (部署)
  ↓
notification (发送通知)
```

## 故障排查

### 工作流失败

1. 查看失败 Job 的日志
2. 检查是否有语法错误
3. 验证依赖是否正确安装
4. 检查环境变量配置

### 代码自动修复未生效

1. 检查文件权限
2. 验证 linting 工具是否正确安装
3. 确认文件路径是否被排除

### 通知未收到

1. 检查 Webhook URL 是否正确配置
2. 验证机器人是否被禁用
3. 查看工作流日志中的通知发送状态

## 最佳实践

1. **代码提交前**: 在本地运行 `./scripts/auto-fix.sh` 进行预检查
2. **Pull Request**: 利用 auto-fix-lint 工作流自动修复代码
3. **部署环境**: 使用不同的环境变量配置 dev/staging/prod
4. **监控通知**: 配置至少一种通知渠道，及时获取部署状态

## 后续改进

- [ ] 支持多环境部署配置
- [ ] 添加回滚机制
- [ ] 集成性能监控
- [ ] 添加更详细的部署报告
