'''
Created on 18-02-2013

@author: kamil
'''
import importlib

import tornado.httpserver
import tornado.ioloop

from boreas.applications import RecipientPoolApplication
from boreas.ws.controllers import RecipientPool, TokenPool
import boreas.api.urls
import boreas.ws.urls

def run(options):
    tp_module, tp_function = options.token_provider.split(':')
    module = importlib.import_module(tp_module)
    provider = getattr(module, tp_function)
    print "Using `{0}` to get authentication tokens...".format(options.token_provider)
    tokens = provider()
    print "Done. Loaded {0} tokens.".format(len(tokens))
    
    print "Configuring servers..."
    receiver_pool = RecipientPool()
    token_pool = TokenPool(*tokens)
    api_handlers = boreas.api.urls.handlers
    if options.debug:
        api_handlers += boreas.api.urls.debug_handlers
        print "Running in debug mode. Available debug urls are:"
        for url, _ in boreas.api.urls.debug_handlers:
            print "\t- {0}".format(url)
    api_app = RecipientPoolApplication(receiver_pool, token_pool, handlers=api_handlers)
    websocket_app = RecipientPoolApplication(receiver_pool, token_pool, handlers=boreas.ws.urls.handlers)
    api_server = tornado.httpserver.HTTPServer(api_app)
    ws_server = tornado.httpserver.HTTPServer(websocket_app)
    
    api_server.listen(options.api_port, address=options.api_host)
    print "API endpoint configured to listen on {0}:{1}".format(
        options.api_host,
        options.api_port,
    )
    ws_server.listen(options.ws_port, address=options.ws_host)
    print "WebSocket endpoint configured to listen on {0}:{1}".format(
        options.ws_host,
        options.ws_port,
    )
    
    print "Running..."
    
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    
    tornado.options.parse_command_line()
    
    
    
    