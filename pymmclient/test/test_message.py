#-*- encoding: utf-8 -*-
from pymmclient.message import Message
import os
import pkg_resources
import unittest
import re
import time

usleep = lambda x: time.sleep(x/1000000.0)


class TestMessage(unittest.TestCase):
    def setUp(self):
        data_dir = pkg_resources.resource_filename(__name__, 'data')
        self.cert = os.path.join(data_dir, 'Kommun_B.crt')
        self.key = os.path.join(data_dir, 'Kommun_B.key')

        self.recipient = ['192705178354']

        self.message = Message(cert=self.cert,
                               key_file=self.key,
                               verify=False,
                               use_cache=False,
                               sender_org_nr='162021003898',
                               sender_org_name='Kommun B',
                               support_text='Vänd er till X om ni har frågor angående detta meddelande',
                               support_phone='08-12121212',
                               support_email='info@kommun_b.se',
                               support_url='http://www.kommun_b.se')
        self.my_msg = self.message.create_secure_message('Test-skicka', 'test', 'text/plain', 'svSE')

    def test_create_secure_message(self):
        self.assertEquals(self.my_msg.Header.Subject, 'Test-skicka')
        self.assertEquals(self.my_msg.Header.Supportinfo.URL, 'http://www.kommun_b.se')

    def test_send_secure_message_and_check_distribution_status(self):
        result = self.message.send_secure_message(self.recipient, self.my_msg)
        self.assertTrue(re.match('^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$', result))
        status = self.message.check_distribution_status(self.message.sender_org_nr, result)
        self.assertEquals(status[0].RecipientId, self.recipient[0])
        self.assertEquals(status[0].Type, 'Digital')

        # Simple queue management to check distribution status
        count = 1
        while status[0].DeliveryStatus == 'Pending' and count <= 10:
            if count > 0:
                usleep(300)
            status = self.message.check_distribution_status(self.message.sender_org_nr, result)
            count += 1
        self.assertEquals(status[0].DeliveryStatus, 'Delivered')

    def test_send_secure_message_input_value_error(self):
        try:
            self.message.send_secure_message(self.recipient[0], self.my_msg)
        except ValueError:
            pass
        else:
            self.fail("Expected exception NOT thrown!")

if __name__ == '__main__':
    unittest.main()
