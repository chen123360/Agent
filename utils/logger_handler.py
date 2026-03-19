"""
日志工具
对于实现这个功能，我们先写好日志保存在哪个根目录下（不仅要在控制台中打印，还有写入文件中去长期保存）
-> 确保日志目录的存在 -> 进行日志格式的配置 -> 获取日志对象 -> 先创建日志管理器对象 -> 配置日志管理器的 handler 处理器，让它往控制台输出还是往文件输出，或者都输出
-> 配置控制台的handler -> 配置文件handler
"""

import logging
from utils.path_tool import get_abs_path
import os
from datetime import datetime

# 日志保存的根目录
LOG_ROOT = get_abs_path("logs")

# 确保日志目录的存在
# exist_ok=True让 LOG_ROOT 不存在就创建，存在则跳过
os.makedirs(LOG_ROOT, exist_ok=True)

# 基础的日志格式的配置
# asctime 表示日志输出时间 name 表示文件 levelname 表示日志的级别 filename 输出的日志文件名 lineno 输出的行号（文件的哪一行） message 输出的日志信息
# 对于日志的级别，有 DEBUG--调试信息 INFO--一般信息 WARNING--警告信息 ERROR--错误信息 CRITICAL--严重错误
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

def get_logger(
        name: str = "agent",
        # 日志的默认级别
        console_level: int = logging.INFO,
        # 文件级别
        file_level: int = logging.DEBUG,
        # 日志文件
        log_file: str = None
) -> logging.Logger:
    """
    获取日志对象
    :return: 日志对象
    """
    # 创建日志管理器对象
    logger = logging.getLogger(name)
    # 设置日志级别
    logger.setLevel(logging.DEBUG)

    # 避免重复添加Handler
    # 对于这个 if 如果没有写那么会重复打印日志，因为在下面的代码中，我们是使用 logger = get_logger()
    # 它会有很多个文件去获得logger这个对象，每次调用都会去执行函数，确保 if 下面的代码不会重复执行
    if logger.handlers:
        return  logger

    # 配置控制台handler，配置的是流式的输出
    console_handler = logging.StreamHandler()
    # 配置控制台的handler级别
    console_handler.setLevel(console_level)
    # 配置控制台的handler所输出的日志格式
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    # 添加控制台的handler
    logger.addHandler(console_handler)

    # 配置文件handler，对于这个配置，我们需要先判断文件是否存在
    if not log_file:
        # 配置文件的存放路径
        # 对于配置文件名，我们有以下规则：首先是name ，然后是时间....
        # strftime 对时间进行格式
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
    # 构建文件
    # FileHandler 负责将日志写入文件，参数：传入文件的路径，配置编码
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    # 配置文件handler级别
    file_handler.setLevel(file_level)
    # 配置文件handler所输出的日志格式
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    # 添加文件handler
    logger.addHandler(file_handler)

    return logger

# 快捷获取日志管理器，以后要使用只需要引入这个文件，import这个变量logger，然后调用 get_logger() 方法即可
logger = get_logger()

# 测试
if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
