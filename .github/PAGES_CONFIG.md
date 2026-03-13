# 📝 py_tools 仓库 GitHub Pages 配置说明

## 🔧 已完成的配置

### 1. 创建 GitHub Pages 部署工作流
- 文件：`.github/workflows/deploy-pages.yml`
- 功能：自动部署 `docs/` 目录到 GitHub Pages
- 触发条件：推送到 master 分支或手动触发

### 2. 创建配置指南
- 文件：`.github/GITHUB_PAGES_SETUP.md`
- 内容：详细的 GitHub Pages 配置步骤和注意事项

## 📋 下一步操作（需要在 GitHub 网页端完成）

### 步骤 1: 启用 GitHub Pages

1. 访问：https://github.com/Noeverer/py_tools/settings/pages
2. 配置如下：
   - **Source**: `GitHub Actions`
   - 点击 **Save**

### 步骤 2: 等待首次部署

推送到 master 分支后，Actions 会自动部署。

### 步骤 3: 访问部署的页面

部署完成后，通过以下地址访问：
```
https://noeverer.github.io/py_tools/
https://noeverer.github.io/py_tools/quick.html
https://noeverer.github.io/py_tools/filter.html
```

## 🔄 工作流程

```
本地代码修改
  ↓
git push origin master
  ↓
触发 GitHub Actions
  ↓
构建和部署 docs/ 目录
  ↓
自动发布到 GitHub Pages
  ↓
访问：https://noeverer.github.io/py_tools/
```

## 📦 包含的文件

### 部署的内容（docs/ 目录）
- `index.html` - 主页仪表板
- `quick.html` - 快速筛选页面
- `filter.html` - 详细筛选页面
- `README.md` - 文档说明
- `QUICK_START.md` - 快速开始指南
- `FILTER_GUIDE.md` - 筛选使用指南
- `BARK_INTERACTION.md` - Bark 交互说明
- `SHORTCUTS_GUIDE.md` - iOS 快捷指令指南
- `shortcuts/` - iOS 快捷指令文件
- `data/` - 数据文件目录

### GitHub Actions 工作流
- `.github/workflows/deploy-pages.yml` - Pages 部署
- `.github/workflows/gzf_spider.yml` - 公租房爬虫定时任务

## ⚠️ 重要说明

### 关于绝对路径

当前文档中使用了绝对路径（如 `https://noeverer.github.io/py_tools/quick.html`），这些路径在子路径部署模式下仍然可以正常工作。

### 如果需要修改为相对路径

如果未来需要将项目部署到其他域名或路径，可以考虑将绝对路径修改为相对路径：

```html
<!-- 绝对路径 -->
<a href="https://noeverer.github.io/py_tools/quick.html">快速筛选</a>

<!-- 相对路径 -->
<a href="./quick.html">快速筛选</a>
```

## 🆘 常见问题

### Q: 如何验证 Pages 是否配置成功？

A: 访问 https://github.com/Noeverer/py_tools/actions，查看 "GitHub Pages 部署" 工作流的状态。

### Q: 如何查看部署日志？

A: 点击 Actions 工作流中的 "GitHub Pages 部署"，查看详细的部署日志。

### Q: 如何手动触发部署？

A: 进入 Actions 标签 -> 选择 "GitHub Pages 部署" -> 点击 "Run workflow" -> 点击 "Run workflow" 按钮。

### Q: 如何回滚到之前的部署？

A: GitHub Pages 每次部署会保留历史记录，可以在 Settings -> Pages -> Deployments 中查看和回滚。

## 📞 需要帮助？

查看详细配置说明：`.github/GITHUB_PAGES_SETUP.md`

提交问题：https://github.com/Noeverer/py_tools/issues
