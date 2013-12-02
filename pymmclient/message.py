"""
This module implements Message from "Mina meddelanden"
"""

from pymmclient.client import MMClient
from pymmclient.plugin import DSigPlugin
from uuid import uuid1
from base64 import b64encode
from logging import getLogger
import pymmclient as p

LOG = getLogger(__name__)


class Message(MMClient):
    """
    This class is used to send secure messages through "Mina meddelanden"
    """
    def __init__(self, cert, key_file, sender_org_nr, sender_org_name, support_text, use_cache=True, support_phone=None,
                 support_email=None, support_url=None, ws_endpoint=p.__ws_base_endpoint__ + 'Message', **kwargs):
        """
        @param cert: Path to authentication client certificate in PEM format
        @type cert: str
        @param key_file: Path to key file in PEM format
        @type key_file: str
        @param sender_org_nr: Sender organisation number
        @type sender_org_nr: int
        @param sender_org_name: Sender organisation name
        @type sender_org_name: str
        @param support_text: Support text instructing the user where to go for help
        @type support_text: str
        @param use_cache: (optional) Enable XSD caching in python-suds
        @type use_cache: bool
        @param support_phone: (optional) Support phone number
        @type support_phone: str
        @param support_email: (optional) Support email address
        @type support_email: str
        @param support_url: (optional) Support web page URL
        @type support_url: str
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
        self.sender_org_nr = sender_org_nr
        self.sender_org_name = sender_org_name
        self.support_text = support_text.decode('utf-8')
        self.support_phone = support_phone
        self.support_email = support_email
        self.support_url = support_url
        MMClient.__init__(self, wsdl='Message.wsdl', cert=(cert, key_file), url=ws_endpoint, use_cache=use_cache,
                          **kwargs)

    def send_secure_message(self, recipients, secure_message):
        """
        Send a secure message to a list of recipients.

        @param recipients: A list of social security numbers
        @type recipients: list of int
        @param
        """
        # Load suds DSIG plugin
        self.load_plugin(DSigPlugin, self.cert, self.key_file)
        secure_delivery = self.client.factory.create('ns3:SecureDelivery')
        header = self._create_delivery_header()

        if isinstance(recipients, list):
            header.Recipient = recipients
        else:
            raise ValueError('Invalid argument type: recipients needs to be a list')

        secure_message.Header.Reply = "NOT_ALLOWED"
        secure_delivery.Header = header
        secure_message.Header.ReceiptRequest = "NOT"
        secure_delivery.Message.append(secure_message)
        signed_delivery = self.client.factory.create('ns3:SignedDelivery')
        signed_delivery.Delivery = secure_delivery

        result = self.client.service.distributeSecure(signed_delivery)

        # Unload DSIG plugin
        self.unload_plugin(DSigPlugin)

        return result

    def create_secure_message(self, subject, message, content_type, language):
        """
        Creates a secure message object used as argument in send_secure_message()

        @param subject: Message subject (utf-8)
        @type subject: unicode
        @param message: The body of the secure message (utf-8)
        @type message: unicode
        @param content_type: Message content type (example: text/plain)
        @type content_type: str
        @param language: Message language (example: svSE)
        @type language: str
        @return Secure Message Object
        """
        sec_message = self.client.factory.create('ns3:SecureMessage')
        sec_message.Header.Supportinfo = self._create_support_info()
        sec_message.Header.Id = uuid1()
        sec_message.Header.Subject = subject.decode('utf-8')
        sec_message.Header.Language = language
        sec_message.Body.ContentType = content_type
        sec_message.Body.Body = b64encode(message).decode('utf-8')

        return sec_message

    def create_signed_delivery(self, recipients, secure_message):
        secure_delivery = self.client.factory.create('ns3:SecureDelivery')
        header = self._create_delivery_header()

        if isinstance(recipients, list):
            header.Recipient = recipients
        else:
            raise ValueError('Invalid argument type: recipients needs to be a list')

        secure_message.Header.Reply = "NOT_ALLOWED"
        secure_delivery.Header = header
        secure_message.Header.ReceiptRequest = "NOT"
        secure_delivery.Message.append(secure_message)
        signed_delivery = self.client.factory.create('ns3:SignedDelivery')
        signed_delivery.Delivery = secure_delivery

        return signed_delivery

    def check_distribution_status(self, sender_org_nr, transaction_id):
        """
        Check if a secure message has been successfully delivered to the recipient.

        @param sender_org_nr: The sender organisation number.
        @type sender_org_nr: int
        @param transaction_id: The transaction ID received from send_secure_message()
        @type transaction_id: str
        """
        return self.client.service.checkDistributionStatus(sender_org_nr, transaction_id)

    def _create_delivery_header(self):
        """ Create delivery header based on Message.xsd """
        header = self.client.factory.create('ns3:DeliveryHeader')
        header.Sender.Id = self.sender_org_nr
        header.Sender.Name = self.sender_org_name
        return header

    def _create_support_info(self):
        """ Create support info based on Message.xsd """
        info = self.client.factory.create('ns3:SupportInfo')
        info.Text = self.support_text
        info.URL = self.support_url
        info.PhoneNumber = self.support_phone
        info.EmailAdress = self.support_email
        return info
