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
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```
