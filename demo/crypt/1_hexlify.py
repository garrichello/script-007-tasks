import binascii

# https://docs.python.org/3/library/binascii.html#binascii.hexlify
b = b'2b\nor\r!2b'
s = binascii.hexlify(b)
print(s)

# https://docs.python.org/3/library/binascii.html#binascii.unhexlify
b = binascii.unhexlify(s)
print(b)
