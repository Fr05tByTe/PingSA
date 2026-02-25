from __future__ import annotations

import base64
import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def hash_id_number(id_number: str) -> str:
    return hashlib.sha256(id_number.encode("utf-8")).hexdigest()


def encrypt_id_number(id_number: str, key_b64: str) -> str:
    key = base64.b64decode(key_b64)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, id_number.encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("utf-8")


def decrypt_id_number(token: str, key_b64: str) -> str:
    raw = base64.b64decode(token)
    nonce, ct = raw[:12], raw[12:]
    aes = AESGCM(base64.b64decode(key_b64))
    return aes.decrypt(nonce, ct, None).decode("utf-8")
