"""
向量存储服务
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document

from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import text_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.path_tool import get_abs_path
import os
from utils.logger_handler import logger

# 创建向量存储服务类
class VectorStoreService:
    # 设置成员变量
    def __init__(self):
        # 向量存储--我们使用Chroma
        self.vector_store = Chroma(
            # 集合名称--类似于表名
            collection_name=chroma_conf["collection_name"],
            # 模型
            # 对于嵌入模型，可能有聊天模型，可能有嵌入模型之类的，所以这里不写死，而是写在工厂文件中
            embedding_function=embed_model,
            # 向量存储目录
            persist_directory=chroma_conf["persist_directory"]
        )
        # 文档分割器
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len
        )

    # 获取检索器对象
    def get_retriever(self):
        # as_retriever 调用这个就能获得检索器对象
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    # 加载文档
    # 从数据文件夹内读取数据文件，然后转为向量存入向量库
    # 在这过程中要计算文档的MD5，然后判断是否已经存在
    def load_document(self):
        # 检查文件夹内MD5，判断文件是否存在
        def check_md5_hex(md5_for_check: str):
            # 对于从配置文件中拿到的路径都是相对路径，所以这里要转换成绝对路径
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 相当于创建文件
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                # 如果不存在，则返回False--md5没处理过
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        # 如果存在，则返回True--md5处理过
                        return True
                # 如果不存在，则返回False--md5没处理过
                return  False

        # 保存md5函数
        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        # 读取文件，拿到全部的document对象
        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return text_loader(read_path)
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)
            # 如果哪种类型都不是，那么返回空列表表示什么都没读到
            return []

        # 调用返回文件夹内的指定文件类型的文件列表函数，拿到允许类型的文件列表
        allowed_file_path: list[str] = listdir_with_allowed_type(
            # 要使用绝对路径不然报错
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )

        # 对文件列表进行遍历
        for path in allowed_file_path:
            # 获取文件的MD5
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]文件{path}已处理过，跳过")
                continue
            try:
                documents: list[Document] = get_file_documents(path)
                if not documents:
                    logger.info(f"[加载知识库]文件{path}没有有效内容，跳过")
                    continue
                split_document: list[Document] = self.splitter.split_documents(documents)

                if not split_document:
                    logger.info(f"[加载知识库]文件{path}分片后没有有效内容，跳过")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理好的md5值，避免下次重复加载
                save_md5_hex(md5_hex)

                # 打印日志
                logger.info(f"[加载知识库]文件{path}处理成功")
            except Exception as e:
                # exc_info=True 表明会进行详细的报错堆栈，如果为False，则只记录报错信息本身
                logger.error(f"[加载知识库]文件{path}处理失败，{str(e)}", exc_info=True)

# 测试
if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)






