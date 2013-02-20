'''
Created on 18-02-2013

@author: kamil
'''
import random
import time

class RecipientPool(object):
    
    def __init__(self, *args, **kwargs):
        self.anonymous = set()
        self.authenticated = dict()
        self.channels = dict()
    
    def __unicode__(self):
        """
        Useful for debugging.
        """
        val = "RECEIVER POOL REPORT\n"
        val += "anonymous: {0}\n".format(len(self.anonymous)) 
        val += "authenticated:\n"
        if len(self.authenticated) == 0:
            val += "\t---\n"
        else:
            for k, v in self.authenticated.items():
                val += "\t - {0}: {1}".format(k, len(v)) + "\n"
        val += "channels:\n"
        if len(self.channels) == 0:
            val += " \t---\n"
        else:
            for channel, receivers in self.channels.items():
                val += "\t - {0}: {1}".format(channel, len(receivers)) + "\n"
        return val
    
    def register(self, receiver):
        self.anonymous.add(receiver)
    
    def unregister(self, receiver, token):
        if receiver in self.anonymous:
            self.anonymous.remove(receiver)
        if token in self.authenticated and receiver in self.authenticated[token]:
            self.authenticated[token].remove(receiver)
            # we can do cleanup here. If after removing receiver from authenticated
            # dictionary, resulting valie is an empty set, we remove whole item
            # from it.
            if len(self.authenticated[token]) == 0:
                self.authenticated.pop(token)
    
    def elevate(self, receiver, old_token, new_token):
        if receiver in self.anonymous:
            self.anonymous.remove(receiver)
        if old_token in self.authenticated and receiver in self.authenticated[old_token]:
            self.authenticated[old_token].remove(receiver)
            # again, cleanup
            if len(self.authenticated[old_token]) == 0:
                self.authenticated.pop(old_token)
        # removing done, now let's add new
        if new_token in self.authenticated:
            self.authenticated[new_token].add(receiver)
        else:
            self.authenticated[new_token] = set()
            self.authenticated[new_token].add(receiver)
    
    def add_to_channels(self, receiver, channels):
        for new_channel in channels:
            try:
                current_channel = self.channels[new_channel]
            except KeyError:
                self.channels[new_channel] = set()
                current_channel = self.channels[new_channel]
                current_channel.add(receiver)
            current_channel.add(receiver)
    
    def remove_from_channels(self, receiver, channels):
        for old_channel in channels:
            try:
                current_channel = self.channels[old_channel]
            except KeyError:
                continue # this channel does not exist so no need to remove
            current_channel.remove(receiver)
            # cleanup - if channel is empty it shall be gone
            if len(self.channels[old_channel]) == 0:
                self.channels.pop(old_channel)

class TokenPool(object):
    
    CHARS = "ABCDEFGHIJKLMNOPKQRSTUVWXYZabcdefghijklmnopkqrstuvwxyz1234567890"
    
    def __init__(self, *tokens):
        self.tokens = set(tokens)
    
    def has(self, token):
        return token in self.tokens
        
    def make(self):
        key = "".join([random.choice(TokenPool.CHARS) for _ in range(0, 128)])
        seconds = int(time.time())
        token = key + "-" + str(seconds)
        self.tokens.add(token)
        return token
    
    def delete(self, token):
        try:
            self.tokens.remove(token)
        except KeyError:
            pass