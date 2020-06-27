from epaycosdk.resources import Token, Customers, Bank, Cash, Charge, Subscriptions, Plan
from epaycosdk.utils.constants import Languages


class Epayco:
    public_key = ''
    api_key = ''
    test = False
    lang = Languages.SPANISH

    def __init__(self, options):
        self.api_key = options['api_key']
        self.private_key = options['private_key']
        self.test = options['test']
        self.lang = options['language']

        self.token = Token(options)
        self.customer = Customers(options)
        self.bank = Bank(options)
        self.cash = Cash(options)
        self.charge = Charge(options)
        self.plan = Plan(options)
        self.subscriptions = Subscriptions(options)
