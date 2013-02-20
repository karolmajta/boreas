'''
Created on 18-02-2013

@author: kamil
'''
import json

import tornado.web
from simplejson.decoder import JSONDecodeError

class TokensHandler(tornado.web.RequestHandler):
    
    def get(self):
        tokens = self.application.recipient_pool.authenticated.keys()
        self.write({'tokens': list(tokens)})
    
    def post(self):
        token = self.application.token_pool.make()
        self.write({'token': token})

class TokenHandler(tornado.web.RequestHandler):
    
    def delete(self, token):
        self.application.token_pool.delete()

class ChannelTokensHandler(tornado.web.RequestHandler):
    
    def get(self, channel):
        tokens = self.application.recipient_pool.channels.get(channel, [])
        print list(tokens)
        self.write({'tokens': [t.token for t in tokens]})

class ChannelMessagesHandler(tornado.web.RequestHandler):
    
    def __init__(self, *args, **kwargs):
        super(ChannelMessagesHandler, self).__init__(*args, **kwargs)
        self.json_payload = None
    
    def post(self, channel):
        is_json, error = self.prepare_json()
        if not is_json:
            self.fail_with(400, [error,])
            return
        else:
            dryrun, valid, error = self.extract_dryrun(self.json_payload)
            if not valid:
                self.fail_with(400, [error,])
                return
            message, valid, error = self.extract_message(self.json_payload)
            if not valid:
                self.fail_with(400, [error,])
                return
            
            if not dryrun:
                self.handle_message(channel, message)
            self.set_status(200)
            self.finish()
    
    def prepare_json(self):
        if self.request.headers.get("Content-Type") == "application/json":
            try:
                self.json_payload = json.loads(self.request.body)
            except (ValueError, JSONDecodeError):
                # we fail silently, if you want to know if this method
                # failed just call it and then check if `json_payload`
                # property is None, or check the return value.
                return (False, u"Could not parse payload as JSON.")
            if type(self.json_payload) != dict:
                return (False, u"Paylod must be an object.")
            else:
                return (True, None)
        else:
            return (False, u"We only accept `Content-Type` `application/json`")
    
    def extract_dryrun(self, payload):
        dryrun = payload.get('dryrun', False)
        return (dryrun, True, None)
        
    def extract_message(self, payload):
        message = payload.get('payload', None)
        if message is None:
            return ("", False, "`payload` key is required.")
        else:
            return (message, True, None)
    
    def handle_message(self, channel, message):
        # first we make message string again
        payload = json.dumps({'message': message, 'channel': channel}) # no exceptions should happen at this point
        self.notify_channel(channel, payload)
        return
    
    def notify_channel(self, channel, message):
        try:
            channel = self.application.recipient_pool.channels[channel]
        except KeyError:
            return
        for recipient in channel:
            recipient.callback(message)
    
    def fail_with(self, status_code, errors):
        self.set_status(status_code)
        self.write({'errors': errors})
        self.finish()