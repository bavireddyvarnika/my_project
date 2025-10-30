import base64, hmac, hashlib, json, time
from django.conf import settings
import random

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def b64url_decode(s: str) -> bytes:
    pad = '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode((s + pad).encode())

def sign(data: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode(), data, hashlib.sha256).digest()
    return b64url(sig)

def now_ts() -> int:
    return int(time.time())

def make_jwt(payload: dict, ttl_seconds: int) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    iat = now_ts()
    exp = iat + ttl_seconds
    full = payload | {"iat": iat, "exp": exp, "iss": settings.JWT_ISSUER}
    header_b64 = b64url(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = b64url(json.dumps(full, separators=(",", ":")).encode())
    to_sign = f"{header_b64}.{payload_b64}".encode()
    signature_b64 = sign(to_sign, settings.SECRET_KEY)
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_jwt(token: str) -> dict | None:
    try:
        header_b64, payload_b64, sig = token.split(".")
        to_sign = f"{header_b64}.{payload_b64}".encode()
        expected = sign(to_sign, settings.SECRET_KEY)
        if not hmac.compare_digest(expected, sig):
            return None
        payload = json.loads(b64url_decode(payload_b64))
        if payload.get("iss") != settings.JWT_ISSUER:
            return None
        if payload.get("exp", 0) < now_ts():
            return None
        return payload
    except Exception:
        return None

def random_otp(n=6) -> str:
    import random
    return "".join(str(random.randint(0, 9)) for _ in range(n))

def request_otp():
    return "".join(str(random.randint(0, 9)) for _ in range(6))