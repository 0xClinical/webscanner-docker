FROM area39/pikachu:latest

# 设置工作目录
WORKDIR /app

# 复制数据库初始化脚本到容器中
COPY init_db.sql /docker-entrypoint-initdb.d/init_db.sql

# 复制初始化脚本到容器中
COPY init_db.sh /usr/local/bin/init_db.sh

# 赋予初始化脚本执行权限
RUN chmod +x /usr/local/bin/init_db.sh

# 修改启动脚本，添加数据库初始化步骤
RUN sed -i 's|exec "$@"|/usr/local/bin/init_db.sh \&\& exec "$@"|' /run.sh

EXPOSE 80

CMD ["/run.sh"]
