from pymmclient.client import MMClient
import pymmclient as p


class Recipient(MMClient):
    def __init__(self, cert, key_file, use_cache=True, ws_endpoint=p.__ws_base_endpoint__ + 'Recipient', **kwargs):
        """
        @param cert: Path to authentication client certificate in PEM format
        @type cert: str
        @param key_file: Path to key file in PEM format
        @type key_file: str
        @param use_cache: Enable/Disable XSD caching in python-suds
        @type use_cache: bool
        @param ws_endpoint: The webservice URL
        @type ws_endpoint: str
        """
        MMClient.__init__(self, wsdl='Recipient.wsdl', cert=(cert, key_file), url=ws_endpoint, use_cache=use_cache, **kwargs)

    def is_reachable(self, sender_org_nr, identifier):
        """
        Check if the recipient is registered. Returns information about the recipient and the recipients service
        provider.

        @param sender_org_nr: Sender organisation number
        @type sender_org_nr: int
        @param identifier: The recipients social security number
        @type identifier: int
        """
        return self.client.service.isReachable(sender_org_nr, identifier)
