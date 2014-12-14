#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Genetic Programming "library"',
    'author': 'Aleksandr Yeganov',
    'url': 'URL to get it at.',
    'download_url': 'github something.',
    'author_email': 'ayeganov@gmail.com.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['gp'],
    'scripts': [],
    'name': 'gp'
}

setup(**config)

