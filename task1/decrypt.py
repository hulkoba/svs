import string
import collections

import enchant

from utils import *
from constants import *
from letter import Letter

enchant = enchant.request_dict("en_US")

alphabet = list(string.ascii_lowercase)

transDict = {'a': "_", 'b': "_", 'c': "_", 'd': "_", 'e': "_", 'f': "_", 'g': "_", 'h': "_",
             'i': "_", 'j': "_", 'k': "_", 'l': "_", 'm': "_", 'n': "_", 'o': "_", 'p': "_",
             'q': "_", 'r': "_", 's': "_", 't': "_", 'u': "_", 'v': "_", 'w': "_", 'x': "_",
             'y': "_", 'z': "_", " ": " "}


##########################################################################################
########################### functions ####################################################
##########################################################################################

def decrypt(cipher, dictionary):
    word_text = ''

    for character in cipher:
        if character in dictionary:
            word_text += dictionary[character]
        else:
            word_text += "_"

    return word_text


def make_dependencies(eng_words, word):
    for c in word:
        letters.get(c).clean_candidates()
    for match in eng_words:
        for index, c in enumerate(word):
            character = letters.get(c)
            character.add_candidate(match[index])
            for dep_index, dep in enumerate(word):
                if dep_index != index:
                    character.add_dependency(match[index], dep, match[dep_index])


def dojob(letter, sol):
    if sol in letter.candidates.keys() and letter.solution == "_":

        solution = sol

        # check if solution violates dependencies
        for dependency in letter.candidates[sol].keys():
            value = letter.candidates[sol][dependency]
            if value == {}:
                break
            other = sorted_dict[dependency]
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
    FREQUENT_LETTERS.remove(solution)

    for other_letter in sorted_list:
        other_letter.remove_candidate(solution)
        other_letter.validate_dependency(letter.letter, solution)

    for other_letter in sorted_list:
        if other_letter.letter == letter.letter:
            break
        for candid in other_letter.candidates.keys():
            if letter.letter in other_letter.candidates[candid].keys():
                if solution in other_letter.candidates[candid][letter.letter] or other_letter.candidates[candid][letter.letter] == {}:
                    # free candidate (dependency fulfilled)
                    other_letter.candidates[candid][letter.letter] = {}
                else:
                    # delete candidate
                    del other_letter.candidates[candid]

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
    print "setting " + letter_from + " to " + letter_to
    transDict[letter_from] = letter_to
    letters_left.remove(letter_to)
    letters_brute_force.remove(letter_from)


##########################################################################################
########################### go ###########################################################
##########################################################################################

ciphertext = read_file_to_string(OUPUT_FILENAME)
frequency = get_letter_frequency(ciphertext)

cipher_with_spaces = add_whitespace(ciphertext, frequency[0][0])
cipher_without_spaces = cipher_with_spaces.split(' ')

freqDict = {}
frequency2 = get_letter_frequency(cipher_with_spaces.replace(' ', ''))
letters_total = len(cipher_with_spaces.replace(' ', ''))


for letter, score in frequency2:
    freqDict[letter] = (score / float(letters_total)) * 100

del freqDict[' ']

#################################### function
letters = {}
for letter in alphabet:
    newLetter = Letter(letter, freqDict[letter])
    for otherLetter in LETTER_PERCENTAGE:
        prob = LETTER_PERCENTAGE[otherLetter]
        newLetter.set_probability(otherLetter, abs(freqDict[letter] - prob))

    newLetter.set_frequency(dict(frequency2)[letter])
    letters[letter] = newLetter
#####################################

words = list(set(cipher_without_spaces))
words.sort(key=len)

########################################
three = get_words_with(3, words)
two = get_words_with(2, words)
one = get_words_with(1, words)


for w3 in three:
    make_dependencies(THREE_LETTER_WORDS, w3)

for w2 in two:
    make_dependencies(TWO_LETTER_WORDS, w2)

for w1 in one:
    make_dependencies(ONE_LETTER_WORDS, w1)
##########################################


for entry in letters.values():
    print entry.to_string()

##########################################

for l in letters:
    cands_to_remove = []
    for cand in letters[l].candidates.keys():
        for dep in letters[l].candidates[cand].keys():
            if letters[l].candidates[cand][dep] == set(cand):
                cands_to_remove.append(cand)

    for cand in cands_to_remove:
        letters[l].remove_candidate(cand)
#############################################

# wie oft kommt der Buchstabe vor?
letter_frequency = sorted(letters.values(), key=lambda x: x.frequency, reverse=True)

# Wie viele Kandidaten hat der Buchstabe?
sorted_list = sorted(letter_frequency, key=lambda x: len(x.candidates))

sorted_dict = {}
for letter in sorted_list:
    sorted_dict[letter.letter] = letter


three_letter_words = get_words_with(3, cipher_without_spaces)
# the is the most common word
the = collections.Counter(three_letter_words).most_common(1)[0][0]

for idx, c in enumerate(the):
    set_solution_for_letter(letters[c], "the"[idx])

for entry in sorted_list:
    print entry.to_string()

print

for letter in sorted_list:
    sortedprob = sort(letter.candidates_probability)
    for fq in sortedprob:
        dojob(letter, fq[0])


for entry in sorted_list:
    transDict[entry.letter] = entry.solution

print
print cipher_with_spaces
print
decrypted = decrypt(cipher_with_spaces, transDict)
print decrypted
print
print read_file_to_string(INPUT_FILENAME)

print
print "=============== PART2 : dict mapping ================="
print

letters_left = FREQUENT_LETTERS

letters_brute_force = []

for entry in sorted_list:
    if entry.solution == "_":
        letters_brute_force.append(entry.letter)

encryped_words_with_missing_letters = []
words_with_missing_letters = []
encr = cipher_without_spaces

for idx, word in enumerate(decrypted.split(' ')):
    if "_" in word:
        words_with_missing_letters.append(word)
        encryped_words_with_missing_letters.append(encr[idx])


words_with_missing_letters.sort(key=len, reverse=True)
encryped_words_with_missing_letters.sort(key=len, reverse=True)

print "words with missing letters: " + str(words_with_missing_letters)
print "words with missing letters: " + str(encryped_words_with_missing_letters)
print "Letter mapping missing: " + str(letters_brute_force)
print " ---------------------> " + str(letters_left)
print


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
    suggestions = enchant.suggest(word)

    # only take words that are of the same length as our word
    suggestions = filter(lambda k: len(k) == len(word), suggestions)
    print "word " + word + " could be " + str(suggestions)

    # go through all suggestions
    for sugg in suggestions:
        if validate_requirements(word, encrypted_word, sugg):
            for idc, char in enumerate(sugg):
                encrypted_letter = encrypted_word[idc]
                if word[idc] == "_" and encrypted_letter in letters_brute_force and char in letters_left:
                    assign_letter(encrypted_letter, char)
            break



print
print "=============== SOLUTION ================="
print
print 'cipher with spaces: \n', cipher_with_spaces
print
print 'decryped text :disco: \n', decrypt(cipher_with_spaces, transDict)
print
print 'given solution: \n', read_file_to_string(INPUT_FILENAME)
print
