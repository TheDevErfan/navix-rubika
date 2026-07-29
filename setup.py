from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="navix-rubika",
    version="1.0.7",
    author="TheDevErfan",
    author_email="your_email@example.com",
    description="A modern, fast, and modular framework for creating Rubika bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheDevErfan/navix-rubika",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.7",
)
