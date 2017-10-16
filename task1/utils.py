import random, copy, string, sys, codecs, operator, re, collections
from pprint import pprint

inputFilename = "plaintext.txt"
outputFilename = "ciphertext.txt"

LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def getBlankCipherletterMapping():
  # Returns a dictionary value that is a blank cipherletter mapping.
  return {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': [], 'j': [], 'k': [],
      'l': [], 'm': [], 'n': [], 'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [],
      'w': [], 'x': [], 'y': [], 'z': []}

def getAlphabet():
  #abc = [chr(a+97) for a in range(26)]
  abc = list(string.ascii_lowercase)
  abc.append(' ')
  print abc
  return abc

def readFileToString(filename):
  f = open(filename, 'r')
  data = f.read().replace('\n', ' ')
  f.close()
  return data

def writeStringToFile(filename, s):
  f = open(filename, 'w')
  f.write(s)
  f.close()

def getLetterFrequency(s):
  letterFrequency = dict()
  abc = getAlphabet()
  #init all values with zero
  for c in abc:
    letterFrequency[c] = 0

  #increment the specific value to get a first overview about the letter frequency
  for c in s:
    letterFrequency[c] += 1

  # sort the frequency array
  sortedFrequency = sorted(letterFrequency.items(), key=operator.itemgetter(1))
  sortedFrequency.reverse()
  return sortedFrequency

def getKeys(freq):
  keys = []
  for i in freq:
    keys.append(i[0])

  return keys

def addLettersToMapping(letterMapping, cipherword, candidate):
  # The letterMapping = "cipherletter mapping" dictionary
  # The cipherword parameter is a string value of the ciphertext word.
  # The candidate parameter is a possible English word that the
  # cipherword could decrypt to. [the, a, one...]

  # This function adds the letters of the candidate as potential
  # decryption letters for the cipherletters in the cipherletter
  # mapping.

  letterMapping = copy.deepcopy(letterMapping)
  for i in range(len(cipherword)):
    if candidate[i] not in letterMapping[cipherword[i]]:
      letterMapping[cipherword[i]].append(candidate[i])
    return letterMapping

def intersectMappings(mapA, mapB):

  # merge dictionaries
  intersectedMapping = getBlankCipherletterMapping()
  for letter in LETTERS:

    # An empty list means "any letter is possible". In this case just
    # copy the other map entirely.
    #if mapA[letter] == [] or mapA[letter] == ' ':
     #   intersectedMapping[letter] = copy.deepcopy(mapB[letter])
    if mapB[letter] == [] or mapB[letter] == ' ':
      intersectedMapping[letter] = copy.deepcopy(mapA[letter])
    else:
      # If a letter in mapA[letter] exists in mapB[letter], add
      # that letter to intersectedMapping[letter].
      for mappedLetter in mapA[letter]:
        if mappedLetter in mapB[letter]:
          intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    # Cipher letters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    letterMapping = copy.deepcopy(letterMapping)
    loopAgain = True
    while loopAgain:
        # First assume that we will not loop again:
        loopAgain = False

        # gibt es je einen buchstaben nur 1 kandidaten
        solvedLetters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])

        # diesen kandidaten von den anderen potentiellen, mit mehreren kanditeten, buchstaben entfernen
        for cipherletter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        # A new letter is now solved, so loop again.
                        loopAgain = True
    return letterMapping
