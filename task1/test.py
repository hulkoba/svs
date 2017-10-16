import os
import re
from utils import *

lowerLetters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v','k', 'j', 'x', 'q', 'z']
letters = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
letterStats = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
cipherStats = {'E': 0, 'T': 0, 'A': 0, 'O': 0, 'I': 0, 'N': 0, 'S': 0, 'H': 0, 'R': 0, 'D': 0, 'L': 0, 'C': 0, 'U': 0, 'M': 0, 'W': 0, 'F': 0, 'G': 0, 'Y': 0, 'P': 0, 'B': 0, 'V': 0, 'K': 0, 'J': 0, 'X': 0, 'Q': 0, 'Z': 0}
oneLetterDictionary = ['A', 'I']
twoLetterDictionary = ['OF', 'TO', 'IN', 'IT', 'IS', 'BE', 'AS', 'AT', 'SO', 'WE', 'HE', 'BY', 'OR', 'ON', 'DO', 'IF', 'ME', 'MY', 'UP', 'AN', 'GO', 'NO', 'US', 'AM']
threeLetterDictionary = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'ANY', 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'MAN', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'TOO', 'USE']
sortedCipherStats = {}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def removeNonLetters(text, spaces=False):
    text = text.upper()
    localAlphabet = alphabet
    if spaces:
        localAlphabet += ' '
    nonLetters = removeMatches(text, localAlphabet, False)
    text = removeMatches(text, nonLetters, True, spaces)

    return text

def removeMatches (string, removeString, doubles, spaces=False):
    outputString = []
    for ch in string:
        if ch not in removeString:
            if doubles or (not doubles and ch not in outputString):
                outputString.append(ch)
        elif spaces:
            outputString.append(' ')

    outputString = ''.join(outputString)
    if spaces:
        outputString = ' '.join(outputString.split())

    return outputString

def countStats(text):
    globalCounter = 0
    for letter in letters:
        counter = text.count(letter.lower())
        globalCounter = globalCounter + counter
        cipherStats[letter] += counter;
    return globalCounter;


def calcStats(globalCounter):
    print('Calculating Letterstats ...\n')
    for letter in cipherStats:
        temp = cipherStats[letter]
        cipherStats[letter] = (temp/globalCounter)*100;


def firstLetterReplace(text, sortedDic, tempdic):
    templine=''
    text
    for c in text:
        if ( c!='?' and  c!='!' and  c!='\'' and   c!='\"' and  c!=')' and c!='(' and  c!='*' and  c!='#' and  c!=']' and c!='\n' and c!='[' and c!= ' ' and c!="'" and c!="," and c!= '.' and c!='-'and c!=';'and c!=':'and c!='1'and c!='2'and c!='4'and c!='8'and c!='9'and c!='7'and c!='3'and c!='0'and c!='5'and c!='6'):
            #tempdic = sorted(sortedDic, key=sortedDic.get, reverse=True)

            ind = tempdic.index(c.upper())
            #print(sortedDic[ind])
            #c.replace(c, )
            templine += lowerLetters[ind];
        else:
            templine += c;
    return templine;

def sortUp(dicti):
    return sorted(dicti.items(), key=getValue, reverse=True)

def readout(dicti):
    for w in dicti:
        print(w  )

def countWords(ciphertext, letterLength):
    words = ciphertext.split()
    rightWords = {}
    for word in words:
        if len(removeNonLetters(word)) == letterLength:
            rightWords[removeNonLetters(word)] = rightWords.get(removeNonLetters(word), 0) + 1
    return sortUp(rightWords)

def checkWords(dictionary, letterLength, ciphertext):
    cipherDict = countWords(ciphertext, letterLength)
    print
    wordDictLen = len(dictionary)
    dict = {}

    for i in range(min(wordDictLen, len(cipherDict))):
        cipherWord = cipherDict[i][0]
        tempdict = cipherDict


        if cipherWord in dictionary:
            continue
        print("compare words")
        hits = compareWords(cipherWord, dictionary, tempdict, letterLength)
        print("find hit")
        print('Word to compare: ' + cipherWord)
        hit = findHit(hits, cipherWord)

        if not hit:
            continue
        for j in range(len(cipherWord)):
            if cipherWord[j] not in dict and hit[j] not in dict and cipherWord[j] != hit[j]:
                dict[cipherWord[j]] = hit[j]
                dict[hit[j]] = cipherWord[j]
                cipherDict = updateWords(cipherDict, {cipherWord[j]: hit[j], hit[j]: cipherWord[j]})
                print("\n Cipherdict")
                print(cipherDict)
                print("\n")

    if len(dict) != 0:
        ciphertext = translateText(ciphertext, dict)
        #print(ciphertext)

    return ciphertext

def countLetterFrequency(text):
    text = removeNonLetters(text)
    letterCount = {}
    total = float(len(text))
    for ch in text:
        letterCount[ch] = letterCount.get(ch, 0) + 1
    for ch in letterCount:
        letterCount[ch] = (letterCount[ch]/total)*100

    return letterCount

def translateText(ciphertext, translationDict):
    translatedText = []
    for ch in ciphertext:
        if ch.upper() in translationDict:
            translatedCh = translationDict[ch.upper()]
            if ch.islower():
                translatedCh = translatedCh.lower()
            translatedText.append(translatedCh)
        else:
            translatedText.append(ch)

    translatedTextString = ''.join(translatedText)

    global sortedCipherStats
    sortedCipherStats = countLetterFrequency(translatedTextString)

    return translatedTextString

def updateWords(words, translastionDict):
    updatedWords = []
    for word in words:
        updatedWord = word
        for ch in translastionDict:
            if ch in word[0]:
                wordString = []
                for ch in word[0]:
                    if ch in translastionDict:
                        wordString.append(translastionDict[ch])
                    else:
                        wordString.append(ch)
                wordString = ''.join(wordString)
                updatedWord = (wordString, word[1])
        updatedWords.append(updatedWord)

    return updatedWords

def findHit(hits, cipherWord):
    if len(hits) == 0:
        return None
    bestHit = hits[0]
    for hit in hits[1:]:
        if cor(cipherWord, hit) > cor(cipherWord, bestHit):
            bestHit = hit
        elif cor(cipherWord, hit) == cor(cipherWord, bestHit)\
                and occu(cipherWord, hit) < occu(cipherWord, bestHit):
            bestHit = hit

    return bestHit

def cor(word1, word2):
    count = 0
    if len(word2) > len(word1):
        tmpWord = word1
        word2 = word1
        word1 = tmpWord

    for ch in word1:
        if ch in word2:
            count += 1

    return count

def occu(word1, word2):
    word1 = word1.upper()
    word2 = word2.upper()
    value = 0
    tempdict = dict(sortedCipherStats)
    print("tempdictionary")
    print(tempdict)
    print("\n")
    for i in range(min(len(word1), len(word2))):

        value += abs(tempdict[word1[i]] - tempdict[word2[i]])

    return value

def compareWords(cipherWord, rightDict, cipherDict, length):
    hits=[]
    for rightWord in rightDict:
        rightLetters = 0
        i = 0
        while i < length:
            if cipherWord[i] == rightWord[i]:
                print("yes")
                rightLetters += 1
                i+= 1
                continue
            i+= 1
        if rightLetters == length-1:
            hits.append(rightWord)
    print("Candidates for Comparing -----")
    print(hits)
    print("-------------\n")
    return hits


def getValue(item):
    return item[1]

def sortList(dicti):
    return sorted(dicti, key=dicti.get, reverse=True)

def main():
    global cipherStats
    global sortedCipherStats

    #fo = open(currentDirectory+"\\ciphertext.txt")
    #text = fo.read();
    text = readFileToString(outputFilename)
    #globalCounter=0
    #globalCounter = countStats(text)
    #calcStats(globalCounter);
    cipherStats = countLetterFrequency(text)
    sortedCipherStats = sorted(cipherStats.items(), key=getValue, reverse=True)
    sortemp = sortList(cipherStats)
    print(sortedCipherStats)
    print('Replacing Letters on first Instance')
    text = firstLetterReplace(text, sortedCipherStats, sortemp)
    #print(text)
    #print("\n\n\n-----------------Redo that stuff--------------------\n\n\n\n\n")
    text = checkWords(oneLetterDictionary, 1, text)
    #print(text)

    #text = checkWords(oneLetterDictionary, 1, text)
    print("\n\n\n\n\n\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n\n\n\n\n\n\n\n\n")
    #print(text)
    text = checkWords(twoLetterDictionary, 2, text)
    #text = checkWords(oneLetterDictionary, 1, text)
    #text = checkWords(oneLetterDictionary, 1, text)
    text = checkWords(threeLetterDictionary, 3, text)

    print(text)

main()