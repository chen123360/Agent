"""
模型工厂代码
作用：帮我们提供模型
"""

from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf

# 创建一个基础抽象类，继承 ABC
class BaseModelFactory(ABC):
    # 定义抽象方法，因为它是抽象方法，所以不写函数体，只写方法头
    @abstractmethod
    # 一般来说实现工厂类，都需要实现一个生成器，让它去生成我们所想要的对象
    # 一般来说返回两个类型，一个聊天模型，一个嵌入模型，所以我们这里定义两个返回类型
    # Embeddings 和 BaseChatModel 分别是 DashScopeEmbeddings 和 ChatTongyi 的父类
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

# 构建聊天模型工厂
class ChatModelFactory(BaseModelFactory):
    # 因为继承了 BaseModelFactory 抽象类，所以需要必须要实现抽象方法
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"])

# 构建嵌入模型工厂
class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

# 得到聊天实例
chat_model = ChatModelFactory().generator()
# 得到嵌入实例
embed_model = EmbeddingsFactory().generator()
