import os


def running_env() -> str:
    return os.environ.get("RUN_ENV", "prod")


def running_prod() -> bool:
    return os.environ.get("RUN_ENV", "prod") == "prod"
