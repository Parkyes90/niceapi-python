from fastapi import FastAPI

from crypto_token import get_crypto_token
from oauth_token import get_oauth_token

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    oauth_token = get_oauth_token()
    if isinstance(oauth_token.dataBody, str):
        crypto_token = get_crypto_token("dummy")
    else:
        crypto_token = get_crypto_token(oauth_token.dataBody.access_token)
    print(crypto_token)
