"""
中间件代码，实现三个函数
"""

from typing import Callable
from utils.prompt_loader import load_report_prompts, load_system_prompts
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger

# 完成工具执行的监控--可以使用 @wrap_tool_call 去监控工具的执行
@wrap_tool_call
def monitor_tool(
        # 请求的数据封装
        request: ToolCallRequest,
        # 执行的函数本身，Callable 它是一个顶级的抽象，可以认为是函数就是 Callable 类型
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")
    try:
        result =  handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        # 只要检测到被调用，那么就把报告生成场景的标记设置为True
        if request.tool_call["name"] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return  result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e

# 在模型执行前输出日志--模型监控使用 @before_model 去实现
@before_model
def log_before_model(
        # 整个Agent智能体的状态记录
        state: AgentState,
        # 记录了整个执行过程的上下文信息
        runtime: Runtime
):
    logger.info(f"[log_before_model]即将调用模型：带有{len(state['messages'])}条消息")
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")
    return None

# 每一次在生成提示词之前，调用这个函数
@dynamic_prompt
# 动态切换提示词--使用装饰器 @dynamic_prompt 去实现
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get("report", False)
    # 是报告生成场景，返回报告生成场景提示词内容
    if is_report:
        return load_report_prompts()
    return load_system_prompts()
