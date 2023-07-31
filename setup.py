from setuptools import setup

setup(
    name='horn_cleaner',
    version='1.0.0',
    py_modules=['horn_cleaner'],
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