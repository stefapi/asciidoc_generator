#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.asc", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="asciidoc-generator",
    version="1.0.0",
    author="Stéphane Apiou",
    author_email="",
    description="A script designed to generate high-quality documentation from Asciidoctor files with templating support",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/yourusername/asciidoc_generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Documentation",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    scripts=[
        "scripts/generate.sh",
        "scripts/clean_template.sh",
        "scripts/parse.py",
        "scripts/style.py",
        "scripts/template.py",
    ],
    include_package_data=True,
    package_data={
        "": ["template/*", "scripts/*", "*.asc", "*.lua"],
    },
)
