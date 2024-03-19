import json, os
from Crypto.Cipher import AES as CryptoAES
from Crypto.Util.Padding import pad
from base64 import b64encode
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'sb.env'))

"""
AES is life
"""

class AES:
    def __init__(self, response):
        self.response = response
        self.encrypted_data = self.encrypt_response()

    def encrypt_response(self):
        key = os.getenv('SECRET_KEY').encode()
        cipher = CryptoAES.new(key, CryptoAES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(self.response.encode(), CryptoAES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        encrypted_dict = {'iv':iv, 'data':ct}
        return encrypted_dict

    @staticmethod
    def to_json(data):
        return json.dumps(data, ensure_ascii=False)

    def __str__(self):
        return AES.to_json(self.encrypted_data)
