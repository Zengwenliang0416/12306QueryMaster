from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "uvicorn>=0.15.0,<0.16.0",
        "pydantic>=1.8.0,<2.0.0",
        "requests>=2.26.0,<3.0.0",
        "python-dotenv>=0.19.0,<0.20.0",
        "python-multipart>=0.0.5,<0.1.0",
        "aiohttp>=3.8.0,<4.0.0",
    ],
) 