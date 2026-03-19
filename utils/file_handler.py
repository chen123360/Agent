"""
文件处理工具
对于文件的加载，我们需要去重--使用MD5
在向量加载的设计规划中，我们要直接去读取指定的数据文件夹，所以要返回指定文件类型的文件
主要实现以下函数
1.获取文件的MD5值
2.返回文件夹内的文件列表
3.加载PDF文档
4.加载文本文档
"""

import os, hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# 获取文件的MD5的十六进制字符串
def get_file_md5_hex(filepath: str):
    # 对于传入的文件我们首先要做的就是判断它是否存在
    if not os.path.exists(filepath):
        # 如果不存在则输出错误日志
        logger.error(f"[md5计算]文件{filepath}不存在")
        return None

    # 然后对于这个传入的文件，我们还需要判断它是不是文件夹
    if not os.path.isfile(filepath):
        # 如果是文件加则输出错误日志
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return None

    # 计算文件的MD5并赋值给md5_obj
    md5_obj = hashlib.md5()

    # 为了避免文件比较大，计算md5的时候，我们应该分片加载，流式的更新md5值
    # 4kb分片，避免文件过大爆内存
    chunk_size = 4096

    try:
        # 如果我们是以分片去计算md5，那么必须用二进制的方式读取文件
        with open(filepath, "rb") as f:
            # 流式更新要在循环中
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            """
            := 是python新出的语法，等价于：
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """
            # 返回文件的MD5值
            return md5_obj.hexdigest()
    except Exception as e:
        # 如果出错则输出错误日志
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return  None

# 返回文件夹内的指定文件类型的文件列表
# allowed_type: tuple[str] 要返回的文件类型，用元组存储，比如(".pdf", ".txt")
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    # 思路：传入文件路径，这个路径是个文件夹，然后我们应该在文件夹中，遍历所有文件，判断文件类型，然后返回指定类型的文件列表
    # 创建空列表存储要返回的文件
    files = []
    # 先判断是否为文件夹
    if not os.path.isdir(path):
        logger.error(f"[返回指定类型文件的文件列表]路径{path}不是文件夹")
        return allowed_types

    # listdir 列出文件夹里面的文件
    for f in os.listdir(path):
        # endswith 文件以什么结尾（就是文件是什么类型）
        if f.endswith(allowed_types):
            # 添加完整的文件路径到列表中
            files.append(os.path.join(path, f))
    # 在返回文件列表时，我们怕文件列表被动态修改，所以我们以元组形式返回
    return  tuple(files)

# 帮我们加载PDF的文档
def pdf_loader(filepath: str, password: str=None) -> list[Document]:
    return PyPDFLoader(filepath, password).load()

# 加载文本文档
def text_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()