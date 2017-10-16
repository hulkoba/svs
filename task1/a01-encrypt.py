import random, string, collections
from pprint import pprint

from utils import *

def encrypt(plain):
    alphabet = getAlphabet()
    #key = list(alphabet)
    key = alphabet[:]
    random.shuffle(key)
    encryption = dict(zip(alphabet, key))

    #build an encrypted string
    ciphertext = ''
    for c in plain:
        try:
          ciphertext += encryption[c]
        except:
          ciphertext += c

    return ciphertext

# read the plaintext file
plaintext = readFileToString(inputFilename)

frequency = getLetterFrequency(plaintext.lower());
print "############################"
pprint(frequency);
cryptedText = encrypt(plaintext.lower())

print '\n crypted text \n', cryptedText
writeStringToFile(outputFilename, cryptedText)
