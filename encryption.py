from dataclasses import dataclass

from Crypto.Cipher import AES

from symmetric_key import SymmetricKey


@dataclass
class RequestData:
    pass


def get_encrypted_data(symmetric_key: SymmetricKey):
    cipher = AES.new(symmetric_key.key, AES.MODE_CBC, symmetric_key.iv)
