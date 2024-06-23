#!/bin/bash

# 等待 MySQL 服务启动
sleep 10

# 初始化数据库
mysql -u root -p${MYSQL_ROOT_PASSWORD} < /docker-entrypoint-initdb.d/init_db.sql
