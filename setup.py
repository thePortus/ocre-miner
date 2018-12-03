#!/usr/bin/python

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup
    from distutils.core import find_packages

config = {
    'name': 'ocre-miner',
    'author': 'David J. Thomas',
    'author_email': 'dave.a.base@gmail.com',
    'description': (
        'Wrapper for the Online Coins of the Roman Empire API'
    ),
    'version': '0.0.1',
    'LICENSE': 'MIT',
    'long_description': (
        'Wrapper for the Online Coins of the Roman Empire API'
    ),
    'url': 'https://github.com/thePortus/ocre-miner',
    'download_url': (
        'https://github.com/thePortus/'
        'ocre-miner/archive/master.zip'
    ),
    'packages': find_packages(),
    'install_requires': [
        'beautifulsoup4==4.6.3'
        'certifi==2018.10.15'
        'chardet==3.0.4'
        'idna==2.7'
        'requests==2.20.1'
        'urllib3==1.24.1'
    ],
    'keywords': [
        'digital-humanities',
        'digital-history',
        'numismatics',
        'digital-analysis',
        'text-processing',
        'text-analysis',
        'nltk',
        'nlp',
        'natural-language-processing',
        'greek',
        'latin',
    ],
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Topic :: Sociology :: History',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Natural Language :: Latin',
        'Natural Language :: Greek',
    ],
}

setup(**config)
