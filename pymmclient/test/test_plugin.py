from pymmclient.plugin import DSigPlugin
from lxml import etree
import pkg_resources
import os
import unittest


class TestPlugin(unittest.TestCase):
    def setUp(self):
        data_dir = pkg_resources.resource_filename(__name__, 'data')
        cert = os.path.join(data_dir, 'Kommun_B.crt')
        key = os.path.join(data_dir, 'Kommun_B.key')
        self.dsig = DSigPlugin(cert=cert, key_file=key)
        self.unsigned_xml = etree.parse(os.path.join(data_dir, 'unsigned.xml')).getroot()
        self.signed_xml = etree.parse(os.path.join(data_dir, 'signed.xml')).getroot()
        self.with_ns = etree.parse(os.path.join(data_dir, 'with_ns.xml')).getroot()
        self.without_ns = etree.parse(os.path.join(data_dir, 'without_ns.xml')).getroot()

    def test_secure_message_sign(self):
        xml = self.dsig.secure_message_sign(self.unsigned_xml)
        self.assertEquals(etree.tostring(xml, pretty_print=False), etree.tostring(self.signed_xml, pretty_print=False))

    def test_drop_namespace(self):
        xml = self.dsig.drop_ns(self.with_ns)
        self.assertEquals(etree.tostring(xml, pretty_print=False), etree.tostring(self.without_ns, pretty_print=False))
