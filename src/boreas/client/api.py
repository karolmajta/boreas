'''
Created on 19-02-2013

@author: karol
'''
import json

import requests

class ApiClient(object):
    
    def __init__(self, base_url):
        self.base_url = base_url
    
    def new_token(self):
        url = self.base_url + '/token/'
        resp = requests.post(url)
        dct = json.loads(resp.text)
        return dct['token']
    
    def active_tokens(self, channel=None):
        if channel is None:
            url = self.base_url + '/token/'
        else:
            url = self.base_url + '/{0}/token/'.format(channel)
        resp = requests.get(url)
        dct = json.loads(resp)
        return dct['tokens']
    
    def broadcast(self, channel, message, dryrun=False):
        data = json.dumps({'payload': message, 'dryrun': dryrun})
        url = '{0}/broadcast/{1}/'.format(self.base_url, channel)
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, data=data, headers=headers)
        if resp.status_code == 200:
            return True
        else:
            return False