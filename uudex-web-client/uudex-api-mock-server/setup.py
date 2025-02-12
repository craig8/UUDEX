from setuptools import setup, find_packages

setup(
    name="uudex-api-mock-server",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-multipart>=0.0.5",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-asyncio>=0.15.0",
            "httpx>=0.18.0",
            "pytest-asyncio>=0.21.0",
        ]
    },
    python_requires=">=3.10",
)
