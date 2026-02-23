import os
import subprocess

import boto3

# 创建 S3 客户端
s3_client = boto3.client("s3")

BUCKET_NAME = "recommend-2026"


def list_files_in_bucket(bucket_name, prefix=""):
    try:
        files = []
        paginator = s3_client.get_paginator("list_objects_v2")

        # Use paginator to handle large buckets
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            if "Contents" in page:
                for obj in page["Contents"]:
                    files.append(obj["Key"])
                    print(obj["Key"])
        return files

    except Exception as e:
        print(f"Error: {e}")
        return []


# 上传文件到 S3
def upload_file(file_name, s3_path, bucket_name=None):
    # s3_path应该直接作为目标路径使用
    object_name = s3_path
    bucket_name = bucket_name or BUCKET_NAME

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded to {bucket_name}/{object_name}.")
    except Exception as e:
        print(f"Error uploading file: {e}")


def upload_folder(local, s3_path, bucket_name=None):
    bucket_name = bucket_name or BUCKET_NAME
    basename = os.path.basename(local)
    s3_path = f"s3://{bucket_name}/{s3_path}"
    subprocess.run(["aws", "s3", "cp", "--recursive", local, os.path.join(s3_path, basename)])


# 下载文件从 S3
def download_file(object_name, saved_path, bucket_name=None):
    bucket_name = bucket_name or BUCKET_NAME
    os.makedirs(saved_path, exist_ok=True)
    basename = os.path.basename(object_name)
    file_name = os.path.join(saved_path, basename)
    try:
        s3_client.download_file(bucket_name, object_name, file_name)
        print(f"File '{object_name}' from '{bucket_name}' downloaded as '{file_name}'.")
    except Exception as e:
        print(f"Error downloading file {object_name}: {e}")


def download_folder(src: str, target: str, bucket_name=None):
    bucket_name = bucket_name or BUCKET_NAME
    src = src.strip().strip("/")
    os.makedirs(target, exist_ok=True)
    basename = os.path.basename(src)
    src = f"s3://{bucket_name}/{src}"
    subprocess.run(["aws", "s3", "sync", src, os.path.join(target, basename)])


# 示例用法
if __name__ == "__main__":
    # list_buckets()  # 列出所有存储桶
    # list_files_in_bucket("recommend-2025")
    # upload_file("example.txt", "test")  # 上传文件
    # download_file("test/example.txt", "./test_downloaded")  # 下载文件
    upload_folder("user_watched_like_cache", "debug")
    # download_folder("test/user_watched_history_cache/", "test_downloaded")
