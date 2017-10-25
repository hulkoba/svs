import random, re, string, collections, operator
from pprint import pprint
from collections import defaultdict

from utils import *
from letter import Letter

englishLetterFrequency = [' ','e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']
englishLetterPercentage = {'e': 12.702,'t':9.056,'a': 8.167,'o':7.507,'i': 6.966 ,'n': 6.749,'s': 6.327,'h': 6.094,'r': 5.987,'d': 4.253,'l': 4.025,'c': 2.782,'u': 2.758,'m': 2.406,'w': 2.360,'f': 2.228,'g': 2.015,'y': 1.974,'p': 1.929,'b': 1.492,'v': 0.978,'k': 0.772,'j': 0.153,'x': 0.150,'q': 0.095,'z':0.074}
alphabet = list(string.ascii_lowercase)

# eher Ausschlusskriterien als Reihenfolge bzgl. Haeufigkeit
oneLetterWords = ['a', 'i']
twoLetterWords = ['he', 'at', 'it', 'if', 'in', 'is', 'on', 'to', 'do', 'go', 'of', 'an', 'so', 'of', 'up', 'as', 'my', 'me', 'be', 'as', 'or', 'we', 'by', 'no', 'am', 'us']
threeLetterWords = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way','who','boy','did','its', 'let', 'put', 'say','too','use']

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

lettersTotal = len(withWhitespaces.replace(' ', ''))

print "LETTERS=" , lettersTotal

freqDict = {}

frequency2 = getLetterFrequency(withWhitespaces.replace(' ', ''))

for letter, score in frequency2:
	freqDict[letter] = (score/float(lettersTotal))*100

del freqDict[' ']
print freqDict

#freqDict = dict(frequency)
print frequency2

letters = {}
for letter in alphabet:
	newLetter = Letter(letter, freqDict[letter])
	for otherLetter in englishLetterPercentage.keys():
		prob = englishLetterPercentage[otherLetter]
		#print letter, otherLetter, freqDict[letter], prob, abs(freqDict[letter] - prob)
		newLetter.set_probability(otherLetter, abs(freqDict[letter] - prob))

	newLetter.set_frequency(dict(frequency2)[letter])	
	letters[letter] = newLetter

words = list(set(withWhitespaces.split(' ')))
words.sort(key=len)
three = filter(lambda k: len(k) == 3, words)
two = filter(lambda k: len(k) == 2, words)
one = filter(lambda k: len(k) == 1, words)

#print words

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

sorted_list = sorted(data_new, key=lambda x: x.frequency, reverse=True)
print sorted_list

frequentLetters = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z']

sortedDict = {}

for letter in sorted_list:
	sortedDict[letter.letter] = letter
	print letter.to_string()

#print sortedDict

def dojob(letter, sol):
	if sol in letter.candidates.keys() and letter.solution == "_":

		solution = sol

		# check if solution violates dependencies
		print("dependencies for " + str(letter.letter) + " = " + str(sol) + " are " + str(letter.candidates[sol]))
		for dependency in letter.candidates[sol].keys():
			value = letter.candidates[sol][dependency]
			print "checking " + str(dependency) + " that should be " + str(value)
			other = sortedDict[dependency]
			hasmatch = False
			for val in value:
				print "checking if " + str(val) + " is " + other.solution + " or one of " + str(other.candidates.keys()) 
				if val == other.solution or val in other.candidates.keys():
					#print depkey
					hasmatch = True
					#print other.candidates.keys()
					#print 
			if not hasmatch:
				print "NO"
				solution = "_";

		# check if solution violates dependencies
		'''
		for otherletter in sorted_list:
			for candkey, deplist in otherletter.candidates.iteritems():
				for depkey, depvalue in deplist.iteritems():

					other = sortedDict[depkey]
					
					if depkey != other.solution and depkey not in other.candidates.keys():
						print depkey
						print "not in"
						print other.candidates.keys()
						print 
						solution = "_";
		'''
						
		if solution != "_":
			print "YES"
			letter.set_solution(solution)
			frequentLetters.remove(solution)
			dependencies = letter.candidates[solution]
			
			for otherLetter in sorted_list:
				otherLetter.remove_candidate(solution)
				otherLetter.validate_dependency(letter.letter, solution)

			for reqKey, reqVal in dependencies.iteritems():
				print reqVal
				dojob(sortedDict[reqKey], reqVal)

#for letter in sorted_list:
for letter in data_new:
	sortedprob = sorted(letter.candidatesProbability.items(), key=operator.itemgetter(1))
	print sortedprob
	
	for fq in sortedprob:
		print "do job for " + str(letter.letter) + " and " + str(fq[0]);
		#print("trying " + str(fq[0]) + " on letter " + str(letter))
		dojob(letter, fq[0])

				

#print
#print
#for x in sortedDict.values():
    #print (x.to_string())


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





