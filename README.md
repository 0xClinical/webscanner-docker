
## 环境要求

在开始之前，请确保你的系统已安装以下软件：

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 项目介绍

本项目为一个由python作为后端，react作为前端编写的web漏洞扫面器，使用docker构建。一键部署。其中涉及四个镜像，
分别为react框架编写的foretend部分和由flask框架编写的backend后端部分，再加上一个postgresql数据库和一个pikachu靶场镜像组成。
已全部调通，解决问题，一键部署，亲测可用。

## 快速开始

按照以下步骤一键运行该项目：

### 克隆仓库

```bash
git clone https://github.com/0xClinical/webscanner-docker.git
cd webscanner-docker
```

### 构建并启动容器

在项目根目录下运行以下命令:

```bash
docker-compose up --build
```

### 停止并删除容器

如果需要停止并删除所有运行的容器，请使用以下命令：

```bash
docker-compose down
```

### 使用教程

部署完成后，打开浏览器访问 localhost:3000 即可访问网页，输入账号密码后就可登录。