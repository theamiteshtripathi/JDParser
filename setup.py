from setuptools import setup, find_packages

setup(
    name="careerforge",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv",
        "fastapi",
        "uvicorn",
        "google-auth",
        "google-api-python-client"
    ]
)
