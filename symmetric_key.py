import base64
from dataclasses import dataclass

from crypto_token import CryptoToken, RequestCryptoToken
import hashlib


@dataclass
class SymmetricKey:
    key: str  # 데이터 암호화할 대칭키 Sha256 -> base64 encoding하여 앞에서부터 16 byte
    iv: str  # 데이터 암호화할 initial vector Sha256 -> base64 encoding하여 뒤에서부터 16 byte
    hmac_key: str  # 암호화 위변조 체크용 Sha256 -> base64 encoding하여 앞에서부터 32 byte
    value: str


def get_symmetric_key(
    request_crypto_token_data: RequestCryptoToken, crypto_token: CryptoToken
):
    base = (
        f"{request_crypto_token_data.dataBody.req_dtim.strip()}"
        f"{request_crypto_token_data.dataBody.req_no.strip()}"
        f"{crypto_token.dataBody.token_val.strip()}"
    )

    digest = hashlib.sha256(base.encode()).digest()
    result = base64.b64encode(digest).decode()
    sk = SymmetricKey(
        key=result[:16],
        hmac_key=result[:32],
        iv=result[len(result) - 16 :],
        value=result,
    )

    return sk
