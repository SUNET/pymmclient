"""
This module implements Recipient from "Mina meddelanden"
"""

from pymmclient.client import MMClient
import pymmclient as p


class Recipient(MMClient):
    """
    This class is used to verify if a user exists in "Mina meddelanden"
    """
    def __init__(self, cert, key_file, sender_org_nr, use_cache=True, ws_endpoint=p.__ws_base_endpoint__ + 'Recipient', **kwargs):
        """
        @param cert: Path to authentication client certificate in PEM format
        @type cert: str
        @param key_file: Path to key file in PEM format
        @type key_file: str
        @param sender_org_nr: Sender organisation number
        @type sender_org_nr: int
        @param use_cache: (Optional) Enable/Disable XSD caching in python-suds
        @type use_cache: bool
        @param ws_endpoint: The webservice URL
        @type ws_endpoint: str
        @param verify: (optional) Whether to verify SSL endpoint certificate or not, default True
        @type verify: bool
        @param serializable: (optional) Return values will be returned in a serializable format instead of as a suds object
        @type serializable: bool
        """
        self.sender_org_nr = sender_org_nr
        MMClient.__init__(self, wsdl='Recipient.wsdl', cert=(cert, key_file), url=ws_endpoint, use_cache=use_cache, **kwargs)

    def is_reachable(self, identifier):
        """
        Check if the recipient is registered. Returns information about the recipient and the recipients service
        provider.

        @param sender_org_nr: Sender organisation number
        @type sender_org_nr: int
        @param identifier: The recipients social security number
        @type identifier: int
        """
        return self.client.service.isReachable(self.sender_org_nr, identifier)
