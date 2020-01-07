from naiveBayesImplementation import executeNB
from datetime import datetime

class outputArr:
    def __init__(self, fileName, hamProb, spamProb, verdict):
        self.fileName = fileName
        self.hamProb = hamProb
        self.spamProb = spamProb
        self.verdict = verdict


def iterationRunner(iterationIndex, filterCount):
    outputArr1 = executeNB(iterationIndex, filterCount)
    return outputArr1


# main block
hamTestFiles = 0
spamTestFiles = 0
truePositive = 0
falsePositive = 0
trueNegative = 0
falseNegative = 0

filterCount = 5  # number of NB Filters

dec = []
resArray = []

start = datetime.now()
startTimestamp = datetime.timestamp(start)
for iteration in range(filterCount):
    print("Results for Naive Bayes Filter " + str(iteration + 1))
    outputArr1 = iterationRunner(iteration, filterCount)
    resArray.append(outputArr1)

j = 0
for arr in resArray:
    for i in range(len(arr)):
        fileN = arr[i].fileName
        spam = arr[i].spamProb
        ham = arr[i].hamProb
        verd = arr[i].verdict
        if j == 0:
            dec.append(outputArr(fileN, ham, spam, verd))
        else:
            dec[i].spamProb += spam
            dec[i].hamProb += ham
    j += 1

for elements in dec:
    fName = elements.fileName
    spamPr = elements.spamProb
    hamPr = elements.hamProb
    if spamPr > hamPr:
        ver = "spam"
    else:
        ver = "ham"
    print(fName + " is classified as " + ver)
    nameArr = fName.split('.')
    fileType = nameArr[len(nameArr) - 2]
    if fileType == "ham":
        hamTestFiles += 1
        if ver == "ham":
            trueNegative += 1
        else:
            falseNegative += 1
    if fileType == "spam":
        spamTestFiles += 1
        if ver == "spam":
            truePositive += 1
        else:
            falsePositive += 1

end = datetime.now()
endTimestamp = datetime.timestamp(end)

# calculating the statistics
acc = (truePositive + trueNegative) / (truePositive + trueNegative + falsePositive + falseNegative)
print("Execution Time: " + str(endTimestamp - startTimestamp) + "seconds")
print("Accuracy: " + str(acc * 100))
print("Recall: " + str((truePositive / (trueNegative + truePositive)) * 100))
sp = (truePositive / (falsePositive + truePositive)) * 100
hp = (trueNegative / (falseNegative + trueNegative)) * 100
print("Precision: " + str((sp+hp)/2))
"""print("True Positives: " + str(truePositive))
print("True Negatives: " + str(trueNegative))
print("False Positives: " + str(falsePositive))
print("False Negatives: " + str(falseNegative))"""
print("Spam Mis-classification Rate:" + str((falsePositive)/(falsePositive+trueNegative)))
print("Ham Mis-classification Rate:" + str((falseNegative)/(falseNegative+truePositive)))
print("Mail Mis-classification Rate:" + str((falsePositive + falseNegative)/ (falsePositive + falseNegative + trueNegative + truePositive)))
