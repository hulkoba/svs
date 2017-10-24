import random, re, string, collections, operator
from pprint import pprint
from collections import defaultdict

from utils import *
from letter import Letter

englishLetterFrequency = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']
alphabet = list(string.ascii_lowercase)

# eher Ausschlusskriterien als Reihenfolge bzgl. Haeufigkeit
oneLetterWords = ['a', 'i']
twoLetterWords = ['he', 'at', 'it', 'if', 'in', 'is', 'on', 'to', 'do', 'go', 'of', 'an', 'so', 'of', 'up', 'as', 'my', 'me', 'be', 'as', 'or', 'we', 'by', 'no', 'am', 'us']
threeLetterWords = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way','who','boy','did','its', 'let', 'put', 'say','too','use']


shortWords = ['a', 'i', 'he', 'at', 'it', 'if', 'in', 'is', 'on', 'to', 'do', 'go', 'of', 'an', 'so', 'of', 'up', 'as', 'my', 'me', 'be', 'as', 'or', 'we', 'by', 'no', 'am', 'us', 'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way','who','boy','did','its', 'let', 'put', 'say','too','use']


def makewhitespace(cipher, wsLetter):
  return cipher.replace(wsLetter, englishLetterFrequency[0])


def decrypt(cipher, dictionary):
  wordText = ''

  for letter in cipher:
    try:
      wordText += dictionary[letter]
    except:
      wordText += "_"

  return wordText


cipherText = readFileToString(outputFilename)
frequency = getLetterFrequency(cipherText)

withWhitespaces = makewhitespace(cipherText, frequency[0][0])

print withWhitespaces

letters = {}

for letter in alphabet:
	letters[letter] = Letter(letter)

words = list(set(withWhitespaces.split(' ')))
words.sort(key=len)
three = filter(lambda k: len(k) == 3, words)
two = filter(lambda k: len(k) == 2, words)
one = filter(lambda k: len(k) == 1, words)

print words

def make_dependencies(words):
	for c in word:
		letters.get(c).clean_candidates()
	for match in words:
		if len(word) == len(match):
			for idx, c in enumerate(word):
				letter = letters.get(c)
				letter.add_candidate(match[idx])
				for idDep, dep in enumerate(word):
					if idDep != idx:
						letter.add_dependency(match[idx], dep, match[idDep])

for word in three:
	make_dependencies(threeLetterWords)
for word in two:
	make_dependencies(twoLetterWords)
for word in one:
	make_dependencies(oneLetterWords)


import numpy as np
data_new = np.array(letters.values()).flatten()

sorted_list = sorted(data_new, key=lambda x: len(x.candidates))

frequentLetters = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']

sortedDict = {}

for letter in sorted_list:
	sortedDict[letter.letter] = letter
	print letter.to_string()

#print sortedDict

def dojob(letter, sol):
	if sol in letter.candidates.keys() and letter.solution == "_":

		solution = "_"
		for otherletter in sorted_list:
			for candkey, deplist in otherletter.candidates.iteritems():
				for depkey, depvalue in deplist.iteritems():
					print depkey, depvalue
					other = sortedDict[depkey]
					if depkey == other.solution or depkey in other.candidates:
						solution = sol;
						letter.set_solution(solution)
		
		if solution != "_":
			frequentLetters.remove(solution)
			dependencies = letter.candidates[solution]
			
			for otherLetter in sorted_list:
				otherLetter.remove_candidates(solution)
				otherLetter.validate_dependency(letter.letter, solution)

			for reqKey, reqVal in dependencies.iteritems():
				dojob(sortedDict[reqKey], reqVal)

for letter in sorted_list:
	for fq in frequentLetters:
		dojob(letter, fq)		
				

print
print
for x in sortedDict.values():
    print (x.to_string())


transDict = {'a': "_" , 'b': "_" , 'c': "_" , 'd': "_" , 'e': "_" , 'f': "_" , 'g': "_" , 'h': "_" , 'i': "_" , 'j': "_" , 'k': "_" ,
      'l': "_" , 'm': "_" , 'n': "_" , 'o': "_" , 'p': "_" , 'q': "_" , 'r': "_" , 's': "_" , 't': "_" , 'u': "_" , 'v': "_" ,
      'w': "_" , 'x': "_" , 'y': "_" , 'z': "_", " ": " "}


for entry in sorted_list:
	transDict[entry.letter] = entry.solution;
print 
print 
print withWhitespaces
print 
print decrypt(withWhitespaces, transDict)
print 
print readFileToString(inputFilename)





