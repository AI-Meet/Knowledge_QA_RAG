# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/11/22 18:53
# @blog: https://blog.csdn.net/weixin_47936614

from langchain_milvus import Milvus

from config import RagConfig
from text_utils.text_embeddings import RagTextEmbeddings

# 加载配置
config = RagConfig()

# 配置索引参数和搜索参数
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 100}
}

search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10}
}

# 初始化 Milvus 向量存储
vector_store = Milvus(
    embedding_function=RagTextEmbeddings(embed_model_path=config.text_embeddings_model_path,
                                         batch_size=32,
                                         device=config.device),
    collection_name=config.milvus_collection_name,
    consistency_level="Bounded",
    connection_args={"host": config.milvus_host, "port": config.milvus_port},
    index_params=index_params,
    search_params=search_params
)
