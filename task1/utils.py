import operator
import string

def get_alphabet():
    #abc = [chr(a+97) for a in range(26)]
    abc = list(string.ascii_lowercase)
    abc.append(' ')
    return abc

def read_file_to_string(filename):
    input_file = open(filename, 'r')
    data = input_file.read().replace('\n', ' ')
    input_file.close()
    return data

def write_string_to_file(filename, text):
    f = open(filename, 'w')
    f.write(text)
    f.close()

def sort(dictionary):
    return sorted(dictionary.items(), key=operator.itemgetter(1))


def get_letter_frequency(text):
    letter_frequency = dict()
    alphabet = get_alphabet()

    #init all values with zero
    for letter in alphabet:
        letter_frequency[letter] = 0

    #increment the specific value to get a first overview about the letter frequency
    for letter in text:
        letter_frequency[letter] += 1

    # sort the frequency array
    sorted_freq = sort(letter_frequency)
    sorted_freq.reverse()
    return sorted_freq

def get_keys(freq):
    keys = []
    for i in freq:
        keys.append(i[0])

    return keys

def get_words_with(number, words):
    return filter(lambda k: len(k) == number, words)

def add_whitespace(cipher, ws_letter):
    return cipher.replace(ws_letter, ' ')
