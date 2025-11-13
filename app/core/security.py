import base64
import hmac
import hashlib
import json
import os
import time
from typing import Tuple, Any, Dict


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _b64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def jwt_encode(payload: Dict[str, Any], secret: str, expires_in_seconds: int = 3600) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = dict(payload)
    payload.setdefault("iat", int(time.time()))
    payload.setdefault("exp", int(time.time()) + expires_in_seconds)

    header_b = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_b}.{payload_b}".encode()
    signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    token = f"{header_b}.{payload_b}.{_b64url_encode(signature)}"
    return token


def jwt_decode(token: str, secret: str) -> Dict[str, Any]:
    try:
        header_b, payload_b, signature_b = token.split(".")
        signing_input = f"{header_b}.{payload_b}".encode()
        expected_sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_sig, _b64url_decode(signature_b)):
            raise ValueError("Invalid signature")
        payload = json.loads(_b64url_decode(payload_b).decode())
        if int(time.time()) >= int(payload.get("exp", 0)):
            raise ValueError("Token expired")
        return payload
    except Exception as e:
        raise ValueError("Invalid token") from e


def hash_password(password: str, salt: bytes | None = None, iterations: int = 100_000) -> Tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return salt.hex(), dk.hex()


def verify_password(password: str, salt_hex: str, hash_hex: str, iterations: int = 100_000) -> bool:
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return hmac.compare_digest(dk.hex(), hash_hex)