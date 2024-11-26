# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/11/20 16:32
# @blog: https://blog.csdn.net/weixin_47936614

import os
import shutil

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pymilvus import Collection, connections
from pymilvus.orm import utility

from milvus_vector import vector_store, config
from file_process import RagFileProcessor
from protocol.prompts import prompt_template
from protocol.mode import ChatRequest

# 初始化 FastAPI 应用
app = FastAPI(title="Knowledge_QA_RAG API", description="API for data process and retrieval using Milvus and LangChain.")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置模板目录
templates = Jinja2Templates(directory="templates")


# 渲染主页
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("qa.html", {"request": request})


@app.post("/rag/chat/")
async def chat(request: ChatRequest):
    """
    根据用户问题，从向量库检索并返回回答。
    """
    print(f"Q: {request.question}")
    try:
        # 初始化 OpenAI Chat 模型
        llm = ChatOpenAI(model=config.llm_model_name, api_key=config.api_key, base_url=config.base_url)
        # 定义 Prompt 模板
        qa_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        # 定义搜索参数
        search_kwargs = {"score_threshold": 0.3, "k": 5}
        retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs=search_kwargs)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": qa_prompt},
            return_source_documents=True
        )
        result = qa_chain.invoke({"query": request.question})
        answer_result = result.get("result", "")
        print(f"A: {answer_result}")

        source = {"source_documents": [{"content": doc.page_content, "metadata": doc.metadata} for doc in
                                       result.get("source_documents", [])]}
        print(f"source: {source}")

        return {"answer": answer_result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/rag/clear/")
async def clear_knowledge(collection_name: str = config.milvus_collection_name,
                          host: str = config.milvus_host,
                          port: int = config.milvus_port):
    """
    清空 Milvus 知识库集合，并删除指定目录中的文件
    """
    folder = "./upload_files"
    try:
        connections.connect("default", host=host, port=port)
        if utility.has_collection(collection_name):
            collection = Collection(name=collection_name)
            collection.drop()
            print(f"Collection '{collection_name}' 成功删除.")
        else:
            print(f"Collection '{collection_name}' 不存在.")
        connections.disconnect("default")

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        return {"message": f"知识库清空: Collection '{collection_name}' 删除, 文件夹 '{folder}' 清空."}
    except Exception as e:
        return {"error": f"知识库清空失败. 原因: {str(e)}"}


@app.post("/rag/create/")
async def create_knowledge(file: UploadFile = File(...)):
    """
    上传文件到指定目录后，处理文件内容并添加到向量库。
    """
    folder = './upload_files'  # 文件存储目录
    os.makedirs(folder, exist_ok=True)  # 确保目录存在
    file_path = os.path.join(folder, file.filename)

    try:
        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        folder: str = './upload_files'
        file_path = os.path.join(folder, file.filename)

        # 初始化文件处理器
        file_processor = RagFileProcessor(chunk_size=64)
        # 处理文件内容并插入到向量库
        text_datas = file_processor.get_data(file_path=file_path)

        # 连接到 Milvus
        vector_store.add_texts(**text_datas)
        return {
            "status": "success",
            "message": f"文件 '{file.filename}' 上传成功并添加至向量数据库.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"文件 '{file.filename}'处理失败. 原因: {str(e)}",
        }


