# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/10/31 14:33
# @blog: https://blog.csdn.net/weixin_47936614

from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class RagTextEmbeddings(Embeddings):
    def __init__(self, embed_model_path: str, **kwargs):
        self.batch_size = kwargs['batch_size']
        self.device = kwargs['device']
        self.embed_model = SentenceTransformer(embed_model_path, trust_remote_code=True, device=self.device)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        docs_embeddings = self.embed_model.encode(texts,
                                                  task="retrieval.passage",
                                                  batch_size=self.batch_size,
                                                  device=self.device,
                                                  show_progress_bar=True)
        return docs_embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        query_embeddings = self.embed_model.encode([text],
                                                   task="retrieval.query",
                                                   device=self.device)
        return query_embeddings.tolist()[0]

