from setuptools import find_packages, setup

with open('README.md') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    dependencies = f.readlines()

setup(
    name='iospytools',
    version='1.0.7',
    author='Merculous',
    author_email='24739823+Merculous@users.noreply.github.com',
    description='provides useful tools/commands which are used in iOS research',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/merculous/ios-python-tools',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    python_requires='>=3.9',
    install_requires=dependencies
)
