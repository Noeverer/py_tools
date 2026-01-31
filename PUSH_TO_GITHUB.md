# 推送至GitHub说明

## 步骤1：创建GitHub仓库
1. 登录GitHub
2. 点击“New repository”
3. 输入仓库名称，例如 `house-crawler`
4. 点击“Create repository”

## 步骤2：连接远程仓库并推送代码
```bash
cd /home/02-code/02-gzf/py_tools-master/refactored_project
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

## 步骤3：配置GitHub Actions Secrets
1. 进入仓库页面
2. 点击“Settings”标签
3. 在左侧菜单中点击“Secrets and variables”，然后点击“Actions”
4. 点击“New repository secret”
5. Name输入：`BARK_KEY`
6. Secret输入您的Bark推送密钥
7. 点击“Add secret”

## 步骤4：启用GitHub Actions
1. 点击仓库页面上的“Actions”标签
2. 如果看到提示启用工作流，点击“Enable workflow”
3. Actions将会按照配置的定时任务自动运行

## 验证Action运行结果
1. 点击仓库页面上的“Actions”标签
2. 点击左侧的“Crawl House Data”工作流
3. 您可以看到每次运行的日志和结果
4. 运行成功后，`data/`目录下会产生新的CSV文件，包含爬取到的房源信息

## 查看收集的数据
1. 在仓库中，您可以直接查看`data/`目录下的CSV文件
2. 每次Action运行后，都会生成按日期命名的CSV文件，如`house_data_YYYY-MM-DD.csv`
3. 这些文件包含了爬取到的房源信息