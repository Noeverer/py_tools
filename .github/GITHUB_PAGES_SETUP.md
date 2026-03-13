# GitHub Pages 配置指南

## 问题描述

你的 `py_tools` 仓库当前绑定了 `https://noeverer.github.io`，这导致其他仓库无法使用独立的 Pages。

## 解决方案

为 `py_tools` 仓库配置独立的 GitHub Pages，部署路径为：
```
https://noeverer.github.io/py_tools/
```

## 配置步骤

### 步骤 1: 启用 GitHub Pages

1. 进入 GitHub 仓库页面：`https://github.com/Noeverer/py_tools`
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Pages**
4. 配置如下：
   - **Source**: 选择 `GitHub Actions`
   - **Build and deployment**: 保持默认
5. 点击 **Save**

### 步骤 2: 配置自定义域名（可选）

如果你想使用自定义域名，可以在 Pages 设置中添加：
```
py-tools.yourdomain.com
```

### 步骤 3: 验证部署

配置完成后，每次推送到 `master` 分支时，会自动触发部署：
```
https://noeverer.github.io/py_tools/
```

## 访问路径说明

### 之前的访问路径（冲突）
```
https://noeverer.github.io/          # py-tools 仓库占用
```

### 现在的访问路径（独立）
```
https://noeverer.github.io/py_tools/          # py_tools 仓库主页
https://noeverer.github.io/py_tools/quick.html  # 快速筛选页面
https://noeverer.github.io/py_tools/filter.html # 详细筛选页面
https://noeverer.github.io/py_tools/index.html  # 仪表板
```

## 其他仓库的 Pages 配置

如果你有其他仓库需要使用 GitHub Pages，可以这样配置：

### 示例：配置 repo2 仓库的 Pages

1. 进入 `https://github.com/Noeverer/repo2/settings/pages`
2. Source 选择 `GitHub Actions`
3. 创建 `.github/workflows/deploy-pages.yml`
4. 部署后访问：`https://noeverer.github.io/repo2/`

## 已配置的文件

- `.github/workflows/deploy-pages.yml` - GitHub Pages 部署工作流
  - 每次 push 到 master 分支自动触发
  - 部署 `docs/` 目录到 GitHub Pages
  - 自动生成数据文件

## 验证部署

### 方法 1: 查看工作流

1. 进入仓库的 Actions 标签
2. 查看 "GitHub Pages 部署" 工作流
3. 检查部署状态

### 方法 2: 访问页面

浏览器打开：
```
https://noeverer.github.io/py_tools/
```

### 方法 3: 查看部署日志

1. 进入 Settings -> Pages
2. 查看 "Deployments" 部分
3. 查看最新的部署状态和 URL

## 注意事项

1. **不要修改主仓库的 Pages 设置**
   - 如果有其他仓库占用了 `https://noeverer.github.io`，保持其配置不变
   - 新仓库使用子路径模式

2. **相对路径配置**
   - 在 HTML 文件中，使用相对路径（如 `./quick.html`）而不是绝对路径
   - 避免硬编码 `https://noeverer.github.io/`

3. **资源引用**
   - CSS/JS/图片等资源使用相对路径
   - 例如：`./assets/style.css` 而不是 `/assets/style.css`

4. **环境变量**
   - 在仓库 Secrets 中配置必要的环境变量（如 BARK_KEY）
   - 不要在代码中硬编码敏感信息

## 常见问题

### Q: 为什么访问 https://noeverer.github.io/py_tools/ 显示 404？
A: 首次部署需要几分钟时间，请等待 Actions 工作流完成。

### Q: 如何切换回主域名？
A: 如果确实需要切换，需要在 Pages 设置中更改 Source，但会影响其他仓库。

### Q: 可以同时部署多个分支吗？
A: 可以，在工作流中配置多个 job，部署到不同的环境。

### Q: 如何设置自定义域名？
A: 在 Pages 设置中添加自定义域名，并配置 DNS 记录。

## 相关链接

- GitHub Actions 文档: https://docs.github.com/en/actions
- GitHub Pages 文档: https://docs.github.com/en/pages
- 部署工作流: `.github/workflows/deploy-pages.yml`
