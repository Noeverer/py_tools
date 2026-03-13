#!/bin/bash
# GitHub Pages 快速配置脚本

echo "=========================================="
echo "  py_tools 仓库 GitHub Pages 快速配置"
echo "=========================================="
echo ""

# 检查是否在 git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 错误：不在 git 仓库中"
    echo "   请在项目根目录下运行此脚本"
    exit 1
fi

echo "✅ 当前在 git 仓库中"
echo ""

# 显示当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 当前分支: $CURRENT_BRANCH"
echo ""

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  警告：有未提交的更改"
    echo "   是否继续提交并推送？"
    read -p "   (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 操作已取消"
        exit 1
    fi

    # 添加所有更改
    echo "📝 正在添加更改..."
    git add .
    git commit -m "chore: 配置 GitHub Pages 部署工作流"
    echo ""
fi

# 推送到远程仓库
echo "📤 正在推送到远程仓库..."
git push origin $CURRENT_BRANCH
echo ""

# 检查推送是否成功
if [ $? -eq 0 ]; then
    echo "✅ 推送成功！"
    echo ""
    echo "=========================================="
    echo "  下一步操作"
    echo "=========================================="
    echo ""
    echo "1. 访问 GitHub 仓库："
    echo "   https://github.com/Noeverer/py_tools"
    echo ""
    echo "2. 进入 Settings -> Pages"
    echo "   设置 Source 为：GitHub Actions"
    echo "   点击 Save"
    echo ""
    echo "3. 等待 Actions 部署完成（约 2-3 分钟）"
    echo "   访问：https://github.com/Noeverer/py_tools/actions"
    echo ""
    echo "4. 部署完成后，访问以下地址："
    echo "   https://noeverer.github.io/py_tools/"
    echo ""
    echo "=========================================="
    echo "  相关文档"
    echo "=========================================="
    echo ""
    echo "- GitHub Pages 配置指南："
    echo "  .github/GITHUB_PAGES_SETUP.md"
    echo ""
    echo "- 快速配置说明："
    echo "  .github/PAGES_CONFIG.md"
    echo ""
else
    echo "❌ 推送失败，请检查网络连接或仓库权限"
    exit 1
fi

echo "✅ 配置完成！"
echo ""
