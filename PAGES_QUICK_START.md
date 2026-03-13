# 🚀 py_tools GitHub Pages 快速配置

## ✅ 已完成的配置

已为 `py_tools` 仓库配置独立的 GitHub Pages 部署，现在可以通过以下路径访问：

```
https://noeverer.github.io/py_tools/
```

## 📋 还需手动完成的步骤（在 GitHub 网页端）

### 步骤 1: 启用 GitHub Pages

1. 打开：https://github.com/Noeverer/py_tools/settings/pages
2. 设置 **Source** 为：`GitHub Actions`
3. 点击 **Save**

### 步骤 2: 等待部署完成

推送到 master 分支后，Actions 会自动部署（约 2-3 分钟）

### 步骤 3: 访问页面

部署完成后访问：
```
https://noeverer.github.io/py_tools/
```

## 📂 新增的文件

- `.github/workflows/deploy-pages.yml` - GitHub Pages 自动部署工作流
- `.github/GITHUB_PAGES_SETUP.md` - 详细配置指南
- `.github/PAGES_CONFIG.md` - 配置说明
- `scripts/setup-pages.sh` - 快速配置脚本

## 🔗 访问路径

| 页面 | URL |
|------|-----|
| 主页 | https://noeverer.github.io/py_tools/ |
| 快速筛选 | https://noeverer.github.io/py_tools/quick.html |
| 详细筛选 | https://noeverer.github.io/py_tools/filter.html |

## 📖 详细文档

- 完整配置指南：[.github/GITHUB_PAGES_SETUP.md](.github/GITHUB_PAGES_SETUP.md)
- 快速配置说明：[.github/PAGES_CONFIG.md](.github/PAGES_CONFIG.md)

## ❓ 常见问题

**Q: 为什么之前无法使用？**
A: `py-tools` 仓库占用了 `https://noeverer.github.io` 主域名，现在改为子路径模式 `https://noeverer.github.io/py_tools/`，不再冲突。

**Q: 需要修改代码中的链接吗？**
A: 不需要。当前使用的绝对路径在子路径模式下仍然可以正常工作。

**Q: 如何查看部署状态？**
A: 访问：https://github.com/Noeverer/py_tools/actions，查看 "GitHub Pages 部署" 工作流。

---

配置已完成！现在去 GitHub 网页端启用 Pages 即可。
