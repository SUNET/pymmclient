"""
This module provides a wrapper for suds.client
"""
import pymmclient.utils
from pymmclient.transport import CertAuthTransport
from pymmclient.plugin import SerializablePlugin
from suds.client import Client
from suds.cache import ObjectCache


__version__ = '0.3dev'


class MMClient(object):
    """
    This class represents a wrapper for suds.client
    """
    def __init__(self, wsdl, cert, url, use_cache, **kwargs):
        """
        @param wsdl: Which bundled wsdl file to load
        @type wsdl: str
        @param cert: Path to certificate file and key file
        @type cert: tuple (cert, key)
        @param url: Service URL endpoint
        @type url: str
        @param use_cache: Enable or disable XSD caching in suds
        @type use_cache: bool
        @param verify: (optional) Whether to verify SSL endpoint certificate or not, default True
        @type verify: bool
        @param serializable: (optional) Return values will be returned in a serializable format instead of as a suds object
        @type serializable: bool
        @param plugins: (optional) List of suds plugins to load
        @type plugins: list of plugins
        """
        path = pymmclient.utils.get_mroot()

        if use_cache:
            cache = ObjectCache(days=1)
        else:
            cache = None

        plugins = kwargs.pop('plugins', None)
        if plugins is not None:
            self.plugins = plugins
        else:
            self.plugins = []

        # If 'True' all objects are returned as serializable and not as suds objects
        serializable = kwargs.pop('serializable', False)
        if serializable:
            # Check that plugins does not contain a serializable plugin already
            found = False
            for plugin in self.plugins:
                if isinstance(plugin, SerializablePlugin):
                    found = True
            if not found:
                serialize = SerializablePlugin()
                self.plugins.append(serialize)

        transport = CertAuthTransport(cert=cert, **kwargs)
        headers = {"Content-TYpe": "text/xml;charset=UTF-8"}
        self.client = Client('file://%s/%s' % (path, wsdl), location=url, transport=transport, headers=headers,
                             cache=cache, plugins=self.plugins)
