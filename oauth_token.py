import base64
from dataclasses import dataclass
from json import JSONDecodeError

import dacite
import requests
import json
from base import NICE_API_CLIENT_ID, NICE_API_CLIENT_SECRET

URL = "https://svc.niceapi.co.kr:22001/digital/niceid/oauth/oauth/token"


@dataclass
class OauthTokenBody:
    access_token: str
    token_type: str
    expires_in: float
    scope: str


@dataclass
class OauthTokenHeader:
    # 1200 정상 그외 오류 코드
    GW_RSLT_CD: str
    GW_RSLT_MSG: str


@dataclass
class OAuthToken:
    dataHeader: OauthTokenHeader
    dataBody: OauthTokenBody


def get_oauth_token() -> OAuthToken:
    """기관 토큰 요청"""
    authorization_value = f"{NICE_API_CLIENT_ID}:{NICE_API_CLIENT_SECRET}".encode()
    authorization = f"Basic {base64.b64encode(authorization_value).decode()}"
    response = requests.post(
        url=URL,
        data={"grant_type": "client_credentials", "scope": "default"},
        headers={
            "Authorization": authorization,
            "Content-type": "application/x-www-form-urlencoded",
        },
    )
    try:
        json_data = response.json()
        print(OauthTokenBody(**json_data["dataBody"]))
        print(type(json_data["dataBody"]))
        token = dacite.from_dict(data_class=OAuthToken, data=response.json())
    except JSONDecodeError:
        token = dacite.from_dict(data_class=OAuthToken, data=response.json())
    return token
