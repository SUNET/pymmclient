"""
pymmclient is a python client wrapper for the 'mina meddelanden' SOAP service.
"""

import os

__version__ = '0.2'
__authors__ = ['Stefan Wold']
__organization__ = 'SUNET'
__license__ = 'BSD'

__all__ = [
    'recipient',
    'message'
]

# Currently set to the test environment
__ws_base_endpoint__ = 'https://notarealhost.skatteverket.se/webservice/acc/'


def get_mroot():
    return os.path.abspath(os.path.dirname(__file__))

