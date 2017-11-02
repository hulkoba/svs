import random, re, string, collections, operator
from pprint import pprint


from utils import *
from constants import LETTER_FREQUENCY, OUPUT_FILENAME


def createDict(cipher):
    textFrequency = get_letter_frequency(cipher)
    frequencyKeys = get_keys(textFrequency)
    #myFrequency =            [' ','e','t','a','o','h','i','s','n','l','r','d','u','f','m','c','g','w','y','b','p','v','k','x','z','q','j']
    decryption = dict(zip(frequencyKeys, LETTER_FREQUENCY))
    #decryption = dict(zip(frequencyKeys, myFrequency))
    return decryption


def decrypt(cipher, dictionary):
  plaintext = ''

  pprint(dictionary)
  for letter in cipher:
    try:
      # if dictionary[letter] == 'h':
      #   keyToSwap = dictionary.keys()[dictionary.values().index('n')]
      #   dictionary[keyToSwap] = 'h'
      #   dictionary[letter] = 'n'

      # elif dictionary[letter] == 'i':
      #   keyToSwap = dictionary.keys()[dictionary.values().index('h')]
      #   dictionary[keyToSwap] = 'i'
      #   dictionary[letter] = 'h'
      # elif dictionary[letter] == 'g':
      #   keyToSwap = dictionary.keys()[dictionary.values().index('w')]
      #   dictionary[keyToSwap] = 'g'
      #   dictionary[letter] = 'w'

      plaintext += dictionary[letter]
    except:
      plaintext += "_"


  return plaintext

print '----------decrypt--------------'

# read the ciphertext
cipherText = read_file_to_string(OUPUT_FILENAME)

decryptedDict = createDict(cipherText)

easydecrypted = decrypt(cipherText, decryptedDict)
print "plaintext:", easydecrypted

write_string_to_file("decrypted-plaintext.txt", easydecrypted)
