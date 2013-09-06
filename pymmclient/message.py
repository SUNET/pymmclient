from pymmclient.client import MMClient
import pymmclient as p

# Todo: Just example code, doesn't actually do anything yet
class Message(MMClient):
    def __init__(self, cert, **kwargs):
        self.ws_endpoint = kwargs.pop('ws_endpoint', p.__ws_base_endpoint__ + 'Message')
        MMClient.__init__(self, wsdl='Message.wsdl', cert=cert, url=self.ws_endpoint, **kwargs)

    def sendSecureMessage(self):
        message = self.client.factory.create('ns3:SecureMessage')
        message.Header.Subject = 'Test'
        print message

    def sendSimpleMessage(self):
        #deliveryHeader = self.client.factory.create('ns3:DeliveryHeader')
        message = self.client.factory.create('ns3:SimpleMessage')
        #print deliveryHeader
        print message
