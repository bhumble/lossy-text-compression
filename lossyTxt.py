#!/usr/bin/python

import sys
import re


def createConversionMatrix(frequencyFilePath, thesaurusFilePath, conversionMatrixFilePath):
    conversionMatrix = dict()
    with open(frequencyFilePath, 'r') as frequencyFile:
        frequencyList = frequencyFile.readlines()
        with open(thesaurusFilePath, 'r') as thesaurusFile:
            with open(conversionMatrixFilePath, 'w', 1) as matrixFile:
                for line in thesaurusFile:
                    synonyms = line.split(',')
                    for synonym in synonyms:
                        mostCommonSynonymRank = len(frequencyList)
                        synonymRank = next((i for i, x in enumerate(frequencyList) if x.lower() == synonym.lower()), mostCommonSynonymRank)
                        if (synonymRank < mostCommonSynonymRank):
                            mostCommonSynonymRank = synonymRank
                            conversionMatrix[synonyms[0].lower()] = synonym.lower()
                            matrixFile.write((synonyms[0].lower() + ',' + conversionMatrix.get(synonyms[0].lower(), synonyms[0].lower())).strip() + '\n')
                    print((synonyms[0].lower() + ',' + conversionMatrix.get(synonyms[0].lower(), synonyms[0].lower())).strip()) # for debugging purposes
    return conversionMatrix

    
def loadConversionMatrix(conversionMatrixFilePath):
    conversionMatrix = dict()
    with open(conversionMatrixFilePath, 'r') as matrixFile:
        for line in matrixFile:
            synonyms = line.split(',')
            conversionMatrix[synonyms[0]] = synonyms[1].strip()
    return conversionMatrix

    
def compress(path, conversionMatrix):
    with open(path,'r') as f:
        for line in f:
            line = re.sub("[^A-Za-z' ]", '', line) # strip out punctuation and numbers
            for word in line.split():
                print(conversionMatrix.get(word, word) + ' ')
                
        
def main():
    conversionMatrix = createConversionMatrix('frequency.txt', 'thesaurus.txt', 'conversionMatrix.txt')
    #conversionMatrix = loadConversionMatrix('conversionMatrix.txt')
    #compress('pride-and-prejudice.txt', conversionMatrix)
    words = sys.argv
    words.pop(0) # remove script name from argv
    output = list()
    for word in words:
        output.append(conversionMatrix.get(word.lower(), word))
    print(' '.join(output))
    
    
main()