import pymmclient.utils
from pymmclient.transport import CertAuthTransport
from pymmclient.plugin import SerializablePlugin
from suds.client import Client
from suds.cache import ObjectCache


__version__ = '0.3dev'


class MMClient:
    def __init__(self, wsdl, cert, url, use_cache, **kwargs):
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
