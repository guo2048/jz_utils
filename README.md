# jz_utils

一个从推荐系统项目中提取出来的通用工具库。

## 功能模块

- **S3 & Configs**: 配置文件管理和 S3 相关的下载、上传功能。
- **Singleton & Telegram**: 单例模式实现、Telegram 消息发送机器人。
- **Logger**: 日志系统初始化与配置。
- **MQ**: 消息队列消费者封装。
- **Cron**: 定时任务。
- **其它依赖项**: 环境变量、序列化/反序列化、加解密方法。

## 安装

本地安装（开发模式）：

```bash
pip install -e .
```

## 使用说明

### ConfigLoader

支持外部传入 Pydantic 模型进行配置加载：

```python
from jz_utils.configs import ConfigLoader
from pydantic import BaseModel

class MyConfig(BaseModel):
    key: str

config = ConfigLoader.get_config(MyConfig, env="prod")
```
