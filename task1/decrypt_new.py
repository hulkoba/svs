import random, re, string, collections, operator
from pprint import pprint
from collections import defaultdict
import numpy as np
import enchant

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

transDict = {'a': "_", 'b': "_", 'c': "_", 'd': "_", 'e': "_", 'f': "_", 'g': "_", 'h': "_", 'i': "_", 'j': "_",
             'k': "_", 'l': "_", 'm': "_", 'n': "_", 'o': "_", 'p': "_", 'q': "_", 'r': "_", 's': "_", 't': "_",
             'u': "_", 'v': "_",  'w': "_", 'x': "_", 'y': "_", 'z': "_", " ": " "}

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
lettersTotal = len(withWhitespaces.replace(' ', ''))

freqDict = {}

frequency2 = getLetterFrequency(withWhitespaces.replace(' ', ''))

for letter, score in frequency2:
    freqDict[letter] = (score / float(lettersTotal)) * 100

del freqDict[' ']

letters = {}
for letter in alphabet:
    newLetter = Letter(letter, freqDict[letter])
    for otherLetter in englishLetterPercentage.keys():
        prob = englishLetterPercentage[otherLetter]
        newLetter.set_probability(otherLetter, abs(freqDict[letter] - prob))

    newLetter.set_frequency(dict(frequency2)[letter])
    letters[letter] = newLetter

data_new = np.array(letters.values()).flatten()

words = list(set(withWhitespaces.split(' ')))
words.sort(key=len)
three = filter(lambda k: len(k) == 3, words)
two = filter(lambda k: len(k) == 2, words)
one = filter(lambda k: len(k) == 1, words)


def make_dependencies(eng_words, word):
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

for l in letters:
    cands_to_remove = []
    for cand in letters[l].candidates.keys():
        for dep in letters[l].candidates[cand].keys():
            if letters[l].candidates[cand][dep] == set(cand):
                cands_to_remove.append(cand)
    for cand in cands_to_remove:
        letters[l].remove_candidate(cand)


sorted_list = sorted(data_new, key=lambda x: x.frequency, reverse=True)  #
sorted_list = sorted(sorted_list, key=lambda x: len(x.candidates))

sortedDict = {}

for letter in sorted_list:
    sortedDict[letter.letter] = letter

def dojob(letter, sol):
    if sol in letter.candidates.keys() and letter.solution == "_":

        solution = sol

        # check if solution violates dependencies
        for dependency in letter.candidates[sol].keys():
            value = letter.candidates[sol][dependency]
            if value == {}:
                break
            other = sortedDict[dependency]
            has_match = False
            for val in value:
                if val == other.solution or val in other.candidates.keys():
                    has_match = True
            if not has_match:
                solution = "_"

        if solution != "_":
            set_solution_for_letter(letter, solution)


def set_solution_for_letter(letter, solution):
    letter.set_solution(solution)
    frequentLetters.remove(solution)

    for other_letter in sorted_list:
        other_letter.remove_candidate(solution)
        other_letter.validate_dependency(letter.letter, solution)

    for other_letter in sorted_list:
        if other_letter.letter == letter.letter:
            break;
        for candid in other_letter.candidates.keys():
            if letter.letter in other_letter.candidates[candid].keys():
                if solution in other_letter.candidates[candid][letter.letter] or other_letter.candidates[candid][letter.letter] == {}:
                    # free candidate (dependency fulfilled)
                    other_letter.candidates[candid][letter.letter] = {}
                else:
                    # delete candidate
                    del other_letter.candidates[candid]


a = filter(lambda k: len(k) <= 3, withWhitespaces.split(' '))
the = collections.Counter(a).most_common(1)[0][0]

for idx, c in enumerate(the):
    set_solution_for_letter(letters[c], "the"[idx])

for entry in sorted_list:
    print(entry.to_string())

print

# for letter in sorted_list:
for letter in sorted_list:
    sortedprob = sorted(letter.candidatesProbability.items(), key=operator.itemgetter(1))
    for fq in sortedprob:
        dojob(letter, fq[0])


for entry in sorted_list:
    print(entry.to_string())
    transDict[entry.letter] = entry.solution

print
print withWhitespaces
print
decrypted = decrypt(withWhitespaces, transDict)
print decrypted
print
print readFileToString(inputFilename)

print
print("=============== PART2 : dict mapping =================")
print

letters_left = frequentLetters

letters_brute_force = []

for entry in sorted_list:
    if entry.solution == "_":
        letters_brute_force.append(entry.letter)

encryped_words_with_missing_letters = []
words_with_missing_letters = []
encr = withWhitespaces.split(" ")

for idx, word in enumerate(decrypted.split(' ')):
    if "_" in word:
        words_with_missing_letters.append(word)
        encryped_words_with_missing_letters.append(encr[idx])


words_with_missing_letters.sort(key=len, reverse=True)
encryped_words_with_missing_letters.sort(key=len, reverse=True)

print("words with missing letters: " + str(words_with_missing_letters))
print("words with missing letters: " + str(encryped_words_with_missing_letters))
print("Letter mapping missing: " + str(letters_brute_force))
print(" ---------------------> " + str(letters_left))
print


def validate_requirements(tmp_word, enc_word, suggestion):
    # check if suggestion matches all requirements
    for idc, char in enumerate(suggestion):
        # - letters are the same if not blanks
        same_if_not_blanks = tmp_word[idc] != "_" and tmp_word[idc] != char
        # - letters at blank postions are still missing
        is_blank = word[idc] == "_"
        letter_still_missing = enc_word[idc] not in letters_brute_force
        # - the value of the suggestion at the blank is still not assigned
        letter_not_assiged = char not in letters_left
        if same_if_not_blanks or (is_blank and (letter_still_missing or letter_not_assiged)):
            return False

    return True


def assign_letter(letter_from, letter_to):
    print("setting " + letter_from + " = " + letter_to)
    transDict[letter_from] = letter_to
    letters_left.remove(letter_to)
    letters_brute_force.remove(letter_from)


d = enchant.request_dict("en_US")

# go through all words with blanks
for idx, word in enumerate(words_with_missing_letters):
    encrypted_word = encryped_words_with_missing_letters[idx]

    # identify g as the last letter of a word if the two next to last letters are "in"
    if "g" not in transDict.values() and word[len(word) - 1] == "_" and word[len(word) - 3: len(word) - 1] == "in":
        encrypted_g = encrypted_word[len(word) - 1]
        assign_letter(encrypted_g, "g")

    # apply newest dicttionary to word
    word = decrypt(encrypted_word, transDict)

    # find suggestions
    suggestions = d.suggest(word)

    # only take words that are of the same length as our word
    suggestions = filter(lambda k: len(k) == len(word), suggestions)
    print("word " + word + " could be " + str(suggestions))

    # go through all suggestions
    for sugg in suggestions:

        if validate_requirements(word, encrypted_word, sugg):
            for idc, char in enumerate(sugg):
                encrypted_letter = encrypted_word[idc]
                if word[idc] == "_" and encrypted_letter in letters_brute_force and char in letters_left:
                    assign_letter(encrypted_letter, char)
            break

print
print("=============== SOLUTION =================")
print
print withWhitespaces
print
print decrypt(withWhitespaces, transDict)
print
print readFileToString(inputFilename)
print

