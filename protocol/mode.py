# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/11/20 16:33
# @blog: https://blog.csdn.net/weixin_47936614

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str

