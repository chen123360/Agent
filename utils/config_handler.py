"""
配置文件处理
在工程项目中，通常使用 yaml 的格式去写配置文件
yaml 的格式和字典很像：k: v 这样就能管理你的配置项
在这个项目中，我们规划实现四个配置文件
1.关于RAG的
2.关于向量数据库的
3.关于提示词的
4.关于Agent的
"""

import yaml
from utils.path_tool import get_abs_path

# 加载和RAG相关的配置文件
# 传入参数：配置文件路径 编码格式
def load_rag_config(config_path: str=get_abs_path("config/rag.yml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        # 全量加载yaml文件
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载和向量数据库相关的配置文件
def load_chroma_config(config_path: str=get_abs_path("config/chroma.yml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        # 全量加载yaml文件
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载和提示词相关的配置文件
def load_prompts_config(config_path: str=get_abs_path("config/prompts.yml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        # 全量加载yaml文件
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载和Agent相关的配置文件
def load_agent_config(config_path: str=get_abs_path("config/agent.yml"), encoding="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        # 全量加载yaml文件
        return yaml.load(f, Loader=yaml.FullLoader)

# 创建对应变量，后续只需要导入这个配置文件，引用这个变量就可以获取配置项了
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()

# 测试
if __name__ == "__main__":
    print(rag_conf["chat_model_name"])