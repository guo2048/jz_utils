"""
测试S3上传功能
"""

import os
import tempfile
import unittest

from jz_utils.s3_resource_manager import S3ResourceManager


class TestS3(unittest.TestCase):
    def test_s3_upload_and_download(self):
        """测试S3上传和下载功能"""
        print("=== 测试S3上传功能 ===")

        # 注意：这里需要环境变量中有有效的 AWS 凭证，或者在测试环境中已配置好
        try:
            s3_manager = S3ResourceManager()

            # 创建临时测试文件
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".txt", delete=False) as f:
                f.write("测试内容: 😀❤️🎉🔥🐶")
                temp_file = f.name

            print(f"创建临时文件: {temp_file}")

            # 测试上传
            upload_success = s3_manager.upload_file_to_s3(temp_file, "test_upload.txt")
            self.assertTrue(upload_success, "S3 文件上传失败")

            # 测试下载
            print("\n=== 测试下载功能 ===")
            local_path = s3_manager.get_local_file_path("test_upload.txt")
            print(f"下载文件路径: {local_path}")
            self.assertTrue(os.path.exists(local_path), "下载文件不存在")

            with open(local_path, "r", encoding="utf-8") as f:
                content = f.read()
                print(f"文件内容: {content}")
                self.assertEqual(content, "测试内容: 😀❤️🎉🔥🐶")

            # 清理临时文件
            os.unlink(temp_file)
        except Exception as e:
            self.fail(f"S3 测试过程中出现异常: {e}")


if __name__ == "__main__":
    unittest.main()
