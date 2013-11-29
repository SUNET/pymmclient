"""
This module implements Service from "Mina meddelanden"
"""

from pymmclient.client import MMClient
from pymmclient.plugin import SealedDeliveryPlugin
from logging import getLogger
from datetime import datetime
import pymmclient as p

LOG = getLogger(__name__)


class Service(MMClient):
    """
    This class is used to deliver messages directly to a mailbox provider
    """
    def __init__(self, cert, key_file, use_cache=True, ws_endpoint=p.__ws_base_endpoint__ + 'Service', **kwargs):
        """
        @param cert: Path to authentication client certificate in PEM format
        @type cert: str
        @param key_file: Path to key file in PEM format
        @type key_file: str
        @param use_cache: Enable or disable XSD caching in suds
        @type use_cache: bool
        @param ws_endpoint: (optional) override webservice URL endpoint
        @type ws_endpoint: str
        @param verify: (optional) Whether to verify SSL endpoint certificate or not, default True
        @type verify: bool
        @param serializable: (optional) Return values will be returned in a serializable format instead of as a suds
        object
        @type serializable: bool
        """
        self.cert = cert
        self.key_file = key_file
        MMClient.__init__(self, wsdl='Service.wsdl', cert=(cert, key_file), url=ws_endpoint, use_cache=use_cache,
                          **kwargs)

    def deliver_secure_message(self, signed_delivery):
        """
        Deliver sealed and signed messages to a mailbox provider.

        @param signed_delivery: A signed delivery message
        @type: signed_delivery
        """
        # Due to issues with SUDS we create a sealed delivery dict manually
        d = datetime.utcnow()
        sealed_delivery = {}
        seal = {
            'ReceivedTime': d.strftime('%Y-%m-%d'),
            'SignaturesOK': True,
        }
        sealed_delivery['SignedDelivery'] = signed_delivery
        sealed_delivery['Seal'] = seal
        self.load_plugin(SealedDeliveryPlugin, self.cert, self.key_file)
        result = self.client.service.deliverSecure(sealed_delivery)
        self.unload_plugin(SealedDeliveryPlugin)

        return result
