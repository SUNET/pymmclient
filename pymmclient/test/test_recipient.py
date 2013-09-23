from pymmclient.recipient import Recipient
import pkg_resources
import os
import unittest


class TestRecipient(unittest.TestCase):
    def setUp(self):
        data_dir = pkg_resources.resource_filename(__name__, 'data')
        cert = os.path.join(data_dir, 'Kommun_B.crt')
        key = os.path.join(data_dir, 'Kommun_B.key')
        self.sender_org_nr = '162021003898'
        self.recipient = '192705178354'
        self.r = Recipient(cert=cert, key_file=key, verify=False)

    def test_is_reachable(self):
        result = self.r.is_reachable(self.sender_org_nr, self.recipient)
        self.assertEquals(result[0].AccountStatus.RecipientId, self.recipient)
        self.assertEquals(result[0].AccountStatus.Type, 'Secure')

if __name__ == '__main__':
    unittest.main()
