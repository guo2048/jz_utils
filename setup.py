from setuptools import find_packages, setup

setup(
    name="jz_utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pydantic", "boto3", "pycryptodome", "pika", "apscheduler"],
    author="yy",
    description="A collection of utility modules.",
)
