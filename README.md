"frist push"

# docker mysql start 
```
# 启动容器（含基础配置）
docker run -d \
  --name gzf-db \
  -p 3306:3306 \
  -v /home/ante/03-code/01-daily:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=Liu@06027 \
  -e MYSQL_DATABASE=app_db \
  -e MYSQL_USER=app_user \
  -e MYSQL_PASSWORD=123@1qaz \
  --restart=unless-stopped \
  docker.1ms.run/mariadb:10.5 \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci
```

# next step
- 从微信上推送
- 爬取更加详细的登录后的个人排队信息