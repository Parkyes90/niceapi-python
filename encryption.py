import dataclasses
import json
from dataclasses import dataclass

from Crypto.Cipher import AES

from crypto_token import RequestCryptoToken, CryptoToken
from symmetric_key import SymmetricKey


@dataclass
class RequestData:
    requestno: str  # 서비스 요청 고유 번호
    returnurl: str  # 인증 결과를 받을 회원사 URL
    sitecode: str  # 암호화 토큰 요청 API에 응답받은 site_code
    # 필수 아님
    # 인증수단 고정
    # (M:휴대폰인증,C:카드본인확인인증,X:인증서인증,U:공동인증서인증,F:금융인증서인증,S:PASS인증서인증)
    # authtype: str = "M"
    # mobilceco: str # 이통사 우선 선택
    # businessno: str # 사업자번호(법인인증인증에 한함)
    # popupyn: str
    # receivedata 인증 후 전달받을 데이터 세팅


def get_encrypted_data(
    symmetric_key: SymmetricKey, request_token: RequestCryptoToken, token: CryptoToken
):
    req_data = RequestData(
        requestno=request_token.dataBody.req_no,
        returnurl="http://localhost:5000/niceapi/callback",
        sitecode=token.dataBody.site_code,
    )

    json_req_data = json.dumps(dataclasses.asdict(req_data))
    cipher = AES.new(symmetric_key.key, AES.MODE_CBC, symmetric_key.iv)
