"""
pymmclient is a python client wrapper for the 'mina meddelanden' SOAP service.
"""

__authors__ = ['Stefan Wold']
__organization__ = 'SUNET'
__license__ = 'BSD'

__all__ = [
    'recipient',
    'message',
    'utils'
]

# Currently set to the test environment
__ws_base_endpoint__ = 'https://notarealhost.skatteverket.se/webservice/acc/'
