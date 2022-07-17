from fastapi import FastAPI

from base import (
    NICE_API_CLIENT_SECRET,
    NICE_API_IPIN_PRODUCT_CODE,
    NICE_API_IV_INTEGRATED_PRODUCT_CODE,
    NICE_API_CLIENT_ID,
)
from crypto_token import get_crypto_token, get_request_crypto_token_data
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
    oauth_token = get_oauth_token()
    print(oauth_token)
    # request_data = get_request_crypto_token_data()
    # if isinstance(oauth_token.dataBody, str):
    #     crypto_token = get_crypto_token("dummy", request_data)
    # else:
    #     crypto_token = get_crypto_token(oauth_token.dataBody.access_token, request_data)
    # symmetric_key = get_symmetric_key(request_data, crypto_token)
