# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ""

setup(
    long_description=readme,
    name="chess-blunders",
    version="0.1.0",
    description="Review the mistakes from your own games.",
    python_requires="==3.*,>=3.7.0",
    author="Ludovic Tiako",
    author_email="ludovic.tiako@gmail.com",
    license="MIT",
    packages=["chess_blunders", "chess_blunders.api", "chess_blunders.api.routers"],
    package_dir={"": "."},
    package_data={},
    install_requires=[
        "chess==1.*,>=1.4.0",
        "fastapi==0.*,>=0.63.0",
        "httpx==0.*,>=0.16.1",
        "requests==2.*,>=2.25.1",
        "uvicorn[standard]==0.*,>=0.13.3",
    ],
    extras_require={
        "dev": [
            "awscli==1.*,>=1.19.6",
            "black==20.*,>=20.8.0.b1",
            "dephell==0.*,>=0.8.3",
            "mypy==0.*,>=0.800.0",
            "pre-commit==2.*,>=2.9.3",
            "pytest==6.*,>=6.2.2",
            "pytest-asyncio==0.*,>=0.14.0",
            "pytest-cov==2.*,>=2.11.1",
            "pytest-rerunfailures==9.*,>=9.1.1",
            "requests-futures==1.*,>=1.0.0",
            "requests-mock==1.*,>=1.8.0",
            "snapshottest==0.*,>=0.6.0",
        ]
    },
)
