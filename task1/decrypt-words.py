import random, re, string, collections, operator
from pprint import pprint
from collections import defaultdict

from utils import *

englishLetterFrequency = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']

oneLetterWords = ['a', 'i']
twoLetterWords = ['he', 'at', 'it', 'if', 'in', 'is', 'on', 'to', 'do', 'go', 'of', 'an', 'so', 'of', 'up', 'as', 'my', 'me', 'be', 'as', 'or', 'we', 'by', 'no', 'am', 'us']
threeLetterWords = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way','who','boy','did','its', 'let', 'put', 'say','too','use']
matchDict = {}

def createDict(cipherText):
  textFrequency = getLetterFrequency(cipherText)
  frequencyKeys = getKeys(textFrequency)
  decryption = dict(zip(frequencyKeys, englishLetterFrequency))
  return decryption

def getWords(text, dict):
  words = ''
  keyAtSpace = dict.keys()[dict.values().index(' ')]
  for letter in text:
    if letter == keyAtSpace:
      letter = ' '
    words += letter
  dict[keyAtSpace] = dict.get(' ') # remove space values from dict
  del dict[' ']
  #pprint(dict)
  return words.split()

def decrypt3Words(cipher, dictionary, matchDict):
  plaintext = ''
  #words = getWords(cipher, dictionary)
  words = cipher.split(' ')

  for word in words:
    if len(word) == 3 and word in threeLetterWords:
      if(word[0] not in dictionary[word[0]]):
        matchDict[word[0]] = dictionary[word[0]]
        #del dictionary[word[0]]

      if(word[1] not in dictionary[word[1]]):
        matchDict[word[1]] = dictionary[word[1]]
        #del dictionary[word[1]]

      if(word[2] not in dictionary[word[2]]):
        matchDict[word[2]] = dictionary[word[2]]
        #del dictionary[word[2]]

    elif len(word) == 3 and word not in threeLetterWords:
      if word == 'tie':
        matchDict[word[0]] = dictionary[word[0]]
        matchDict[word[1]] = 'h'
        matchDict[word[2]] = dictionary[word[2]]
      elif word == 'ohe':
        matchDict[word[0]] = dictionary[word[0]]
        matchDict[word[1]] = 'n'
        matchDict[word[2]] = dictionary[word[2]]
      elif word == 'gas':
        matchDict[word[0]] = 'h'
        matchDict[word[1]] = dictionary[word[1]]
        matchDict[word[2]] = dictionary[word[2]]

    plaintext += word+' '

  return plaintext

def decrypt1Word(cipher, dictionary):
  plaintext = ''
  #words = getWords(cipher, dictionary)
  words = cipher.split(' ')

  letterCount = {}

  for word in words:
    if len(word) == 1:
      if not word in letterCount:
        letterCount[word] = 1
      else:
        letterCount[word] += 1

  newLetterCount = sorted(letterCount.items())

  for idx, letter in enumerate(newLetterCount):
    print idx, letter
    #newLetterCount.keys()[letter.idx]
    matchDict[letter[0]] = oneLetterWords[idx]

  #print matchDict
  plaintext = cipher
  print matchDict

  for rule in matchDict.items():
    #print rule
    plaintext = plaintext.replace(rule[0], rule[1].upper())

  return plaintext

def decryptHuman(cipher):
  plaintext = ''

  matchDict['i'] = 'i'
  matchDict['e'] = 'e'

  plaintext = cipher

  for rule in matchDict.items():
    #print rule
    plaintext = plaintext.replace(rule[0], rule[1].upper())

  return plaintext



def decrypt(cipher, dictionary):
  wordText = ''

  for letter in cipher:
    try:
      wordText += dictionary[letter]
    except:
      wordText += "_"

  return wordText

def decryptEnd(cipher, dictionary, matchDict):
  wordText = ''
  matchDict[' '] = dictionary[' ']

  for letter in cipher:
    if matchDict.has_key(letter):
      wordText += matchDict[letter]
    else:
      wordText += dictionary[letter]

  pprint(matchDict)
  pprint(dictionary)
  return wordText
print '----------decrypt--------------'

# read the ciphertext
cipherText = readFileToString(outputFilename)

decryptedDict = createDict(cipherText)

wordSeparatedText = decrypt(cipherText, decryptedDict)

decryptHuman = decryptHuman(wordSeparatedText)
oneWordDecrypted = decrypt1Word(decryptHuman, decryptedDict)
#threeWordDecrypted = decrypt3Words(oneWordDecrypted, decryptedDict, matchDict)
#testWordDecrypted = decryptEnd(cipherText, decryptedDict, matchDict)
#print "plaintext:", threeWordDecrypted

print 'beforetex:', wordSeparatedText
print '----------------------------------------------------------------------------'
print "plaintext:", oneWordDecrypted

writeStringToFile("decrypted-plaintext.txt", oneWordDecrypted)
