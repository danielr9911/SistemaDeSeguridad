import sys
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS, YOWSUP_PROTOCOL_LAYERS_FULL
from yowsup.stacks import  YowStackBuilder
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.common import YowConstants
#from yowsup import env
from yowsup.env import YowsupEnv
#from yowsup.env.env import YowsupEnv
from .layer import SendMedia

class sendmediafile(object):
    def __init__(self, credentials, messages):
        layers = (SendMedia,) + (YOWSUP_PROTOCOL_LAYERS_FULL,) + YOWSUP_CORE_LAYERS

        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(True)\
            .push(SendMedia)\
            .build()

        #envi = YowsupEnv()
        ##self.stack = YowStack(layers)
        self.stack.setProp(SendMedia.PROP_MESSAGES, messages)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)
        self.stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
        self.stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        #self.stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())
        self.stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource())
        #self.stack.setProp(YowCoderLayer.PROP_RESOURCE, envi.getResource())
    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
