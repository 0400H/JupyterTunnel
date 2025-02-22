# coding:utf-8

from setuptools import setup, find_packages

setup(
    name = "jupytertunnel",
    version = "0.1.0",
    keywords = ["jupyter", "tunnel", "cloudflare"],
    description = "Enable tunnel for jupyter.",
    license = "Apache License",
    url = "https://github.com/0400H/JupyterTunnel",
    author = "0400h",
    author_email = "github@0400h.cn",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
