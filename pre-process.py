import re
import sys
import operator
from sklearn.svm import LinearSVC
from sets import Set

stopWordListFileName="stopwords.txt"
vocabulary = {}
total_words = 0
word_freq = {}

def getStopWords():
  stopWords = Set()
  fp = open(stopWordListFileName, 'r')
  line = fp.readline()
  while line:
    word = line.strip()
    stopWords.add(word)
    line = fp.readline()
  fp.close()
  return stopWords

stopWords = getStopWords()

def processLine(line):
  global stopWords, total_words, vocabulary, word_freq
  featureVector = []
  line = line.replace('\\', ' ')
  words = re.split('[?,.;:~"* !/]+', line)
  # print words

  for word in words:
    if not word in stopWords:
      if word_freq.has_key(word):
        word_freq[word] += 1
      else:
        word_freq[word] = 1
        vocabulary[word] = total_words
        total_words += 1

sentences = []
filename_obj = "objective"
filename_sub = "subjective"
fp = open(filename_obj, 'r')
line = fp.readline()
while line:
  sentences.append(line)
  line = fp.readline()
  processLine(line)

fp = open(filename_sub, 'r')
line = fp.readline()
while line:
  sentences.append(line)
  line = fp.readline()
  processLine(line)

fp.close()


# print vocabulary
# print total_words

total_words = 0
for word in word_freq.keys():
  freq = word_freq[word]
  if freq < 3:
    del vocabulary[word]
    del word_freq[word]
  else:
    vocabulary[word] = total_words
    total_words += 1


print "Total words: " + str(total_words)


# print word_list
# print meta_freq

def createCountFeatureVector(line):
  global vocabulary, total_words
  feature = [0] * total_words
  for word in line:
    if vocabulary.has_key(word):
      feature[vocabulary[word]] += 1
  return feature

print "Creating Feature Vectors..."

features = []
for line in sentences:
  features.append(createCountFeatureVector(line))

classes = ([0] * 1000) + ([1] * 1000)

print "Sending for Classifcation..."

classifier = LinearSVC(max_iter=100).fit(features, classes)
predictions = classifier.predict(features)


difference = [abs(a_i - b_i) for a_i, b_i in zip(classes, predictions)]
# print difference
print sum(difference)







