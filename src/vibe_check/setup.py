# filepath: /Users/harshitchoudhary/Desktop/TBH/vibe_check/src/setup.py
from setuptools import setup, find_packages

setup(
    name="vibe_check",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "vibe-check=vibe_check.__main__:main"
        ]
    },
)