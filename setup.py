#!/usr/bin/env python

from setuptools import setup, find_packages
from distutils import versionpredicate

install_requires=[
    'suds >= 0.4.1',
    'requests >= 1.2.3',
    'lxml >= 3.0',
    'pyXMLSecurity == 0.11'
]

testing_extras = [
    'nose==1.2.1',
    'nosexcover==1.0.8',
    'coverage==3.6',
    'suds==0.4.1'
]

setup(
    name='pymmclient',
    version='0.6.4',
    description='Python API for the Swedish government service "Mina Meddelanden"',
    author='Stefan Wold',
    author_email='swold@sunet.se',
    maintainer='Stefan Wold',
    license='BSD',
    url='https://github.com/SUNET/pymmclient',
    packages=find_packages(exclude=['test']),
    package_data={
        'pymmclient': ['*.wsdl', 'schema/*.xsd', 'xslt/*.xsl']
    },
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras
    }
)
