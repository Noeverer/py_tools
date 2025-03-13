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
  mariadb:10.5 \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci

```
