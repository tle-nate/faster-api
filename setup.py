from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tle-faster-api",
    version="0.2.3",
    description="A CLI tool for bootstrapping FastAPI projects and apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tlenate",
    license="MIT",

    url="https://github.com/tle-nate/faster-api",
    project_urls={
        "Source": "https://github.com/tle-nate/faster-api",
        "Issue Tracker": "https://github.com/tle-nate/faster-api/issues",
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    keywords="fastapi cli scaffold generator",

    packages=find_packages(include=["faster_api", "faster_api.*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "fastapi",
        "pydantic",
        "alembic",
        "passlib",
        "sqlalchemy",
        "psycopg",
        "psycopg-binary",
        "python-jose",
        "python-multipart",
        "argon2_cffi",
        "uvicorn",
        "rich",
        "python-dotenv",
        "pydantic-settings",
    ],

    entry_points={
        "console_scripts": [
            "fasterapi=faster_api.cli:main",
        ],
    }
)
