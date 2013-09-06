from suds.transport.http import HttpAuthenticated
from suds.transport import Reply
import requests


class CertAuthTransport(HttpAuthenticated):
    def __init__(self, **kwargs):
        self.cert = kwargs.pop('cert', None)
        self.verify = kwargs.pop('verify', True)
        HttpAuthenticated.__init__(self, **kwargs)

    def send(self, request):
        self.addcredentials(request)
        response = requests.post(request.url, data=request.message, headers=request.headers, cert=self.cert, verify=self.verify)
        result = Reply(response.status_code, response.headers, response.content)

        return result
