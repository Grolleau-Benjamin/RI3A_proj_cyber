from src.aes.contants import sbox


def aes_internal(data: bytes, key: bytes) -> bytes:
    return sbox[data ^ key]


assert aes_internal(0xAB, 0xEF) == 0x1B
assert aes_internal(0x22, 0x01) == 0x26
