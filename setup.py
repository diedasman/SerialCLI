#!/usr/bin/env python3
# setup.py
# Installation script for SerialCLI package.
# Allows users to install SerialCLI globally using: pip install -e .

from setuptools import setup, find_packages
from pathlib import Path

# Read README if available
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    with open(readme_file, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name="SerialCLI",
    version="0.1.0",
    description="A command-line interface for serial device communication via USB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Developer",
    author_email="dev@example.com",
    url="https://github.com/yourusername/SerialCLI",
    license="MIT",
    
    # Package discovery
    packages=find_packages(where="."),
    py_modules=["cli", "serial_core", "dev", "__main__"],
    
    # Entry point for the 'SerialCLI' command
    entry_points={
        'console_scripts': [
            'SerialCLI=__main__:main',
        ],
    },
    
    # Dependencies
    install_requires=[
        "pyserial>=3.5",
    ],
    
    # Python version requirement
    python_requires=">=3.7",
    
    # Include additional files
    package_data={
        '': ['logo.txt', 'config.json', 'dev.json'],
    },
    include_package_data=True,
    
    # Metadata
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Communications",
    ],
    keywords="serial communication USB CLI device",
)
