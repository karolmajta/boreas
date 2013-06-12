'''
Created on 18-02-2013

@author: kamil
'''
import json
import uuid
import time

import tornado.websocket
from simplejson.decoder import JSONDecodeError

class GlobalFeedHandler(tornado.websocket.WebSocketHandler):
    
    def __init__(self, *args, **kwargs):
        super(GlobalFeedHandler, self).__init__(*args, **kwargs)
        self.token = None
        self.channels = set()
    
    def open(self):
        self.application.recipient_pool.register(self)
        if not self.application.require_auth:
            # elevate all clients upon connection using unique token
            random_token = u"{0}-{1}".format(str(uuid.uuid4()), int(time.time()))
            self.elevate(random_token, noauth=True)

    def on_close(self):
        self.leave(self, *list(self.channels))
        self.application.recipient_pool.unregister(self, self.token)
    
    def on_message(self, message):
        """
        Client can only send messages in format:
            
            1. {
                "access_token": '23asd...'
                }
            
            2. {
                "channels": {
                    "join":
                        ["es3ka...", "ad2...", ...],
                    "leave":
                        ["a45...", "sd334...", ...]
                    }
                }
                
        This method WILL ALWAYS FAIL SILENTLY on any exception, like:
            - when input cannot be parsed as json
            - when `access_token` key is missing
        If your client doesn't get elevated you probably should check
        if sent message is valid.
        """
        try:
            payload = json.loads(message)
        except (ValueError, JSONDecodeError):
            return
        try:
            token = str(payload['access_token'])
            if not self.application.require_auth:
                return # just ignore authentication messages when auth is disabled
            else:
                self.elevate(token)
                return
        except (ValueError, KeyError):
            pass # hackish - exceptions for flow control, but hell, its python
        if self.token is None:
            return
        try:
            channels = payload['channels']
            channels_to_join = channels.get('join', None)
            channels_to_leave = channels.get('leave', None)
            if channels_to_join is None or channels_to_leave is None: return
            if type(channels_to_join) != list: return
            if type(channels_to_leave) != list: return
            self.join(*channels_to_join)
            self.leave(*channels_to_leave)
        except (ValueError, KeyError):
            return
        
    
    def callback(self, message):
        self.write_message(message)
    
    def elevate(self, new_token, noauth=False):
        if noauth or self.application.token_pool.has(new_token):
            self.application.recipient_pool.elevate(self, self.token, new_token)
            self.token = new_token
    
    def join(self, *channels):
        self.channels.update(set(channels))
        self.application.recipient_pool.add_to_channels(self, channels)
    
    def leave(self, *channels):
        self.application.recipient_pool.remove_from_channels(self, channels)
        self.channels.difference_update(set(channels))