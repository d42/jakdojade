#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import random
import time
import urllib.parse
from hmac import new as hmac
import base64
from functools import partial
from hashlib import sha1
import requests
class Authorization():
    key = b'401b0ea412a8120d5fe68aa9d59ed5d0b6ab420b&'
    def __init__(self):
        self.params = {
            'oauth_consumer_key': "anonym_ALKL481602142145",
            'oauth_version': "1.0",
            'oauth_signature_method': "HMAC-SHA1",
        }
        pass

    def update_param(self, key, value):
        self.params[key] = value
    def update_params(self, dict):
        self.params.update(dict)

    def get_params(self):
        required_params = [
            'oauth_consumer_key', 'oauth_version', 'oauth_signature_method',
            'oauth_timestamp', 'oauth_nonce'
        ]

        params = [
            (param, self.params[param])
            if param in self.params else
            (param, getattr(self, 'get_{}'.format(param))())
            for param in required_params
        ]
        return params

    def get_oauth_timestamp(self):
        return str(int(time.time()))

    def get_oauth_nonce(self):
        return str(int(random.getrandbits(64)))

    def request(self, params=None):
        if not params: params = []
        return params + self.get_params()

    def set_key(self, key):
        self.key = key

    def get_signature(self, url, params, method):
        url = urllib.parse.quote(url, safe='')
        q = urllib.parse.quote
        params = [(k, q(v)) for (k, v) in params]
        params = '%26'.join(k+'%3D'+q(v) for (k, v) in params)
        message = '&'.join([method, url, params])
        message = bytes(message, encoding='utf-8')
        return base64.b64encode(
            hmac(self.key, message, sha1).digest()
        )


class RequestMachine():
    user_agent = 'android'
    def __init__(self):
        self.defaults = {
            "devId": "c55698d2-1c3c-41bb-8b8a-e611bdb7df51",
            "user-agent": "Genymotion Custom Phone 7 - 4.4.2 - API 19 - 1024x600 Android 4.4.2",
            "appV": "and_36_free",
            "locale": "en"
        }

    def update_defaults(self, dictionary):
        self.defaults.update(dictionary)

    def set_auth(self, auth):
        self.auth = auth

    def request(self, url, params):
        default_params = [(k, v) for (k, v) in self.defaults.items()]
        request_params = [(k, v) for (k, v) in params.items()]
        params = default_params + request_params
        auth_params = self.get_auth_params(url, params)
        return(self._request(url, params, auth_params))

    def authorization_header(self, auth_params):
        t = '{k}="{v}"'
        q = partial(urllib.parse.quote, safe='')
        return 'OAuth ' + ', '.join(t.format(k=k, v=q(v)) for (k, v) in auth_params)

    def get_auth_params(self, url, params, method='GET'):
        auth_params = auth.get_params()
        params = sorted(params + auth_params)
        key = self.auth.get_signature(url, params, method)
        auth_params += [('oauth_signature', key.decode('utf-8'))]
        return auth_params

    def _request(self, url, params, auth_params):
        headers = {}
        payload = {k: v for (k, v) in params}
        auth_header = self.authorization_header(auth_params)
        headers["Authorization"] = auth_header
        headers['User-Agent'] = self.user_agent
        headers['Connection'] = 'Keep-Alive'
        headers['Accept-Encoding'] = 'gzip'
        return(requests.get(url, params=payload, headers=headers))

if __name__ == '__main__':
    auth = Authorization()
    auth.update_params({
        'oauth_timestamp': "1392595377",
        'oauth_nonce': "-6650870060017922296"
    })

    url = 'http://jakdojade.pl/api/mobile/v2/routes'
    p = {
            'cid': '12000',
            'rc': '3',
            'ri': '1',
            'fc': '51.23678:22.54831',
            'fsn': 'Politechnika',
            'tc': '51.228224:22.501976',
            'time': '17.02.14 02:12',
            'ia': 'false',
            't': 'optimal',
            'aac': 'false',
            'aab': 'false',
            'aax': 'false',
            'aaz': 'false',
            'aol': 'false',
            'aro': '1',
            'alt': '2',
    }

    rm = RequestMachine()
    rm.set_auth(auth)

    derp = rm.request(url, p)
    print(derp.text)
    import ipdb; ipdb.set_trace()
