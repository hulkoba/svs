import random, re, string, collections, operator
from pprint import pprint
from collections import defaultdict

from utils import *

englishLetterFrequency = [' ','e','t','a','o','i','h','s','n','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']

myFrequency =            [' ','e','t','a','o','h','i','s','n','l','r','d','u','f','m','c','g','w','b','y','p','v','k','x','z','q','j']

def createDict(cipherText):
  textFrequency = getLetterFrequency(cipherText)
  frequencyKeys = getKeys(textFrequency)
  #myFrequency =            [' ','e','t','a','o','h','i','s','n','l','r','d','u','f','m','c','g','w','y','b','p','v','k','x','z','q','j']
  decryption = dict(zip(frequencyKeys, englishLetterFrequency))
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
cipherText = readFileToString(outputFilename)

decryptedDict = createDict(cipherText)

easydecrypted = decrypt(cipherText, decryptedDict)
print "plaintext:", easydecrypted

writeStringToFile("decrypted-plaintext.txt", easydecrypted)
