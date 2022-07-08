import base64
from dataclasses import dataclass

import dacite
import requests

APP_ID = "1234"
APP_SECRET = "1234"


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
    dataBody: str | OauthTokenBody


def get_oauth_token() -> OAuthToken:
    """기관 토큰 요청"""
    url = "https://svc.niceapi.co.kr:22001/digital/niceid/oauth/oauth/token"
    authorization = (
        f"Basic {base64.b64encode(f'{APP_ID}:{APP_SECRET}'.encode()).decode()}"
    )
    response = requests.post(
        url=url,
        data={"grant_type": "client_credentials", "scope": "default"},
        headers={
            "Authorization": authorization,
            "Content-type": "application/x-www-form-urlencoded",
        },
    )
    return dacite.from_dict(OAuthToken, response.json())
