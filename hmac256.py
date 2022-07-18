import base64
import hashlib
import hmac


def get_iv(hmac_key: bytes, enc_data: bytes):
    h = hmac.new(hmac_key, enc_data, hashlib.sha256)
    return base64.b64encode(h.digest()).decode()
