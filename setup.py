#!/usr/bin/env python

import pymmclient
from setuptools import setup, find_packages

setup(
    name='pymmclient',
    version=pymmclient.__version__,
    description='Python API for the Swedish government service "Mina Meddelanden"',
    author='Stefan Wold',
    author_email='swold@sunet.se',
    maintainer='Stefan Wold',
    license='BSD',
    url='https://github.com/SUNET/pymmclient',
    packages=find_packages(),
    package_data={
        'pymmclient': ['*.wsdl','schema/*.xsd']
    }
)
