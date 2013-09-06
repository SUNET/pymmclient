from pymmclient.client import MMClient
import pymmclient as p


class Recipient(MMClient):
    def __init__(self, cert, **kwargs):
        self.ws_endpoint = kwargs.pop('ws_endpoint', p.__ws_base_endpoint__ + 'Recipient')
        MMClient.__init__(self, wsdl='Recipient.wsdl', cert=cert, url=self.ws_endpoint, **kwargs)

    def isRegistered(self, identifier):
        return self.client.service.isRegistered(identifier)
