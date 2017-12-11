import struct

# used http://code.activestate.com/recipes/496737/

XTEA_DELTA = 0x9E3779B9
MASK = 0xffffffffL


# todo MAGIC method
# https://stackoverflow.com/a/231855
def keygen(password, iv, rounds):
    while True: # todo why?
        iv = encipher(password, iv, rounds)
        for k in iv:
            yield ord(k)


# def crypt(key,data,iv='\00\00\00\00\00\00\00\00',n=32):
def crypt(password, content, iv, rounds=32, mode='CFB'):
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

    generator = keygen(password, iv, rounds)
    ord_content = map(ord, content)

    xor = []
    # every time we use generator, encipher() is called and the result is yielded
    for (x, y) in zip(ord_content, generator):
        #print("orig = " + str(x) + " / enc =" + str(y))
        xor.append(chr(x ^ y))
    return "".join(xor)


def encipher(password, block, num_rounds):
    # split in 2 32bit blocks
    v0, v1 = struct.unpack("!2L", block)
    password = struct.unpack("!4L", password)

    xtea_sum = 0
    for i in range(num_rounds):
        v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (xtea_sum + password[xtea_sum & 3]))) & MASK
        xtea_sum = (xtea_sum + XTEA_DELTA) & MASK
        v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (xtea_sum + password[xtea_sum >> 11 & 3]))) & MASK

    # combine to one block
    result = struct.pack("!2L", v0, v1)
    return result


# todo this method is not needed right now - why!?
def decipher(password, block, num_rounds):
    # split in 2 32bit blocks
    v0, v1 = struct.unpack("!2L", block)
    password = struct.unpack("!4L", password)

    xtea_sum = (XTEA_DELTA * num_rounds) & MASK
    for i in range(num_rounds):
        v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (xtea_sum + password[xtea_sum >> 11 & 3]))) & MASK
        xtea_sum = (xtea_sum - XTEA_DELTA) & MASK
        v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (xtea_sum + password[xtea_sum & 3]))) & MASK

    # combine to one block
    return struct.pack("!2L", v0, v1)


#encrypted = crypt("0123456789012345", "kljshfdls kjfskksf lash dk gse hliuewi7t5 437tl   Text", "ABCDEFGH")
#print("enc = " + str(encrypted))

#decrypted = crypt("0123456789012345", encrypted, "ABCDEFGH")
#print("dec = " + str(decrypted))
