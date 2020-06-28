from Crypto.Cipher import AES
from Crypto.Random import random
import base64


class AESCipher:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    @staticmethod
    def generate_ascii_iv():
        ascii_range = (33, 126)
        return ''.join([chr(random.randint(*ascii_range)) for i in range(16)])

    @staticmethod
    def pad(s):
        BS = 16
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf8')

    @staticmethod
    def unpad(s):
        return s[0:-(s[-1])]

    def encrypt(self, row):
        raw = AESCipher.pad(str(row).encode('utf8'))
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.iv.encode('utf8'))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key.encode('utf8'), AES.MODE_CBC, self.iv.encode('utf8'))
        dec = cipher.decrypt(enc)
        return AESCipher.unpad(dec).decode('utf-8')

    def encrypt_dict(self, data):
        aux = {}
        for key, value in data.items():
            aux[key] = self.encrypt(value)
        return aux
