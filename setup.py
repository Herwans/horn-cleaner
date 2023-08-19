from setuptools import setup, find_packages

setup(
    name='horn_cleaner',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        hcleaner=horn_cleaner.cli:cli
    ''',
    author="Herwans Harvel",
    description="Small tools to clean file and folder name",
    url="https://github.com/Herwans/horn_cleaner"
)