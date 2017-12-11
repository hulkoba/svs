import struct
from utils import *
from operator import xor

# used http://code.activestate.com/recipes/496737/

XTEA_DELTA = 0x9e3779b9L
MASK = 0xffffffffL

def xor_block_enc(password, iv, content, rounds):
    enc = encipher(password, content, rounds)

    print("ENC " + str(password) + " | " + str(iv) + " | " + str(content) + " = " + str(enc))

    result = sxor(enc, iv)
    print("    result = " + str(result))
    return result


def xor_block_dec(password, iv, content, rounds):
    unxor = sxor(content, iv)

    print("DEC " + str(password) + " | " + str(iv) + " | " + str(content) + " = " + str(unxor))

    result = decipher(password, unxor, rounds)

    print("    result = " + str(result))
    return result

    '''
    print("enc + " + str(type(enc)))

    binary_iv = ""
    for c in iv:
        binary_iv += getBinary(ord(c))

    binary_enc = ""
    for c in enc:
        binary_enc += getBinary(ord(c))

    result = ""
    for x,y in zip(binary_iv, binary_enc):
        xor_v = xor(int(x), int(y))
        result += str(xor_v)

    return result
    '''


# def crypt(key,data,iv='\00\00\00\00\00\00\00\00',n=32):
def crypt(password, content, iv, rounds=32, mode='CFB', enc=True):
    '''
    :param password: hashed password of length 12
    :param content: content to be encrypted
    :param iv: generated seed for the key generator of length 8
    :param rounds: number of rounds (defaults to 32)
    :return: the encrypted text
    '''

    assert (len(iv) == 8)
    assert (len(password) == 16)

    # todo switch over mode

    #content = ''.join(x.encode('hex') for x in content)

    #ord_content = map(ord, content)

    # print("content = " + str(content))
    # print("ord_content = " + str(ord_content))

    result = []
    for i in range(len(content) / 8):
        block = content[i * 8:i * 8 + 8]
        if enc:
            encoded = xor_block_enc(password, iv, block, rounds)
            result.append(encoded)
        else:
            decoded = xor_block_dec(password, iv, block, rounds)
            result.append(decoded)

        #print("key = " + str(iv))

    #res = ''.join(x.encode('hex') for x in result)
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

# encrypted = crypt("0123456789012345", "kljshfdls kjfskksf lash dk gse hliuewi7t5 437tl   Text", "ABCDEFGH")
# print("enc = " + str(encrypted))

# decrypted = crypt("0123456789012345", encrypted, "ABCDEFGH")
# print("dec = " + str(decrypted))
