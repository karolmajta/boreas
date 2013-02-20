'''
Created on 19-02-2013

@author: karol
'''
import tornado.web

class RecipientDumpHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.set_header('Content-Type', 'text-plain')
        text = unicode(self.application.recipient_pool)
        self.write(text)

class TokenDumpHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.set_header('Content-Type', 'text-plain')
        for token in self.application.token_pool.tokens:
            self.write(token + "\n")
    