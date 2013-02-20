'''
Created on 18-02-2013

@author: kamil
'''
from boreas.api import handlers, debug

handlers = [
    (r'/token/', handlers.TokensHandler),
    (r'/token/([A-za-z0-9-])', handlers.TokenHandler),
    (r'/([A-Za-z0-9-]+)/token/', handlers.ChannelTokensHandler),
    (r'/broadcast/([A-Za-z0-9-]+)/', handlers.ChannelMessagesHandler),
]

debug_handlers = [
    (r'/debug/token-dump', debug.TokenDumpHandler),
    (r'/debug/recipient-dump', debug.RecipientDumpHandler),
]