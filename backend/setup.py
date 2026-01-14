from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "sqlmodel==0.0.8",
        "uvicorn==0.24.0",
        "pydantic==1.10.13",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "asyncpg==0.29.0",
        "psycopg[binary]==3.1.18",
    ],
)