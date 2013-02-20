'''
Created on 18-02-2013

@author: kamil
'''
from boreas.ws import handlers

handlers = [
    ('/', handlers.GlobalFeedHandler),
]