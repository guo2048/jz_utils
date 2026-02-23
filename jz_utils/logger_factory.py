import logging
import os
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv

from jz_utils.env import running_prod

# 自动加载 .env 文件中的环境变量
load_dotenv()

_initialized = False


def _setup_logger(project_name: str = None):
    """配置全局根日志记录器"""
    global _initialized
    if _initialized:
        return

    # 优先使用传入参数，否则从环境变量 PROJECT_NAME 读取
    project_name = project_name or os.environ.get("PROJECT_NAME")

    if not project_name:
        raise ValueError(
            "project_name must be provided as an argument or set via the PROJECT_NAME environment variable"
        )

    _logger = logging.getLogger()

    # 防止重复添加 Handler
    if _logger.hasHandlers():
        _initialized = True
        return

    _logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(pathname)s:%(lineno)d] %(message)s")

    console_handler = None
    # 根据环境确定日志文件路径
    if running_prod():
        os.makedirs("/root/logs/", exist_ok=True)
        fname = f"/root/logs/{project_name}_serving.log"
    else:
        fname = f"./{project_name}_test.log"
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        fname,  # 日志文件名
        when="midnight",  # 每天午夜进行轮转
        interval=1,  # 间隔1天
        backupCount=7,  # 保留7天的日志
    )
    file_handler.setFormatter(formatter)

    # 将处理器添加到全局的 logger
    _logger.addHandler(file_handler)
    if console_handler:
        _logger.addHandler(console_handler)

    _initialized = True


def get_logger(name, project_name=None):
    """
    获取一个命名的日志记录器。第一次调用时会初始化根日志记录器。

    Args:
        name: 记录器名称
        project_name: 项目名称。如果不传，则尝试从环境变量 PROJECT_NAME 读取。
    """
    _setup_logger(project_name)
    return logging.getLogger(name)


if __name__ == "__main__":
    # 模拟从环境变量读取
    os.environ["PROJECT_NAME"] = "env_project"
    get_logger("test_env").info("This project name comes from os.environ['PROJECT_NAME']")
