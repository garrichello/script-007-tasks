"""Utils"""
import hashlib

EXPIRATION_DAYS = 1

def get_sha256_salted(data: str, salt: str) -> str:
    m = hashlib.sha256()
    m.update((data + salt).encode())
    return f"${salt}${m.hexdigest()}"
