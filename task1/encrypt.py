import random

from utils import get_alphabet, read_file_to_string, write_string_to_file
from constants import INPUT_FILENAME, OUPUT_FILENAME

def encrypt(plain):
    alphabet = get_alphabet()
    key = alphabet[:]
    random.shuffle(key)
    encryption = dict(zip(alphabet, key))

    #build an encrypted string
    ciphertext = ''
    for letter in plain:
        try:
            ciphertext += encryption[letter]
        except:
            ciphertext += letter

    return ciphertext

# read the plaintext file
PLAINTEXT = read_file_to_string(INPUT_FILENAME)

# encrypt
CRYPTED_TEXT = encrypt(PLAINTEXT.lower())

print '\n encrypted text: \n', CRYPTED_TEXT
write_string_to_file(OUPUT_FILENAME, CRYPTED_TEXT)
