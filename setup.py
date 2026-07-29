from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8") if (here / "README.md").exists() else ""

setup(
    name="navix-rubika",
    version="1.0.9",
    description="A modern, fast, and modular framework for creating Rubika bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TheDevErfan",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiohttp>=3.8.0"
    ],
    entry_points={
        "console_scripts": [
            "navix=navix.cli:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
    ],
)
