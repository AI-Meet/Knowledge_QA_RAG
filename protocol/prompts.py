# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/11/20 16:17
# @blog: https://blog.csdn.net/weixin_47936614

prompt_template = """
Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say "sorry, I can't answer this question.", don't try to make up an answer.
{context}
Question: {question}
Answer in Chinese:
"""