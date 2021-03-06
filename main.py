from fastapi import FastAPI

from base import (
    NICE_API_CLIENT_SECRET,
    NICE_API_IPIN_PRODUCT_CODE,
    NICE_API_IV_INTEGRATED_PRODUCT_CODE,
    NICE_API_CLIENT_ID,
    NICE_API_ACCESS_TOKEN,
)
from crypto_token import get_crypto_token, get_request_crypto_token_data
from encryption import get_encrypted_data
from hmac256 import get_iv
from oauth_token import get_oauth_token
from symmetric_key import get_symmetric_key

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    # oauth_token = get_oauth_token()
    request_data = get_request_crypto_token_data()
    crypto_token = get_crypto_token(NICE_API_ACCESS_TOKEN, request_data)
    symmetric_key = get_symmetric_key(request_data, crypto_token)
    encrypted_data = get_encrypted_data(symmetric_key, request_data, crypto_token)
    integrity_value = get_iv(symmetric_key.hmac_key.encode(), encrypted_data.encode())
    api_response = {
        "action": "https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb",
        "token_version_id": crypto_token.dataBody.token_version_id,
        "enc_data": encrypted_data,
        "integrity_value": integrity_value,
    }
    print(api_response)
