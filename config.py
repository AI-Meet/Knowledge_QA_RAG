# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/10/31 14:30
# @blog: https://blog.csdn.net/weixin_47936614

import os

import torch
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv()


class RagConfig:
    # FastAPI 服务配置
    fastapi_host = os.getenv("fastapi_host")
    fastapi_port = os.getenv("fastapi_port")

    # Milvus 配置
    milvus_host = os.getenv("milvus_host")
    milvus_port = os.getenv("milvus_port")
    milvus_collection_name = os.getenv("milvus_collection_name")

    # OpenAI 设置
    base_url = os.getenv("openai_base_url")
    api_key = os.getenv("openai_api_key")
    llm_model_name = os.getenv("openai_llm_model_name")

    # 嵌入模型路径
    text_embeddings_model_path = os.getenv("text_embeddings_model_path")

    # 设备设置
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

