import random, re, string, collections, operator
from pprint import pprint
from collections import defaultdict
import numpy as np
#import enchant

from utils import *
from letter import Letter

import collections


englishLetterFrequency = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y',
                          'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']

frequentLetters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b',
                   'v', 'k', 'j', 'x', 'q', 'z']

englishLetterPercentage = {'e': 12.702, 't': 9.056, 'a': 8.167, 'o': 7.507, 'i': 6.966, 'n': 6.749, 's': 6.327,
                           'h': 6.094, 'r': 5.987, 'd': 4.253, 'l': 4.025, 'c': 2.782, 'u': 2.758, 'm': 2.406,
                           'w': 2.360, 'f': 2.228, 'g': 2.015, 'y': 1.974, 'p': 1.929, 'b': 1.492, 'v': 0.978,
                           'k': 0.772, 'j': 0.153, 'x': 0.150, 'q': 0.095, 'z': 0.074}

alphabet = list(string.ascii_lowercase)

# eher Ausschlusskriterien als Reihenfolge bzgl. Haeufigkeit
oneLetterWords = ['a', 'i']
twoLetterWords = ['he', 'at', 'it', 'if', 'in', 'is', 'on', 'to', 'do', 'go', 'of', 'an', 'so', 'of', 'up', 'as', 'my',
                  'me', 'be', 'as', 'or', 'we', 'by', 'no', 'am', 'us']
threeLetterWords = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one',
                    'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two',
                    'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'too', 'use']

def makewhitespace(cipher, ws_letter):
    return cipher.replace(ws_letter, englishLetterFrequency[0])


def decrypt(cipher, dictionary):
    word_text = ''

    for l in cipher:
        if l in dictionary:
            word_text += dictionary[l]
        else:
            word_text += "_"

    return word_text


cipherText = readFileToString(outputFilename)
frequency = getLetterFrequency(cipherText)

withWhitespaces = makewhitespace(cipherText, frequency[0][0])
print withWhitespaces

lettersTotal = len(withWhitespaces.replace(' ', ''))

print "LETTERS=", lettersTotal

freqDict = {}

frequency2 = getLetterFrequency(withWhitespaces.replace(' ', ''))

for letter, score in frequency2:
    freqDict[letter] = (score / float(lettersTotal)) * 100

del freqDict[' ']
print freqDict

# freqDict = dict(frequency)
print frequency2

letters = {}
for letter in alphabet:
    newLetter = Letter(letter, freqDict[letter])
    for otherLetter in englishLetterPercentage.keys():
        prob = englishLetterPercentage[otherLetter]
        # print letter, otherLetter, freqDict[letter], prob, abs(freqDict[letter] - prob)
        newLetter.set_probability(otherLetter, abs(freqDict[letter] - prob))

    newLetter.set_frequency(dict(frequency2)[letter])
    letters[letter] = newLetter

data_new = np.array(letters.values()).flatten()

#for entry in data_new:
    #print("Q? " + str(entry.letter))


words = list(set(withWhitespaces.split(' ')))
words.sort(key=len)
three = filter(lambda k: len(k) == 3, words)
two = filter(lambda k: len(k) == 2, words)
one = filter(lambda k: len(k) == 1, words)




def make_dependencies(eng_words, word):
    #print("making dependency for " + word + " and " + str(eng_words))
    for c in word:
        letters.get(c).clean_candidates()
    for match in eng_words:
        for idx, c in enumerate(word):
            character = letters.get(c)
            character.add_candidate(match[idx])
            for idDep, dep in enumerate(word):
                if idDep != idx:
                    character.add_dependency(match[idx], dep, match[idDep])



for w3 in three:
    make_dependencies(threeLetterWords, w3)

for w2 in two:
    make_dependencies(twoLetterWords, w2)

for w1 in one:
    make_dependencies(oneLetterWords, w1)

#print("LETTERS = " + str(letters))
for l in letters:
    #print("LETTER=" + str(l))
    cands_to_remove = []
    for cand in letters[l].candidates.keys():
        for dep in letters[l].candidates[cand].keys():
            #print "sfis " + str(list(cand)) + " = " + str(letters[l].candidates[cand][dep])
            if letters[l].candidates[cand][dep] == set(cand):
                cands_to_remove.append(cand)
                #print "HERE! " + cand
    for cand in cands_to_remove:
        #print "HERE! " + cand
        letters[l].remove_candidate(cand)


sorted_list = sorted(data_new, key=lambda x: x.frequency, reverse=True)  #
sorted_list = sorted(sorted_list, key=lambda x: len(x.candidates))

sortedDict = {}

for letter in sorted_list:
    sortedDict[letter.letter] = letter
    #print letter.to_string()

def dojob(letter, sol):
    print("sdfjds "+ letter.letter + " " + sol)
    if sol in letter.candidates.keys() and letter.solution == "_":

        solution = sol

        # check if solution violates dependencies
        print("dependencies for " + str(letter.letter) + " = " + str(sol) + " are " + str(letter.candidates[sol]))
        for dependency in letter.candidates[sol].keys():
            value = letter.candidates[sol][dependency]
            #print "checking " + str(dependency) + " that should be " + str(value)
            if value == {}:
                break
            other = sortedDict[dependency]
            has_match = False
            for val in value:
                # print "checking if " + str(val) + " is " + other.solution + " or one of " + str(other.candidates.keys())
                if val == other.solution or val in other.candidates.keys():
                    # print depkey
                    has_match = True
                # print other.candidates.keys()
                # print
            if not has_match:
                #print "NO"
                solution = "_"

        if solution != "_":
            #print "YES"
            set_solution_for_letter(letter, solution)


def set_solution_for_letter(letter, solution):
    letter.set_solution(solution)
    frequentLetters.remove(solution)
    print(" 01 setting " + letter.letter + " = " + solution + " with cand " + str(letter.candidates))

    for other_letter in sorted_list:
        other_letter.remove_candidate(solution)
        other_letter.validate_dependency(letter.letter, solution)

    for other_letter in sorted_list:
        if other_letter.letter == letter.letter:
            break;
        for candid in other_letter.candidates.keys():
            print("LOOKING FOR " + letter.letter + "="+ solution + " in " + str(other_letter.candidates[candid]))
            #print("BEFORE =" + str(other_letter.to_string()))
            if letter.letter in other_letter.candidates[candid].keys():
                #print "1"
                if solution in other_letter.candidates[candid][letter.letter] or other_letter.candidates[candid][letter.letter] == {}:
                    print("FULFILLED = " + str(other_letter.candidates[candid][letter.letter]))
                    # free candidate (dependency fulfilled)
                    other_letter.candidates[candid][letter.letter] = {}
                else:
                    print("ARGH")
                    # delete candidate
                    del other_letter.candidates[candid]
                #print "NOT"
            print("AFTER =" + str(other_letter.to_string()))


a = filter(lambda k: len(k) <= 3, withWhitespaces.split(' '))
counter = collections.Counter(a)

print
print counter.most_common(10)
print

the = counter.most_common(1)[0][0]

the_eng = "the"

for entry in sorted_list:
    print entry.to_string()

for idx, c in enumerate(the):
    print(" 02 setting " + str(letters[c].letter) + " = " + str(the_eng[idx]))
    set_solution_for_letter(letters[c], the_eng[idx])

print
print("the is ready")
print

for entry in sorted_list:
    print entry.to_string()

# for letter in sorted_list:
for letter in sorted_list:
    sortedprob = sorted(letter.candidatesProbability.items(), key=operator.itemgetter(1))
    print "letter " + letter.letter + " prob: " + str(sortedprob)

    for fq in sortedprob:

        dojob(letter, fq[0])

    # for x in sortedDict.values():
    # print (x.to_string())

transDict = {'a': "_", 'b': "_", 'c': "_", 'd': "_", 'e': "_", 'f': "_", 'g': "_", 'h': "_", 'i': "_", 'j': "_",
             'k': "_",
             'l': "_", 'm': "_", 'n': "_", 'o': "_", 'p': "_", 'q': "_", 'r': "_", 's': "_", 't': "_", 'u': "_",
             'v': "_",
             'w': "_", 'x': "_", 'y': "_", 'z': "_", " ": " "}

for entry in sorted_list:
    print entry.to_string()

for entry in sorted_list:
    transDict[entry.letter] = entry.solution

print
print withWhitespaces
print
print decrypt(withWhitespaces, transDict)
print
print readFileToString(inputFilename)
