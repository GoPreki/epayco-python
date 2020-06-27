from epaycosdk.client import Client, SECURE_URL


class Resource:

    def __init__(self, config):
        self.client = Client(config)


class Token(Resource):

    @Client.auth_request
    @Client.catch_error('Error creating Token')
    def create(self, card):
        url = 'v1/tokens'
        return self.client.post(url=url, data=card, encrypted=False, with_payload=False, req_auth=False)


class Customers(Resource):

    @Client.auth_request
    @Client.catch_error('Error creating Customer')
    def create(self, options=None):
        url = 'payment/v1/customer/create'
        return self.client.post(url=url, data=options, encrypted=False, with_payload=False, req_auth=False)

    @Client.auth_request
    @Client.catch_error('Error getting Customer')
    def get(self, uid):
        url = f'payment/v1/customer/{self.client.api_key}/{uid}/'
        return self.client.get(url=url)

    @Client.auth_request
    @Client.catch_error('Error listing Customers')
    def list(self):
        url = f'payment/v1/customers/{self.client.api_key}/'
        return self.client.get(url=url)

    @Client.auth_request
    @Client.catch_error('Error updating Customer')
    def update(self, uid, options):
        url = f'payment/v1/customer/edit/{self.client.api_key}/{uid}/'
        return self.client.post(url=url, data=options, encrypted=False, with_payload=False, req_auth=False)

    @Client.auth_request
    @Client.catch_error('Error deleting Customer')
    def delete(self, options):
        url = '/v1/remove/token'
        return self.client.post(url=url, data=options, encrypted=False, with_payload=False, req_auth=False)

    @Client.auth_request
    @Client.catch_error('Error setting default card for Customer')
    def set_default_card(self, options):
        url = '/payment/v1/customer/reasign/card/default'
        return self.client.post(url=url, data=options, encrypted=False, with_payload=False, req_auth=False)

    @Client.auth_request
    @Client.catch_error('Error adding Token to Customer')
    def add_token(self, options):
        url = '/v1/customer/add/token'
        return self.client.post(url=url, data=options, encrypted=False, with_payload=False, req_auth=False)


class Charge(Resource):

    @Client.auth_request
    @Client.catch_error('Error creating Charge')
    def create(self, options=None):
        url = 'payment/v1/charge/create'
        return self.client.post(url=url, data=options, encrypted=False, with_payload=False, req_auth=False)

    @Client.auth_request
    @Client.catch_error('Error getting Charge')
    def get(self, uid):
        url = 'restpagos/transaction/response.json'
        data = {'ref_payco': uid, 'public_key': self.client.api_key}
        return self.client.get(url=url, data=data, encrypted=False, base_url=SECURE_URL)


class Bank(Resource):

    @Client.auth_request
    @Client.catch_error('Error listing PSE Banks')
    def list_banks(self):
        url = 'restpagos/pse/bancos.json'
        data = {'public_key': self.client.api_key}
        return self.client.get(url=url, data=data, base_url=SECURE_URL)

    @Client.auth_request
    @Client.catch_error('Error creating PSE transaction')
    def create(self, options=None):
        url = 'restpagos/pagos/debitos.json'
        return self.client.post(url=url, data=options, base_url=SECURE_URL)

    @Client.auth_request
    @Client.catch_error('Error getting PSE transaction')
    def get(self, uid):
        url = 'restpagos/pse/transactioninfomation.json'
        data = {'transactionID': uid, 'public_key': self.client.api_key}
        return self.client.get(url=url, data=data, base_url=SECURE_URL)


class Cash(Resource):

    @Client.auth_request
    @Client.catch_error('Error creating Cash transaction')
    def create(self, method=None, options=None):
        if method not in ['efecty', 'baloto', 'gana', 'redservi', 'puntored']:
            raise Exception(f'Payment method ({method}) not allowed')

        url = f'restpagos/v2/efectivo/{method}'
        return self.client.post(url=url, data=options, encrypted=False, base_url=SECURE_URL)

    @Client.auth_request
    @Client.catch_error('Error getting Cash transaction')
    def get(self, uid):
        url = 'restpagos/transaction/response.json'
        data = {'ref_payco': uid, 'public_key': self.client.api_key}
        return self.client.get(url=url, data=data, encrypted=False, base_url=SECURE_URL)


class Subscriptions(Resource):

    @Client.auth_request
    @Client.catch_error('Error creating Subscription')
    def create(self, options=None):
        url = 'recurring/v1/subscription/create'
        return self.client.post(url=url, data=options)

    @Client.auth_request
    @Client.catch_error('Error getting Subscription')
    def get(self, uid):
        url = f'recurring/v1/subscription/{uid}/{self.client.api_key}'
        return self.client.get(url=url)

    @Client.auth_request
    @Client.catch_error('Error listing Subscriptions')
    def list(self):
        url = f'recurring/v1/subscriptions/{self.client.api_key}/'
        return self.client.get(url=url)

    @Client.auth_request
    @Client.catch_error('Error canceling Subscription')
    def cancel(self, uid=None):
        url = 'recurring/v1/subscription/cancel'
        data = {'id': uid}
        return self.client.post(url=url, data=data)

    @Client.auth_request
    @Client.catch_error('Error charging Subscription')
    def charge(self, options=None):
        url = 'payment/v1/charge/subscription/create'
        return self.client.post(url=url, data=options)


class Plan(Resource):

    @Client.auth_request
    @Client.catch_error('Error creating Plan')
    def create(self, options=None):
        url = 'recurring/v1/plan/create'
        return self.client.post(url=url, data=options)

    @Client.auth_request
    @Client.catch_error('Error getting Plan')
    def get(self, uid):
        url = f'recurring/v1/plan/{self.client.api_key}/{uid}'
        return self.client.get(url=url)

    @Client.auth_request
    @Client.catch_error('Error listing Plans')
    def list(self):
        url = f'recurring/v1/plans/{self.client.api_key}/'
        return self.client.get(url=url)

    @Client.auth_request
    @Client.catch_error('Error updating Plans')
    def update(self, uid, options=None):
        url = f'recurring/v1/plan/edit/{self.client.api_key}/{uid}/'
        return self.client.post(url=url, data=options)

    @Client.auth_request
    @Client.catch_error('Error deleting Plan')
    def delete(self, uid):
        url = f'recurring/v1/plan/remove/{self.client.api_key}/{uid}/'
        return self.client.post(url=url)
