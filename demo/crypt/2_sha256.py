import hashlib
import binascii

# https://docs.python.org/3/library/hashlib.html
def get_sha256(data: bytes) -> str:
    m = hashlib.sha256()
    m.update(data)
    return binascii.hexlify(m.digest())

def get_sha256_salted(data: bytes, salt: bytes) -> str:
    m = hashlib.sha256()
    m.update(data + salt)
    # return b'$' + salt + b'$' + binascii.hexlify(m.digest())
    return b'$' + salt + b'$' + m.hexdigest().encode()


print(get_sha256(b'2b\nor\r!2b'))
print(get_sha256_salted(b'2bor!2b', b'mysalt'))
