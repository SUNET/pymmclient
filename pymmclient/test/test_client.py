from pymmclient.client import MMClient
from pymmclient.plugin import SerializablePlugin, DSigPlugin
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
        dp = DSigPlugin('1', '2')
        sp = SerializablePlugin()
        mmclient = MMClient('Message.wsdl', '', '', False, plugins=[dp, sp], serializable=True)
        self.assertTrue(isinstance(mmclient.client.options.plugins[0], DSigPlugin))
        self.assertTrue(isinstance(mmclient.client.options.plugins[1], SerializablePlugin))
        self.assertEquals(len(mmclient.client.options.plugins), 2)

    def test_load_unload_plugins(self):
        dp = DSigPlugin('1', '2')
        sp = SerializablePlugin()
        mmclient = MMClient('Message.wsdl', '', '', False, plugins=[dp, sp], serializable=True)
        mmclient.unload_plugin(DSigPlugin)
        self.assertEquals(len(mmclient.client.options.plugins), 1)
        mmclient.load_plugin(DSigPlugin,'1', '2')
        self.assertEquals(len(mmclient.client.options.plugins), 2)
        self.assertTrue(isinstance(mmclient.client.options.plugins[0], SerializablePlugin))
        self.assertTrue(isinstance(mmclient.client.options.plugins[1], DSigPlugin))


if __name__ == '__main__':
    unittest.main()
