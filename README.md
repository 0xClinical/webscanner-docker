
## 环境要求

在开始之前，请确保你的系统已安装以下软件：

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

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