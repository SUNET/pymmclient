import pymmclient
from pymmclient.transport import CertAuthTransport
#from suds.xsd.sxbasic import Import
from suds.client import Client


class MMClient:
    def __init__(self, wsdl, cert, url, **kwargs):
        #for s in ('Authority', 'Consent', 'Common', 'Dispatcher', 'Message','Notification', 'Receipt', 'Recipient', 'Reply','Sender','Service'):
        #    Import.bind('http://minameddelanden.gov.se/schema/%s' % s, 'file://%s/schema/%s.xsd' % (path, s))
        transport = CertAuthTransport(cert=cert, **kwargs)
        headers = {"Content-TYpe": "text/xml;charset=UTF-8"}
        self.client = Client('file://%s/%s' % (pymmclient.get_mroot(), wsdl), location=url, transport=transport, headers=headers)
