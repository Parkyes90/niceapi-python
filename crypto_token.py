import base64
import dataclasses
import json
import time
from dataclasses import dataclass

import dacite
import requests

from base import NICE_API_CLIENT_ID, NICE_API_IV_INTEGRATED_PRODUCT_CODE

URL = "https://svc.niceapi.co.kr:22001/digital/niceid/api/v1.0/common/crypto/token"
REQ_NO = "82f85597a3fc4fe2b884615bdb9ae1"
REQ_DTIM = "20220718084600"


@dataclass
class RequestCryptoTokenDataHeader:
    CNTY_CD: str = "ko"  # 이용 언어


@dataclass
class RequestCryptoTokenDataBody:
    req_dtim: str  # 요청 일시 length 14
    req_no: str  # 고유 번호 length 30
    enc_mode: str = "1"  # 사용할 암복호화 구분 AES128/CBC/PKCS7 사용 length 1


@dataclass
class RequestCryptoToken:
    dataHeader: RequestCryptoTokenDataHeader
    dataBody: RequestCryptoTokenDataBody


@dataclass
class CryptoTokenDataHeader:
    GW_RSLT_CD: str  # 응답 코드 1200 정상 그외 오류
    GW_RSLT_MSG: str  # 응답 메시지


@dataclass
class CryptoTokenDataBody:
    rsp_cd: str  # dataBody 정상 처리 여부 P000 성공 이외 모두 오류
    result_cd: str  # rsp_cd가 P000일 때 상세 결과 코드
    site_code: str  # 사이트 코드
    token_version_id: str  # 서버 토큰 버전
    token_val: str  # 암복호화 위한 서버 토큰 값
    period: float  # 토큰 만료까지 남은 period
    res_msg: str | None = None  # rsp_cd가 EAPI로 시작될 경우 오류 메시지


@dataclass
class CryptoToken:
    dataHeader: CryptoTokenDataHeader
    dataBody: CryptoTokenDataBody


def get_request_crypto_token_data():
    request_body = RequestCryptoTokenDataBody(req_no=REQ_NO, req_dtim=REQ_DTIM)
    request_header = RequestCryptoTokenDataHeader()
    return RequestCryptoToken(dataBody=request_body, dataHeader=request_header)


def get_crypto_token(access_token: str, request_data: RequestCryptoToken):
    timestamp = int(time.time())
    authorization_value = f"{access_token}:{timestamp}:{NICE_API_CLIENT_ID}".encode()
    base64_encoded = base64.b64encode(authorization_value).decode()
    authorization = f"bearer {base64_encoded}"
    response = requests.post(
        url=URL,
        data=json.dumps(dataclasses.asdict(request_data)),
        headers={
            "Authorization": authorization,
            "Content-type": "application/json",
            "productID": NICE_API_IV_INTEGRATED_PRODUCT_CODE,
            "client_id": NICE_API_CLIENT_ID,
        },
    )
    return dacite.from_dict(data_class=CryptoToken, data=response.json())
