#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="genius_lite",
    version="0.2.1",
    keywords=("Spider", "Web Crawler"),
    description="A Light Spider(Web Crawler) System in Python",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",

    url="https://github.com/f840415070/genius-lite",
    author="fanyibin",
    author_email="f84041507@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['requests']
)
