from setuptools import setup, find_packages

setup(
    name="civitas",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt",
    ],
    entry_points={
        "console_scripts": [
            "civitas = src.cli:main",
        ],
    },
)
