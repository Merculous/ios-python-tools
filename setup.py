from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
# rbp https://stackoverflow.com/questions/6947988/when-to-use-pip-requirements-file-versus-install-requires-in-setup-py

setup(
    name="iospytools",
    version="1.0.4",
    author="Merculous",
    author_email="vycemerculous@gmail.com",
    description="provides useful tools/commands which are used in iOS research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/merculous/ios-python-tools",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "iospytools = src.__main__:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.5',
    install_requires=REQUIREMENTS
)
