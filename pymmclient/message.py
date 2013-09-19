from pymmclient.client import MMClient
from plugin import DSigPlugin
from uuid import uuid1
from base64 import b64encode

import pymmclient as p


class Message(MMClient):
    def __init__(self, cert, key_file, use_cache, sender_org_nr, sender_org_name, support_text, support_phone,
                 support_email, support_url, **kwargs):
        """
        @param cert: Path to authorization certificate (cert + key) in PEM format
        @type cert: str
        @param use_cache: Enable XSD caching in python-suds
        @type use_cache: bool
        @param sender_org_nr: Sender organisation number
        @type sender_org_nr: int
        @param sender_org_name: Sender organisation name
        @type sender_org_name: str
        @param ws_endpoint: (optional) override webservice URL endpoint
        @type ws_endpoint: str
        @param support_text: Support text instructing the user where to go for help
        @type support_text: basestring
        @param support_phone: Support phone number
        @type support_phone: str
        @param support_email: Support email address
        @type support_email: str
        @param support_url: Support web page URL
        @type support_url: str
        """
        self.cert = cert
        self.key_file = key_file
        self.use_cache = use_cache
        self.sender_org_nr = sender_org_nr
        self.sender_org_name = sender_org_name
        self.support_text = support_text
        self.support_phone = support_phone
        self.support_email = support_email
        self.support_url = support_url
        self.ws_endpoint = kwargs.pop('ws_endpoint', p.__ws_base_endpoint__ + 'Message')
        dsig_plugin = DSigPlugin(self.cert, self.key_file)
        MMClient.__init__(self, wsdl='Message.wsdl', cert=(cert, key_file), url=self.ws_endpoint, use_cache=use_cache,
                          plugins=[dsig_plugin], **kwargs)

    def send_secure_message(self, recipients, secure_message):
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
        print signed_delivery

        self.client.service.distributeSecure(signed_delivery)

    def create_secure_message(self, subject, message, content_type, language):
        """
        Creates a secure message object used as argument in send_secure_message()

        @return Secure Message Object
        """
        sec_message = self.client.factory.create('ns3:SecureMessage')
        sec_message.Header.Supportinfo = self._create_support_info()
        sec_message.Header.Id = uuid1()
        sec_message.Header.Subject = subject
        sec_message.Header.Language = language
        sec_message.Body.ContentType = content_type
        sec_message.Body.Body = b64encode(message)

        return sec_message

    def _create_delivery_header(self):
        header = self.client.factory.create('ns3:DeliveryHeader')
        header.Sender.Id = self.sender_org_nr
        header.Sender.Name = self.sender_org_name
        return header

    def _create_support_info(self):
        info = self.client.factory.create('ns3:SupportInfo')
        info.Text = self.support_text
        info.URL = self.support_url
        info.PhoneNumber = self.support_phone
        info.EmailAdress = self.support_email
        return info
