from setuptools import setup, find_packages

setup(
    name="amaip",
    version="1.0.0",
    description="Python SDK for Autonomous Multi-Agent Innovation Platform",
    author="Neeraj Sachdeva",
    packages=find_packages(),
    install_requires=[
        "python-socketio[client]>=5.10.0",
        "requests>=2.31.0",
    ],
    python_requires=">=3.7",
)
