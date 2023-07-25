from setuptools import setup

setup(
    name='HornCleaner',
    version='0.1.0',
    py_modules=['horn_cleaner'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hcleaner=horn_cleaner:cli
    '''
)