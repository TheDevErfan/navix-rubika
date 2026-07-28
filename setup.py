from setuptools import setup, find_packages

setup(
    name="navix",
    version="1.0.0.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "navix=navix.cli:main",
        ],
    },
    author="Navix Developers",
    description="Enterprise-grade async Rubika bot framework",
    python_requires=">=3.7",
)
