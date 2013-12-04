#-*- encoding: utf-8 -*-
from pymmclient.service import Service
from pymmclient.message import Message
from pymmclient.recipient import Recipient
from unittest import TestCase
import os
import pkg_resources


class TestService(TestCase):
    def setUp(self):
        data_dir = pkg_resources.resource_filename(__name__, 'data')
        self.cert = os.path.join(data_dir, 'Kommun_B.crt')
        self.key = os.path.join(data_dir, 'Kommun_B.key')
        self.org_nr = '162021003898'
        self.recipient = '192705178354'
        self.message = Message(cert='/tmp/Kommun_B.crt',
                               key_file='/tmp/Kommun_B.key',
                               sender_org_nr=self.org_nr,
                               sender_org_name='Kommun B',
                               support_text='Vänd er till X om ni har frågor angående detta meddelande',
                               verify=False,
                               use_cache=False,
                               support_phone='08-12121212',
                               support_email='info@kommun_b.se',
                               support_url='http://www.kommun_b.se')
        self.far = Recipient(cert=self.cert, key_file=self.key, sender_org_nr=self.org_nr, use_cache=False, verify=False)

    def test_deliver_secure_message(self):
        # Get service URL from FAR
        reachable = self.far.is_reachable(self.recipient)
        status = reachable[0].AccountStatus
        if status.Type == 'Secure' and status.Pending is False:
            service_address = status.ServiceSupplier.ServiceAdress
            m = self.message.create_secure_message('Test-dela-ut', 'test', 'text/plain', 'svSE')
            m.Body.Body = 'RXR0IGxpdGV0IHPDpGtlcnQgbWVkZGVsYW5kZSBmcsOlbiBNaW5hTWVkZGVsYW5kZW4h'
            signed_delivery = self.message.create_signed_delivery([self.recipient], m)
            service = Service(cert=self.cert,
                              key_file=self.key,
                              use_cache=False,
                              ws_endpoint=service_address,
                              verify=False)
            result = service.deliver_secure_message(signed_delivery)
            self.assertTrue(result.Status[0].Delivered)

