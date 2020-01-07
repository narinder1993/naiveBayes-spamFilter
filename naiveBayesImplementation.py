import os
import math
from _decimal import Decimal
from collections import Counter

directory_path = "mails/nw"

#reading the spam folder for creating spam dictionary
def createSpamDictionary(spam_words, iteration, filterCount):
    numOfFiles = len(os.listdir(directory_path + '/spam'))
    filesForIter = int(numOfFiles / filterCount)
    windowStart = iteration * filesForIter - 240
    windowEnd = windowStart + filesForIter + 240
    j = 0
    for file in os.listdir(directory_path + '/spam'):
        j = j + 1
        if (j >= windowStart and j <= windowEnd):
            try:
                fread = open(directory_path + '/spam/' + str(file), 'r')
                text = fread.read()
                text = text.lower()
                text1 = cleanText(text)
                words_in_file = text1.split(' ')
                spam_words += [word for word in words_in_file if word != ' ' and word != '']
            except:
                continue

def createHamDictionary(ham_words, iteration, filterCount):
    numOfFiles = len(os.listdir(directory_path + '/ham'))
    filesForIter = numOfFiles/filterCount
    windowStart = iteration * filesForIter - 240
    windowEnd = windowStart + filesForIter + 240
    j =0
    for file in os.listdir(directory_path + '/ham'):
        j = j + 1
        if (j >= windowStart and j<= windowEnd ):
            try:
                fread = open(directory_path + '/ham/' + str(file), 'r')
                text = fread.read()
                text = text.lower()
                text1 = cleanText(text)
                words_in_file = text1.split(' ')
                ham_words += [word for word in words_in_file if word != ' ' and word != '']
            except:
                continue

def processTestSetFile(testSetFile, fileName):
    fread = open(directory_path + '/testSet/' + fileName[0], 'r')
    text = fread.read()
    text = text.lower()
    text1 = cleanText(text)
    words_in_file = text1.split(' ')
    testSetFile += [word for word in words_in_file if word != ' ' and word != '']


def cleanText(text):
    stop_words = ['\n', '\t', '\r', '\'', '"', ':', ';', '.', '/', '!', '#', '$', '%', '{', '}', '(', ')', '?', '&', ']', '[',
     '-', '_', ',']
    for words in stop_words:
        text = text.replace(words, '')
    return text

def createDictionary(text):
    dictionary = Counter(text)
    waste_words = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now']
    list_to_remove = [k for k in dictionary]
    for item in list_to_remove:
        if item.isalpha() == False:
            del dictionary[item] #removes alpha numeric characters
        elif len(item) == 1:
            del dictionary[item] #deletes items with length 1
        elif  item in waste_words:
            del dictionary[item]
    dictionary = dictionary.most_common(4000)
    return dictionary

class outputArr:
    def __init__(self, fileName, hamProb, spamProb, verdict):
        self.fileName = fileName
        self.hamProb = hamProb
        self.spamProb = spamProb
        self.verdict = verdict

def executeNB(iteration, filterCount):
    #main implementation
    print("Training the algorithm......")
    spam_words = []
    ham_words = []
    #extracts words from the files in spam and ham folders
    createSpamDictionary(spam_words, iteration, filterCount)
    createHamDictionary(ham_words, iteration, filterCount)
    numSpam = len(spam_words)
    numHam = len(ham_words)
    #creates dictionary with frequency of occurance of words
    spam_words = createDictionary(spam_words)
    ham_words = createDictionary(ham_words)
    #calculate spam and ham probabilities
    hamProb = float(len(ham_words)) / float(len(ham_words) + len(spam_words))
    spamProb = float(len(spam_words)) / float(len(ham_words) + len(spam_words))
    #print('Probability of Ham: ' + str(hamProb*100))
    #print('Probability of Spam: ' + str(spamProb*100))
    spam_dict = dict(spam_words)
    ham_dict = dict(ham_words)
    outList = []

    print("Testing on the test set......")
    for file in os.listdir(directory_path + '/testSet'):
        testSetFile = []
        fileName = []
        fileName.append(str(file))
        processTestSetFile(testSetFile, fileName)
        testDict = createDictionary(testSetFile)
        testDict = dict(testDict)
        total_dict = len(spam_words) + len(ham_words)
        ham_denom = total_dict + numHam
        spam_denom = total_dict + numSpam

        tempHam = hamProb
        for words in testSetFile:
            if(ham_dict.get(words) != None):
                tempHam = float(tempHam) * ((float(ham_dict.get(words) + 1) / float(ham_denom)))
                tempHam = tempHam * 100000000

        tempSpam = spamProb
        for words in testSetFile:
            if (spam_dict.get(words) != None):
                tempSpam = float(tempSpam) * ((float(spam_dict.get(words) + 1) / float(spam_denom)))
                tempSpam = tempSpam * 100000000


        if (tempHam > tempSpam):
            verdict = "HAM"
        else:
            verdict = "SPAM"""
        outList.append(outputArr(fileName[0], tempHam, tempSpam, verdict))

    return outList