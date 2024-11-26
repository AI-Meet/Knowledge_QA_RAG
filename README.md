# Knowledge_QA_RAG

1. 环境准备
```
conda create --name rag-env python=3.10
cd Knowledge_QA_RAG
conda activate rag-env
pip install -r requirements.txt
```
2. 启动milvus数据库


3. 启动系统服务
```
python main.py
```
或
```
uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

4. 访问页面: 在浏览器中输入下面url地址
```
http://127.0.0.1:8000/
```
