from pymmclient.client import MMClient
import pymmclient as p


class Recipient(MMClient):
    """

    """
    def __init__(self, cert, key_file, use_cache=True, **kwargs):
        """

        """
        self.ws_endpoint = kwargs.pop('ws_endpoint', p.__ws_base_endpoint__ + 'Recipient')
        MMClient.__init__(self, wsdl='Recipient.wsdl', cert=(cert, key_file), url=self.ws_endpoint, use_cache=use_cache, **kwargs)

    def is_registered(self, identifier):
        """

        """
        return self.client.service.isRegistered(identifier)

    def is_reachable(self, org_nr, identifier):
        """

        """
        return self.client.service.isReachable(org_nr, identifier)
