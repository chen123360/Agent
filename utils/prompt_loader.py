"""
提示词模板加载工具
"""

from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

# 加载系统提示词
def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[加载系统提示词]在yaml配置文件中缺少main_prompt_path配置项")
        raise e

    # 读取文件相关的
    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[加载系统提示词]解析系统提示词出错，{str(e)}")
        raise e

# 加载rag提示词
def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[加载rag提示词]在yaml配置文件中缺少rag_summarize_prompt_path配置项")
        raise e

    # 读取文件相关的
    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[加载rag提示词]解析rag提示词出错，{str(e)}")
        raise e

# 加载报告提示词
def load_report_prompts():
    try:
        load_report_prompt = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[加载报告提示词]在yaml配置文件中缺少report_prompt_path配置项")
        raise e

    # 读取文件相关的
    try:
        return open(load_report_prompt, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[加载报告提示词]解析报告提示词出错，{str(e)}")
        raise e

# 测试
if __name__ == '__main__':
    print(load_system_prompts())
    print(load_rag_prompts())
    print(load_report_prompts())