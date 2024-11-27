# Knowledge_QA_RAG

## Introduction
本系统是一种基于 RAG 的知识库问答系统简单示例，采用前后端分离的架构设计，融合了多种技术和方法。具体详情可参考：[https://blog.csdn.net/weixin_47936614/article/details/143932997](https://blog.csdn.net/weixin_47936614/article/details/143932997)

本系统是在 Windows 11 上进行部署和运行的，关于milvus向量数据库的安装和启动可以参考以下步骤：
1. 勾选`适用于Linux的Windows子系统`和`虚拟机平台`

![image](https://github.com/user-attachments/assets/32200acc-042e-48d0-a31c-ebc07511f963)

2. 点击 `确定` 并重新启动计算机
3. 安装WSL. 以管理员身份打开命令提示符，输入以下命令：
- 在 PowerShell 中设置 WSL 2 为默认版本： 
```
wsl --set-default-version 2
```
- 更新 WSL 内核，使用国内网络建议添加`--web-download`： 
```
wsl --update --web-download
```
安装成功后的结果如下：

![abe944eb639649fae89175ed09af9fdd](https://github.com/user-attachments/assets/74fc0c97-cf3c-47c6-b3a2-240ba97a44ff)

4. 下载安装docker-desktop
进入官网下载对应的版本安装即可，官网链接：[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

5. 验证是否安装成功：
```
docker --version
docker-compose --version
```

![a263610663c19d4046f28773a1126369](https://github.com/user-attachments/assets/1f8e801b-b2db-4644-83d7-5da10f4e5764)

6. milvus向量数据库安装
- 创建milvus文件夹，并在该文件夹下创建多个子文件夹，如下：
![image](https://github.com/user-attachments/assets/4b6a179f-86e8-4093-b2f0-259030f32627)

- 下载milvus
进入下载页面：[https://github.com/milvus-io/milvus/releases](https://github.com/milvus-io/milvus/releases)
选择milvus版本及其对应的yml文件，点击下载即可，如下：

![image](https://github.com/user-attachments/assets/5b8804ca-5c6b-4102-82ac-d47eee31c77b)

- 将下载好的`milvus-standalone-docker-compose.yml`重命名为`docker-compose.yml`，并放入milvus文件中，如下：

![image](https://github.com/user-attachments/assets/037c6ecf-28a0-4569-ada0-7143a24ebfe0)

- 在milvus文件夹中启动cmd命令，输入以下命令：
```
docker compose up -d
docker compose ps
docker port milvus-standalone 19530/tcp
```
运行结果如下：

![694be819cd99abc328136139f2e8e8d2](https://github.com/user-attachments/assets/2506153f-9625-42dd-b09c-db01e5ded5d6)

![1a3086ad4519524717991dffa47cce29](https://github.com/user-attachments/assets/a8e9a22c-2b1c-4c95-9e15-fe8d6cb0c3ee)

至此，milvus数据库部署成功！

7. Attu图形化界面安装
下载地址：[https://github.com/zilliztech/attu/releases](https://github.com/zilliztech/attu/releases)
选择对应的版本直接下载安装即可：

![image](https://github.com/user-attachments/assets/b4e96c46-e5e8-42e0-aae9-670008d3ff53)

## Usage
1. 环境准备
```
conda create --name rag-env python=3.10
cd Knowledge_QA_RAG
conda activate rag-env
pip install -r requirements.txt
```

2. 启动milvus数据库

![image](https://github.com/user-attachments/assets/4d2a37ad-3f74-4b72-969c-685c6b023e96)

3. 启动系统服务
```
python main.py
```
或
```
uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

4. 访问页面: 在浏览器中输入下面url地址即可访问
```
http://127.0.0.1:8000/
```
