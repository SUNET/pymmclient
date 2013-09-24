from pymmclient.client import MMClient
from pymmclient.plugin import SerializablePlugin, MessagePlugin
from pymmclient.transport import CertAuthTransport
from suds.cache import ObjectCache, NoCache
import unittest


class TestMMClient(unittest.TestCase):
    def test_mm_client_use_cache(self):
        mmclient = MMClient('Message.wsdl', '', '', True)
        self.assertTrue(isinstance(mmclient.client.options.cache, ObjectCache))

    def test_mm_client_no_cache(self):
        mmclient = MMClient('Message.wsdl', '', '', False)
        self.assertTrue(isinstance(mmclient.client.options.cache, NoCache))

    def test_mm_client_serializable_plugin_loaded(self):
        mmclient = MMClient('Message.wsdl', '', '', False, serializable=True)
        self.assertTrue(isinstance(mmclient.client.options.plugins[0], SerializablePlugin))

    def test_mm_client_cert_auth_transport(self):
        mmclient = MMClient('Message.wsdl', '', '', False)
        self.assertTrue(isinstance(mmclient.client.options.transport, CertAuthTransport))

    def test_mm_client_multiple_plugins(self):
        mp = MessagePlugin()
        sp = SerializablePlugin()
        mmclient = MMClient('Message.wsdl', '', '', False, plugins=[mp, sp], serializable=True)
        self.assertTrue(isinstance(mmclient.client.options.plugins[0], MessagePlugin))
        self.assertTrue(isinstance(mmclient.client.options.plugins[1], SerializablePlugin))
        self.assertEquals(len(mmclient.client.options.plugins), 2)


if __name__ == '__main__':
    unittest.main()
