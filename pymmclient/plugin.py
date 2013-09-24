from lxml import etree
from suds.plugin import MessagePlugin
from suds.sudsobject import asdict
from logging import getLogger
import pymmclient.utils
import xmlsec

log = getLogger(__name__)


class DSigPlugin(MessagePlugin):
    def __init__(self, cert, key_file):
        self.cert = cert
        self.key_file = key_file

    def sending(self, context):
        """
        Extract arg0 and apply XML Signature to the element, then insert it back into the SOAP envelope.
        """
        envelope = etree.fromstring(context.envelope)
        arg0 = envelope.xpath('//SOAP-ENV:Envelope/SOAP-ENV:Body/ns0:distributeSecure/arg0',
                              namespaces={'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
                                          'ns0': 'http://minameddelanden.gov.se/Message',
                                          'ns4': 'http://minameddelanden.gov.se/schema/Message'})
        parser = etree.XMLParser(ns_clean=True, recover=True)
        unsigned_delivery = self.drop_ns(etree.fromstring(etree.tostring(arg0[0]), parser=parser))
        log.debug("Before adding dsig signature:\n%s", etree.tostring(unsigned_delivery, pretty_print=True))
        signed_delivery = self.secure_message_sign(unsigned_delivery)
        log.debug("After adding dsig signature:\n%s", etree.tostring(signed_delivery, pretty_print=True))
        signed_delivery = self.apply_ns(signed_delivery)

        # Find distributeSecure element
        dist = envelope.xpath('//SOAP-ENV:Envelope/SOAP-ENV:Body/ns0:distributeSecure',
                              namespaces={'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
                                          'ns0': 'http://minameddelanden.gov.se/Message',
                                          'ns4': 'http://minameddelanden.gov.se/schema/Message'})

        # Find arg0 element and delete it, then we append the signed arg0 element
        xarg = dist[0].xpath('//arg0')
        dist[0].remove(xarg[0])
        dist[0].append(signed_delivery)

        context.envelope = etree.tostring(envelope, encoding='utf-8')

    def drop_ns(self, root):
        xslt_doc = etree.parse('%s/%s' % (pymmclient.utils.get_mroot(), 'xslt/drop_ns.xsl'))
        transform = etree.XSLT(xslt_doc)
        return etree.fromstring(etree.tostring(transform(root), encoding='utf-8'))

    def apply_ns(self, root):
        xslt_doc = etree.parse('%s/%s' % (pymmclient.utils.get_mroot(), 'xslt/apply_ns.xsl'))
        transform = etree.XSLT(xslt_doc)
        return etree.fromstring(etree.tostring(transform(root), encoding='utf-8'))

    def secure_message_sign(self, root):
        # Root element must be renamed before signing and then renamed back to the old value
        root.tag = 'SignedDelivery'
        unsigned_xml = self.drop_ns(root)
        unsigned_xml.attrib['xmlns']='http://minameddelanden.gov.se/schema/Message'
        xmlsec.add_enveloped_signature(unsigned_xml, pos=-1, c14n_method=xmlsec.TRANSFORM_C14N_EXCLUSIVE,
                                       transforms=[xmlsec.TRANSFORM_ENVELOPED_SIGNATURE])
        xml_signed = xmlsec.sign(unsigned_xml, self.key_file, self.cert)
        xml_signed.tag = 'arg0'
        del xml_signed.attrib['xmlns']

        return xml_signed


class SerializablePlugin(MessagePlugin):
    def unmarshalled(self, context):
        if isinstance(context.reply, list) and len(context.reply) > 0:
            reply = []
            for item in context.reply:
                reply.append(self._recursive_asdict(item))
        else:
            reply = self._recursive_asdict(context.reply)

        context.reply = reply

    def _recursive_asdict(self, d):
        """
        Convert Suds object into serializable format.
        """
        out = {}
        for k, v in asdict(d).iteritems():
            if hasattr(v, '__keylist__'):
                out[k] = self._recursive_asdict(v)
            elif isinstance(v, list):
                out[k] = []
                for item in v:
                    if hasattr(item, '__keylist__'):
                        out[k].append(self._recursive_asdict(item))
                    else:
                        out[k].append(item)
            else:
                out[k] = v
        return out
