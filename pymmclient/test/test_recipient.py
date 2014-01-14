from . import BaseTest
from pymmclient.recipient import Recipient
from pymmclient.plugin import SerializablePlugin
import pkg_resources
import os
import cPickle


class TestRecipient(BaseTest):
    def setUp(self):
        data_dir = pkg_resources.resource_filename(__name__, 'data')
        cert = os.path.join(data_dir, 'Kommun_B.crt')
        key = os.path.join(data_dir, 'Kommun_B.key')
        sender_org_nr = '162021003898'
        self.recipient = '192705178354'
        self.r = Recipient(cert=cert, key_file=key, sender_org_nr=sender_org_nr, verify=False,
                           ws_endpoint=self.ws_url + 'Recipient')

    def test_is_reachable(self):
        result = self.r.is_reachable(self.recipient)
        self.assertEquals(result[0].AccountStatus.RecipientId, self.recipient)
        self.assertEquals(result[0].AccountStatus.Type, 'Secure')

    def test_is_serializable(self):
        serialize = SerializablePlugin()
        self.r.client.set_options(plugins=[serialize])
        result = self.r.is_reachable(self.recipient)
        self.assertTrue(cPickle.dumps(result))
