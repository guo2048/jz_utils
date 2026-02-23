from jz_utils.env import running_env
from jz_utils.s3_resource_manager import S3ResourceManager
from jz_utils.saver import load_json


class ConfigLoader:
    _config_cache = {}  # 缓存不同环境的配置

    @staticmethod
    def get_config(config_cls, config_name: str = "configs_v2.json", env: str = None):
        """
        获取指定环境的配置

        Args:
            config_cls: 配置类 (Pydantic model)
            config_name: 配置文件名
            env: 环境名称 ('prod', 'debug')，如果为None则使用环境变量

        Returns:
            对应环境的配置对象
        """
        # 确定要使用的环境
        if env is None:
            env = running_env()

        # 缓存键使用 (类名, 环境)
        cache_key = (config_cls.__name__, env)

        # 检查缓存
        if cache_key in ConfigLoader._config_cache:
            return ConfigLoader._config_cache[cache_key]

        # 确保配置文件存在（如果不存在会自动从 S3 下载）
        # 注意：这里 S3ResourceManager 内部可能还依赖旧逻辑或者硬编码路径，
        # 我们假设它能根据 config_name 下载。
        config_path = S3ResourceManager().get_local_file_path(config_name, env=env)

        # 加载配置
        config_data = load_json(config_path)
        config_obj = config_cls.model_validate(config_data)

        # 缓存配置
        ConfigLoader._config_cache[cache_key] = config_obj

        return config_obj
