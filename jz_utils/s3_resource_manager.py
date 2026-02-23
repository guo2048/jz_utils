import logging
import os

from jz_utils.env import running_env
from jz_utils.s3 import (
    download_file as s3_download_file,
)
from jz_utils.s3 import (
    download_folder as s3_download_folder,
)
from jz_utils.s3 import (
    upload_file as s3_upload_file,
)
from jz_utils.singleton import singleton

logger = logging.getLogger(__name__)


@singleton
class S3ResourceManager:
    def __init__(self, bucket_name: str = None, base_cache_dir: str = None):
        self.base_cache_dir = base_cache_dir or "./resource"
        self.bucket_name = bucket_name or "recommend-2026"
        os.makedirs(self.base_cache_dir, exist_ok=True)
        logger.info(f"S3ResourceManager 初始化完成，缓存目录: {self.base_cache_dir}")

    def get_local_file_path(self, relative_file_path: str, is_path: bool = False, env: str = None) -> str:
        if env is None:
            env = running_env()

        local_target_path = os.path.join(self.base_cache_dir, env)
        remote_path = f"{env}/{relative_file_path}"
        local_path = os.path.join(local_target_path, relative_file_path)

        if os.path.exists(local_path):
            logger.debug(f"文件已存在: {local_path}")
            return local_path

        logger.info(f"下载文件: {remote_path} -> {local_path}")
        try:
            if is_path:
                s3_download_folder(remote_path, local_target_path, bucket_name=self.bucket_name)
            else:
                s3_download_file(remote_path, local_target_path, bucket_name=self.bucket_name)
            logger.info(f"文件下载成功: {local_path}")
            return local_path
        except Exception as e:
            logger.error(f"文件下载失败: {remote_path}, 错误: {e}")
            raise

    def upload_file_to_s3(self, local_file_path: str, relative_s3_path: str, env: str = None) -> bool:
        """
        上传文件到S3

        Args:
            local_file_path: 本地文件路径
            relative_s3_path: S3上的相对路径（包含文件名）
            env: 环境名称，如 "prod", "debug"

        Returns:
            bool: 是否上传成功
        """
        if env is None:
            env = running_env()

        # 确保路径格式正确，直接使用相对路径作为目标路径
        remote_path = f"{env}/{relative_s3_path}"

        try:
            logger.info(f"上传文件到S3: {local_file_path} -> {remote_path}")
            s3_upload_file(local_file_path, remote_path, bucket_name=self.bucket_name)
            logger.info(f"文件上传成功: {remote_path}")
            return True
        except Exception as e:
            logger.error(f"文件上传失败: {local_file_path} -> {remote_path}, 错误: {e}")
            return False

    def _clear_cache(self):
        import shutil

        if os.path.exists(self.base_cache_dir):
            shutil.rmtree(self.base_cache_dir)
            os.makedirs(self.base_cache_dir)
            logger.info(f"缓存目录已清空: {self.base_cache_dir}")


if __name__ == "__main__":
    manager = S3ResourceManager()

    config_path = manager.get_local_file_path("configs_v2.json", env="prod")
    print(f"配置文件路径: {config_path}")
    print(os.path.exists(config_path))

    config_path = manager.get_local_file_path("configs_v2.json", env="debug")
    print(f"配置文件路径: {config_path}")
    print(os.path.exists(config_path))
