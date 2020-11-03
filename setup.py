from setuptools import find_packages, setup

PACKAGE_NAME = "async-up-bank-api"
VERSION = "v0.1.2"
PROJECT_URL = "https://github.com/unchartedshark/async-up-bank-api"
PROJECT_AUTHOR = "Joshua Cowie-Willox & Jason Dau"
DOWNLOAD_URL = f"{PROJECT_URL}/archive/{VERSION}.zip"
PACKAGES = find_packages()

with open("README.md", "r", encoding="UTF-8") as file:
    LONG_DESCRIPTION = file.read()

if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        url=PROJECT_URL,
        download_url=DOWNLOAD_URL,
        author=PROJECT_AUTHOR,
        author_email="",
        packages=PACKAGES,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        python_requires=">=3.7",
        install_requires=["aiohttp>=3.7.2","pydantic>=1.7.2"],
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 3 - Alpha",
        ],
    )
