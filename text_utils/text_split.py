# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/10/31 11:17
# @blog: https://blog.csdn.net/weixin_47936614

import re
from typing import List

from langchain.text_splitter import CharacterTextSplitter


class RagTextSplitter(CharacterTextSplitter):
    def __init__(self, chunk_size: int = 1024):
        super().__init__()
        self.chunk_size = chunk_size

    def split_text(self, text: str) -> List[str]:
        text = re.sub(r"\n{3,}", "\n", text)  # 移除三个或更多的连续换行符，用一个换行符代替
        text = re.sub(r'\s+', ' ', text)  # 替换所有的空白字符为单个空格
        text = text.replace("\n\n", "")  # 移除双换行符

        sent_sep_pattern = re.compile(r'([﹒﹔﹖﹗．。！？]["’”」』]{0,2})')  # 用于匹配中文句子结束标点符号以及紧随其后的引号
        sentences = []
        current_chunk = ""

        start = 0
        for match in sent_sep_pattern.finditer(text):
            end = match.end()
            sentence = text[start:end]
            start = end

            # 检查当前块是否能容纳新句子
            if len(current_chunk) + len(sentence) > self.chunk_size:  # 不能容纳
                if current_chunk:
                    sentences.append(current_chunk)
                current_chunk = sentence
            else:  # 可以容纳
                current_chunk += sentence

        if len(sentences) == 0:
            sentences.append(text.strip())

        final_sentences = []
        for line in sentences:
            if len(line) <= self.chunk_size:
                final_sentences.append(line)
            else:
                final_sentences.extend(self.split_string(line, self.chunk_size))
        return final_sentences

    @staticmethod
    def split_string(text: str, size: int) -> List[str]:
        """
        Split the input string into chunks of specified size, splitting at the last space if needed.

        Parameters:
            text (str): The input string to be split.
            size (int): The size of each chunk.

        Returns:
            list: A list containing the chunks of the input string.
        """
        # 定义句子或标记分割符号列表
        SENTENCE_BREAK_SYMBOLS = [' ', '.', '!', '?', ',', ';', ':', '。', '？', '！', '，', '；', '：']
        chunks = []
        start = 0
        while start < len(text):
            end = start + size
            if end < len(text):
                # 在最后一个空格处进行切分
                while end > start and text[end - 1] not in SENTENCE_BREAK_SYMBOLS:
                    end -= 1
            chunks.append(text[start:end])
            start = end
        return chunks
