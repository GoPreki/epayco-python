import requests

r = requests.get('https://s3-us-west-2.amazonaws.com/epayco/message_api/errors.json')
errors = r.json()


class EpaycoException(Exception):

    def __init__(self, language, code):
        '''
            Se inicializa pasando los argmentos codigo e idioma

            Args:
                idioma ([str]): 'ES' or 'EN'
                code ([type]): Exception code
        '''
        self.code = code
        self.language = language
        self.message = f'{language}: {code}'

    def __str__(self):
        '''
            Se carga el json de la url se parsea y de devuelve el código del error de acuerdo al idioma

            Returns:
                str: Exception message
        '''
        error = errors[str(self.code)][self.language]
        return f'ErrorException: {{ {error} }}\n'
