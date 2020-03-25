from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
# rbp https://stackoverflow.com/questions/6947988/when-to-use-pip-requirements-file-versus-install-requires-in-setup-py

setup(
    name="iospytools",
    version="1.0",
    author="Merculous",
    author_email="vycemerculous@gmail.com",
    description="provides useful tools/commands which are used in iOS research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/merculous/ios-python-tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS
)
