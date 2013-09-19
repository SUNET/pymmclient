#!/usr/bin/env python

from pymmclient import client
from setuptools import setup, find_packages

install_requires=[
    'suds (>= 0.4.1)',
    'requests (>= 1.2.3)',
    'lxml (>= 3.0)',
    'pyXMLSecurity (>=0.10)'
]

setup(
    name='pymmclient',
    version=client.__version__,
    description='Python API for the Swedish government service "Mina Meddelanden"',
    author='Stefan Wold',
    author_email='swold@sunet.se',
    maintainer='Stefan Wold',
    license='BSD',
    url='https://github.com/SUNET/pymmclient',
    packages=find_packages(),
    package_data={
        'pymmclient': ['*.wsdl', 'schema/*.xsd', 'xslt/*.xsl']
    },
    requires=install_requires
)
