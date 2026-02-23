import logging
from logging.handlers import TimedRotatingFileHandler
import os
from jz_utils.env import running_prod

# 创建一个全局日志记录器
_logger = logging.getLogger()
_logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s %(levelname)s [%(pathname)s:%(lineno)d] %(message)s")

fname = "./resys_test.log"
console_handler = None
# 创建一个定时轮转的日志处理器，按天分割
if running_prod():
    os.makedirs("/root/logs/", exist_ok=True)
    fname = "/root/logs/resys_serving.log"
else:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

file_handler = TimedRotatingFileHandler(
    fname,  # 日志文件名
    when="midnight",  # 每天午夜进行轮转
    interval=1,  # 间隔1天
    backupCount=7,  # 保留7天的日志
)
file_handler.setFormatter(formatter)  # 为文件处理器设置格式


# 将处理器添加到全局的 logger
_logger.addHandler(file_handler)
if console_handler:
    _logger.addHandler(console_handler)


def get_logger(name):
    return logging.getLogger(name)


if __name__ == "__main__":
    get_logger("test").info("test")
