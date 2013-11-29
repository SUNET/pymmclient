from pymmclient.plugin import DSigPlugin, SerializablePlugin, apply_xslt, SealedDeliveryPlugin
from pymmclient.client import MMClient
from lxml import etree
from mock import MagicMock
import pkg_resources
import os
import cPickle
import unittest


class TestDSIGPlugin(unittest.TestCase):
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
        xml = apply_xslt(self.with_ns, 'secure_message_drop_ns.xsl')
        self.assertEquals(etree.tostring(xml, pretty_print=False), etree.tostring(self.without_ns, pretty_print=False))


class TestSealedDeliveryPlugin(unittest.TestCase):
    def setUp(self):
        data_dir = pkg_resources.resource_filename(__name__, 'data')
        cert = os.path.join(data_dir, 'Kommun_B.crt')
        key = os.path.join(data_dir, 'Kommun_B.key')
        self.seal = SealedDeliveryPlugin(cert=cert, key_file=key)
        self.unsigned_seal = etree.parse(os.path.join(data_dir, 'seal_in.xml')).getroot()
        self.signed_seal = etree.parse(os.path.join(data_dir, 'seal_out.xml')).getroot()

    def test_sending(self):
        context = MagicMock
        context.envelope = etree.tostring(self.unsigned_seal)
        self.seal.sending(context)
        self.assertEquals(context.envelope, etree.tostring(self.signed_seal))


class TestSerializablePlugin(unittest.TestCase):
    def setUp(self):
        self.serialize = SerializablePlugin()
        self.not_serializable = MMClient('Message.wsdl', '', '', False).client.factory.create('ns3:SecureMessage')

    def test_serializable(self):
        try:
            cPickle.dumps(self.not_serializable)
        except AttributeError:
            pass

        serializable = self.serialize._recursive_asdict(self.not_serializable)
        self.assertTrue(cPickle.dumps(serializable))

if __name__ == '__main__':
    unittest.main()
