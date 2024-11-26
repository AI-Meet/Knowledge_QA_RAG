# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: CS_木成河
# @time: 2024/11/26 10:14
# @blog: https://blog.csdn.net/weixin_47936614

import uvicorn

from milvus_vector import config

if __name__ == '__main__':
    # 主函数启动方式
    uvicorn.run(
        "server:app",  # 指定模块名和应用实例
        host=config.fastapi_host,  # 本地地址
        port=int(config.fastapi_port),  # 端口
        reload=True  # 开启热重载
    )
