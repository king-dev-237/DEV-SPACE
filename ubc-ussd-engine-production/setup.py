from setuptools import setup, find_packages

setup(
    name="ubc-ussd-engine",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "fastapi",
        "uvicorn",
        # Add other dependencies here
        "pydantic",
        "jinja2",
        "python-dotenv",
        "pytest",
        "pytest-asyncio",
        "httpx",
    ],
)