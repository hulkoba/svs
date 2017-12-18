import struct
from utils import *

# used http://code.activestate.com/recipes/496737/

XTEA_DELTA = 0x9e3779b9L
MASK = 0xffffffffL


def xor_block_enc(password, iv, content, rounds):
    enc = encipher(password, content, rounds)
    result = sxor(enc, iv)
    # print("ENC " + str(password) + " | iv = " + str(iv) + " | content = " + str(content) + " | enc = " + str(enc) + " | result = " + str(result))

    return result


def xor_block_dec(password, iv, content, rounds):
    unxor = sxor(content, iv)
    result = decipher(password, unxor, rounds)
    # print("DEC " + str(password) + " | iv = " + str(iv) + " | content = " + str(content) + " | dec = " + str(unxor) + " | result = " + str(result))

    return result


def crypt(password, content, iv, rounds=32, mode='CFB', enc=True):
    '''
    :param password: hashed password of length 12
    :param content: content to be encrypted
    :param iv: generated seed for the key generator of length 8
    :param rounds: number of rounds (defaults to 32)
    :param mode: XTEA-Mode (CFB, ...)
    :param enc: encode or decode
    :return: the encrypted text
    '''

    assert (len(iv) == 8)
    assert (len(password) == 16)

    result = []
    for i in range(len(content) / 8):
        block = content[i * 8:i * 8 + 8]
        if enc:
            iv = xor_block_enc(password, iv, block, rounds)
            result.append(iv)
        else:
            result.append(xor_block_dec(password, iv, block, rounds))
            iv = block

    return "".join(result)


def encipher(password, block, num_rounds):
    v0, v1 = struct.unpack("!2L", block)
    k = struct.unpack("!4L", password)

    sum_value = 0L

    for r in range(num_rounds):
        v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum_value + k[sum_value & 3]))) & MASK
        sum_value = (sum_value + XTEA_DELTA) & MASK
        v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum_value + k[sum_value >> 11 & 3]))) & MASK
    return struct.pack("!2L", v0, v1)


def decipher(password, block, num_rounds):
    v0, v1 = struct.unpack("!2L", block)
    k = struct.unpack("!4L", password)

    sum_value = (XTEA_DELTA * num_rounds) & MASK

    for r in range(num_rounds):
        v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum_value + k[sum_value >> 11 & 3]))) & MASK
        sum_value = (sum_value - XTEA_DELTA) & MASK
        v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum_value + k[sum_value & 3]))) & MASK
    return struct.pack("!2L", v0, v1)
