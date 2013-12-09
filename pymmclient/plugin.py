"""
This module provides suds plugins.
"""

from lxml import etree
from suds.plugin import MessagePlugin
from suds.sudsobject import asdict
from logging import getLogger
import pymmclient.utils
import xmlsec
from xmlsec import constants

LOG = getLogger(__name__)


class DSigPlugin(MessagePlugin):
    """
    This class is a suds plugin providing XML DSIG for "Mina meddelanden"
    """
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
        unsigned_delivery = apply_xslt(etree.fromstring(etree.tostring(arg0[0]), parser=parser),
                                       'secure_message_drop_ns.xsl')
        LOG.debug("Before adding dsig signature:\n%s", etree.tostring(unsigned_delivery, pretty_print=True))
        signed_delivery = self.secure_message_sign(unsigned_delivery)
        LOG.debug("After adding dsig signature:\n%s", etree.tostring(signed_delivery, pretty_print=True))
        signed_delivery = apply_xslt(signed_delivery, 'secure_message_apply_ns.xsl')

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

    def secure_message_sign(self, root):
        """
        Sign the the SignedDelivery message.
        """
        # Root element must be renamed before signing and then renamed back to the old value
        root.tag = 'SignedDelivery'
        unsigned_xml = apply_xslt(root, 'secure_message_drop_ns.xsl')
        unsigned_xml.attrib['xmlns'] = 'http://minameddelanden.gov.se/schema/Message'
        xmlsec.add_enveloped_signature(unsigned_xml, pos=-1, c14n_method=constants.TRANSFORM_C14N_EXCLUSIVE,
                                       transforms=[constants.TRANSFORM_ENVELOPED_SIGNATURE])
        xml_signed = xmlsec.sign(unsigned_xml, self.key_file, self.cert)
        xml_signed.tag = 'arg0'
        del xml_signed.attrib['xmlns']

        return xml_signed


class SealedDeliveryPlugin(MessagePlugin):
    def __init__(self, cert, key_file):
        self.cert = cert
        self.key_file = key_file

    def sending(self, context):
        """
        Extract SignedDelivery and arg0 in a two step signing process and apply XML Signature to the element,
        then insert it back into the SOAP envelope.
        """
        envelope = etree.fromstring(context.envelope)
        arg0 = envelope.xpath('//SOAP-ENV:Envelope/SOAP-ENV:Body/ns4:deliverSecure/arg0/ns3:SignedDelivery',
                              namespaces={'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
                                          'ns3': 'http://minameddelanden.gov.se/schema/Message',
                                          'ns4': 'http://minameddelanden.gov.se/Service'})
        parser = etree.XMLParser(ns_clean=True, recover=True)
        unsigned_delivery = apply_xslt(etree.fromstring(etree.tostring(arg0[0]), parser=parser),
                                       'secure_message_drop_ns.xsl')
        unsigned_delivery.attrib['xmlns'] = 'http://minameddelanden.gov.se/schema/Message'
        LOG.debug("Before adding delivery dsig signature:\n%s", etree.tostring(unsigned_delivery, pretty_print=True))
        signed_delivery = self.secure_message_sign(unsigned_delivery)
        del signed_delivery.attrib['xmlns']
        LOG.debug("After adding delivery dsig signature:\n%s", etree.tostring(signed_delivery, pretty_print=True))

        # Find distributeSecure element
        dist = envelope.xpath('//SOAP-ENV:Envelope/SOAP-ENV:Body/ns4:deliverSecure/arg0',
                              namespaces={'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
                                          'ns3': 'http://minameddelanden.gov.se/schema/Message',
                                          'ns4': 'http://minameddelanden.gov.se/Service'})

        # Find SignedDelivery element and delete it, then we append the signed arg0 element
        xarg = dist[0].xpath('//ns3:SignedDelivery',
                             namespaces={'ns3': 'http://minameddelanden.gov.se/schema/Message',})
        dist[0].remove(xarg[0])
        dist[0].insert(0, signed_delivery)

        # Now final signing step (phew)
        unsigned_sealed_delivery = apply_xslt(etree.fromstring(etree.tostring(dist[0]), parser=parser),
                                              'deliver_secure_drop_ns.xsl')
        unsigned_sealed_delivery = apply_xslt(unsigned_sealed_delivery, 'signature.xsl')

        LOG.debug("Before adding sealed delivery dsig signature:\n%s", etree.tostring(unsigned_sealed_delivery,
                                                                                      pretty_print=True))
        seal_signed = self.seal_delivery_sign(unsigned_sealed_delivery)
        seal_signed = apply_xslt(seal_signed, 'deliver_secure_apply_ns.xsl')
        LOG.debug("After adding sealed delivery dsig signature:\n%s", etree.tostring(seal_signed, pretty_print=True))

        dist = envelope.xpath('//SOAP-ENV:Envelope/SOAP-ENV:Body/ns4:deliverSecure',
                              namespaces={'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/',
                                          'ns3': 'http://minameddelanden.gov.se/schema/Message',
                                          'ns4': 'http://minameddelanden.gov.se/Service'})
        xarg = dist[0].xpath('//arg0')
        dist[0].remove(xarg[0])
        dist[0].append(seal_signed)

        context.envelope = etree.tostring(envelope, encoding='utf-8')

    def secure_message_sign(self, root):
        """
        Sign the SignedDelivery message.
        """
        del root.attrib['xmlns']
        unsigned_xml = apply_xslt(root, 'secure_message_drop_ns.xsl')
        unsigned_xml.attrib['xmlns'] = 'http://minameddelanden.gov.se/schema/Message'
        xmlsec.add_enveloped_signature(unsigned_xml, pos=-1, c14n_method=constants.TRANSFORM_C14N_EXCLUSIVE,
                                       transforms=[constants.TRANSFORM_ENVELOPED_SIGNATURE])
        xml_signed = xmlsec.sign(unsigned_xml, self.key_file, self.cert)

        return xml_signed

    def seal_delivery_sign(self, root):
        """
        Sign the SealedDelivery message.
        """
        root.tag = 'SealedDelivery'
        root.attrib['xmlns'] = 'http://minameddelanden.gov.se/schema/Message'
        xmlsec.add_enveloped_signature(root, pos=-1, c14n_method=constants.TRANSFORM_C14N_EXCLUSIVE,
                                       transforms=[constants.TRANSFORM_ENVELOPED_SIGNATURE,
                                                   constants.TRANSFORM_C14N_EXCLUSIVE])
        xml_signed = xmlsec.sign(root,
                                 self.key_file,
                                 self.cert,
                                 sig_path="./{http://www.w3.org/2000/09/xmldsig#}Signature")
        xml_signed.tag = 'arg0'
        del xml_signed.attrib['xmlns']
        return xml_signed


class SerializablePlugin(MessagePlugin):
    """
    This class is a suds plugin that convert all suds results into serializable format.
    """
    def unmarshalled(self, context):
        if isinstance(context.reply, list) and len(context.reply) > 0:
            LOG.debug("context.reply list size %s", len(context.reply))
            reply = []
            for item in context.reply:
                reply.append(self._recursive_asdict(item))
        elif isinstance(context.reply, dict) or isinstance(context.reply, object):
            reply = self._recursive_asdict(context.reply)
        else:
            reply = context.reply

        context.reply = reply

    def _recursive_asdict(self, suds_dict):
        """
        Convert Suds object into serializable format.
        """
        out = {}
        for key, val in asdict(suds_dict).iteritems():
            if hasattr(val, '__keylist__'):
                out[key] = self._recursive_asdict(val)
            elif isinstance(val, list):
                out[key] = []
                for item in val:
                    if hasattr(item, '__keylist__'):
                        out[key].append(self._recursive_asdict(item))
                    else:
                        out[key].append(item)
            else:
                out[key] = val
        return out


def apply_xslt(root, xslt):
    """
    Apply xslt on XML.
    """
    xslt_doc = etree.parse('%s/xslt/%s' % (pymmclient.utils.get_mroot(), xslt))
    transform = etree.XSLT(xslt_doc)
    return etree.fromstring(etree.tostring(transform(root), encoding='utf-8'))
