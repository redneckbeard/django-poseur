#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "django-poseur",
    version = "0.1.0",
    url = 'http://github.com/threadsafelabs/django-poseur',
    license = 'BSD',
    description = "Faker utilities for Django.",
    author = 'Jonathan Lukens',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'python-faker'],
)
