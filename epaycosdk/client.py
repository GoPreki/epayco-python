import base64
import json
import requests
from functools import wraps
from epaycosdk.crypto import AESCipher
from epaycosdk.utils.errors import EpaycoException


BASE_URL = 'https://api.secure.payco.co'
SECURE_URL = 'https://secure.payco.co'
IV = AESCipher.generate_ascii_iv()
LANGUAGE = 'python'
SWITCH = False

common_headers = {
    'Content-Type': 'application/json',
    # 'Accept': 'application/json',
    'type': 'sdk-jwt',
}


class Client:

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.api_key = config['api_key']
        self.private_key = config['private_key']
        self.test = config['test']
        self.language = config['language']
        self.auth_token = None

    def _is_test(self):
        return 'TRUE' if self.test else 'FALSE'

    def _get_headers(self):
        if self.auth_token is None:
            raise Exception('Must authenticate request first')

        return {
            **common_headers,
            # 'lang': LANGUAGE,
            'Authorization': f'Bearer {self.auth_token}'
        }

    def _auth(self):
        headers = {
            **common_headers,
            'Accept': 'application/json'
        }
        url = f'{BASE_URL}/v1/auth/login'
        send_data = {
            'public_key': self.api_key,
            'private_key': self.private_key
        }

        print(send_data, headers)

        response = requests.post(url=url, headers=headers, data=json.dumps(send_data))
        data = response.json()
        print(data)
        if data['status']:
            self.auth_token = data['bearer_token']
        else:
            error = data.get('message', json.dumps(data))
            raise Exception(f'ePayco: Could not authenticate. {error}')

    def post(self, url, data, encrypted=True, base_url=BASE_URL, with_payload=True, req_auth=True):
        payload = {
            'public_key': self.api_key,
            'i': base64.b64encode(IV.encode('ascii')).decode('utf8'),
            'lenguaje': LANGUAGE,
            'p': ''
        }
        encrypted_payload = {
            'enpruebas': self._is_test()
        }
        if encrypted:
            aes = AESCipher(self.private_key, IV)
            encrypted_data = aes.encrypt_dict(data)
            encrypted_payload = aes.encrypt_dict(encrypted_payload)

            payload = {**encrypted_data, **payload, **encrypted_payload}
        else:
            if with_payload:
                payload = {**payload, **encrypted_payload, **data}
            else:
                payload = {**data}

        auth_req = None
        if not req_auth:
            payload['test'] = self.test
        else:
            auth_req = (self.api_key, '')

        f_url = f'{base_url}/{url}'
        return requests.post(f_url, json=payload, headers=self._get_headers(), auth=auth_req)

    def get(self, url, data=None, encrypted=True, base_url=BASE_URL):
        kwargs = {}
        if base_url is not BASE_URL:
            kwargs['auth'] = (self.api_key, '')

        return requests.get(f'{base_url}/{url}', params=data, headers=self._get_headers(), **kwargs)

    @staticmethod
    def auth_request(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client = args[0].client
            client._auth()
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def catch_error(message):
        def fun_wrapper(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                client = args[0].client
                response = func(*args, **kwargs)

                if (response.status_code >= 200 and response.status_code <= 206):
                    return response.json()
                else:
                    error_map = {
                        400: 103,
                        401: 104,
                        403: 106,
                        404: 105,
                        405: 107,
                    }

                    error_code = error_map.get(response.status_code, None)
                    if error_code is not None:
                        raise EpaycoException(client.language, 103)
                    try:
                        raise EpaycoException(client.language, 102)
                    except EpaycoException:
                        raise Exception(message)

            return wrapper
        return fun_wrapper
