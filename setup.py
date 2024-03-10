from setuptools import setup, find_packages

setup(
    name='vulcan',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'setuptools',
        'Pillow'
    ],
    entry_points='''
        [console_scripts]
        vulcan=vulcan.cli:cli
    ''',
    author="Herwans Harvel",
    description="Small tools to clean file and folder name",
    url="https://github.com/Herwans/vulcan"
)