from setuptools import setup, find_packages


setup(
    name="snapshot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "psutil"
    ],
    entry_points={
        "console_scripts": [
            "snapshot=snapshot.snapshot:main"
        ]
    },
    author="Eduardo Martínez Piña",
    description="A simple python app that monitors the system/server in which it's executed.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
)