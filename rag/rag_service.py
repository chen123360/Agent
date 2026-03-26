"""
实现RAG总结服务的类
作用：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from langchain_core.documents import Document
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser

# 调试输出提示词内容
def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return  prompt

# 构建RAG总结服务的类
class RagSummarizeService(object):
    def __init__(self):
        # 创建向量存储对象
        self.vector_store = VectorStoreService()
        # 创建检索器对象
        self.retriever = self.vector_store.get_retriever()
        # 创建提示词文本对象
        self.prompt_text = load_rag_prompts()
        # 创建提示词模板对象
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        # 创建模型对象
        self.model = chat_model
        # 创建rag当前执行的链对象--它需要写一个方法 ._init_chain
        self.chain = self._init_chain()

    def _init_chain(self):
        # 构建一个链对象
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return  chain

    # 检索文档的函数
    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    # 总结的函数
    def rag_summarize(self, query: str) -> str:
        # 参考资料的文档
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        # 把他拼接为字符串
        for doc in context_docs:
            counter += 1
            context += f"[参考资料{counter}]：参考资料内容： {doc.page_content} | 参考元数据：{doc.metadata}\n"
        return self.chain.invoke({"input": query, "context": context})

# 测试
if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize("小户型适合哪些扫地机器人"))