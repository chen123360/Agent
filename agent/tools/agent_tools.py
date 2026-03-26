"""
存放agent所有工具的代码
"""

from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import random, os
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

# rag 总结服务的类对象
rag = RagSummarizeService()

# rag 总结服务
# description 是必须要写，不然会报错
@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

# 获取天气的函数，这里使用固定的天气，用于测试
@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    return f"城市{city}天气为晴天，温度为25度，空气湿度为60%，南风一级，AQI21，最近六小时概率极低"

# 这里测试用随机抽取一个城市
@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    return random.choice(["北京", "上海", "广州", "深圳", "杭州", "西安", "武汉", "南京", "成都", "苏州"])

# 这里准备一份id列表随机去抽
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
# 获取用户id--用于后续获取生成使用报告用的
@tool(description="获取用户id，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)

# 获取月份--对于给用户生成使用报告，我们不仅需要知道它的id，也需要知道它的月份，比如：生成2023年一月份的报告
# 这里测试同样是创建一个月份列表然后随机返回
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)

# 全局变量
external_data = {}

# 获取外部数据
def generate_external_data():
    """
    根据数据文件来看，我们需要组装返回结果，格式为：
    {
        "user_id": {
            "month": {"特征": xxx, "效率": xxx, ...}
            "month": {"特征": xxx, "效率": xxx, ...}
            "month": {"特征": xxx, "效率": xxx, ...}
            ...
        }
        "user_id": {
            "month": {"特征": xxx, "效率": xxx, ...}
            "month": {"特征": xxx, "效率": xxx, ...}
            "month": {"特征": xxx, "效率": xxx, ...}
            ...
        }
        ...
    }
    为了避免以上数据在 return 中来回返回，我们定义一个全局变量 external_data
    """
    if not external_data:
        # 拿到外部数据的绝对路径
        external_data_path = get_abs_path(agent_conf["external_data_path"])
        if not os.path.exists(external_data_path):
            # 如果不存在则输出错误日志
            raise FileNotFoundError(f"[外部数据]文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            # 因为第一个数据是没用的，所以对数据进行切片，从一取到末尾
            for line in f.readlines()[1:]:
                # 取对于字段的数据
                arr: list[str] = line.strip().split(",")
                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}
                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison
                }

# 获取外部数据，假如要生成使用报告，那么需要知道用户的行为，需要用户的行为数据（测试数据在文件中）
# 所以我们要实现一个工具能从外部系统里面加载这个CSV然后拿到所需要的原始信息
@tool(description="从外部系统获取指定用户在指定月份的使用记录，以纯字符串的形式返回，如果未检索到则返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    # 对于从外部系统加载数据，我们需要有一个工具函数 def generate_external_data(): 的支持，考虑写在一起太臃肿，所以分开写
    # 调用函数生成数据字典
    generate_external_data()

    try:
         return external_data[user_id][month]
    # 如果找不到这个字段
    except KeyError:
        logger.warning(f"[外部数据]未找到用户{user_id}在{month}的记录")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report 已调用"

# 测试
if __name__ == "__main__":
    print(fetch_external_data("1001", "2025-01"))





