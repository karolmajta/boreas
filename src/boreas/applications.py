'''
Created on 18-02-2013

@author: kamil
'''
import tornado.web

class RecipientPoolApplication(tornado.web.Application):
    
    def __init__(self, recipient_pool, token_pool, require_auth=True, *args, **kwargs):
        super(RecipientPoolApplication, self).__init__(*args, **kwargs)
        self._recipient_pool = recipient_pool
        self._token_pool = token_pool
        self._require_auth = require_auth
    
    @property
    def recipient_pool(self):
        return self._recipient_pool
    
    @property
    def token_pool(self):
        return self._token_pool

    @property
    def require_auth(self):
        return self._require_auth