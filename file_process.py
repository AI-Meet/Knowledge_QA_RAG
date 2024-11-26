# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/10/31 13:59
# @blog: https://blog.csdn.net/weixin_47936614

import os

from langchain_community.document_loaders import TextLoader, UnstructuredWordDocumentLoader, PyPDFLoader

from text_utils.text_split import RagTextSplitter


class RagFileProcessor(object):
    def __init__(self, chunk_size: int = 512):
        self.text_splitter = RagTextSplitter(chunk_size=chunk_size)

    def file_process(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在！")

        if file_path.lower().endswith(".txt"):
            txt_loader = TextLoader(file_path, autodetect_encoding=True)
            txt_docs = txt_loader.load_and_split(text_splitter=self.text_splitter)
            return txt_docs
        elif file_path.lower().endswith(".docx"):
            docx_loader = UnstructuredWordDocumentLoader(file_path, mode="single")
            docx_docs = docx_loader.load_and_split(text_splitter=self.text_splitter)
            return docx_docs
        elif file_path.lower().endswith(".pdf"):
            pdf_loader = PyPDFLoader(file_path)
            pdf_docs = pdf_loader.load_and_split(text_splitter=self.text_splitter)
            return pdf_docs
        else:
            raise TypeError("文件类型不支持，目前仅支持：txt/docx/pdf")

    def get_data(self, file_path: str):
        docs = self.file_process(file_path)
        passage_docs = [doc.page_content.strip() for doc in docs]
        file_name = {"source": os.path.basename(docs[0].metadata['source'])}
        ids = [str(i) for i in range(len(passage_docs))]  # 确保每个文档有唯一的 ID
        meta_datas = [file_name for _ in range(len(passage_docs))]  # 定义元数据信息，包括文件名等
        dict_data = {"texts": passage_docs, "ids": ids, "meta_datas": meta_datas}
        return dict_data

