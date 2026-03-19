"""
路径工具
为整个工程提供统一的绝对路径
不使用相对工具是因为怕在解析相对路径时报错，那么会找不到数据

实现的过程
获取工程所在的根目录
传递相对路径，获得绝对路径（在这里调用获取工程根目录的函数，然后把相对路径和根目录结合，得到完整绝对路径）
"""

import os

def get_project_root():
    """
    获取工程所在的根目录
    对于实现这个要求，我们先获取当前文件的绝对路径，然后再得到当前文件的文件夹绝对路径（因为这个路径只能一层一层去获取）
    最后才能得到工程的根目录，并把它返回
    :return:字符串根目录
    """
    # abspath() 获取绝对路径，__file__ 指定是当前文件，所以这个变量接收的是当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    # 获取当前文件的文件夹绝对路径
    current_dir = os.path.dirname(current_file)
    # 获取工程根目录
    project_root = os.path.dirname(current_dir)
    return project_root

def get_abs_path(relative_path: str) -> str:
    """
    传递相对路径，获取绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    # 先获得工程的根目录
    project_root = get_project_root()
    # 把传入的相对路径和工程根目录通过join方法结合，得到完整的绝对路径
    return os.path.join(project_root, relative_path)

# 测试
if __name__ == '__main__':
    print(get_abs_path('config/config.txt'))