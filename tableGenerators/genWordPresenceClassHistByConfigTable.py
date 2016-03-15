import pandas as pd
import IPython
import nltk
import numpy as np
import math
from collections import defaultdict
from operator import add
import csv
import re

# creates dictionary of dictionaries
def csvToDoD(fileName,keyColumnName):

   reader = csv.DictReader(open(fileName))

   result = {}
   for row in reader:
       key = int(row.pop(keyColumnName))
       if key in result:
           # implement duplicate row handling here
           pass
       result[key] = row
   return result

# creates dictionary of lists
def csvToDoL(fileName):

   with open(fileName, mode='r') as infile:
      reader = csv.reader(infile)
      dic = dict((rows[1],rows) for rows in reader)
   
   header = dic['Index']
   dic.pop('Index')
   dic = dict((int(k),v) for k,v in dic.iteritems()) 

   return header,dic 

def csvToDoLByHeaders(fileName):

   with open(fileName, 'rU') as infile:
     # read the file as a dictionary for each row ({header : value})
     reader = csv.DictReader(infile)
     data = {}
     for row in reader:
       for header, value in row.iteritems():
         try:
           data[header].append(value)
         except KeyError:
           data[header] = [value]

   return data

def dolToCsv(DoL, fieldnames,  filepath):
   with open(filepath , 'w' ) as f:
      writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\\', quotechar="")
      writer.writerow(fieldnames)
      for k, v in DoL.iteritems():
            writer.writerow(v)

def lolToCsv(DoL, fieldnames,  filepath):
   with open(filepath , 'w' ) as f:
      writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\\', quotechar="")
      writer.writerow(fieldnames)
      for  v in DoL:
            writer.writerow(v)

def descripsToWords(dataFrameOfWords):
   
   # intial parsing
   tokens = nltk.wordpunct_tokenize(' '.join(dataFrameOfWords))
   text = nltk.Text(tokens)
   words = [w.lower() for w in text]
   vocab = sorted(set(words))


   # remove words in removeWords list and punctuation
   removeWords = {'rosario'} # just an example
   filtered_words = [word for word in words if word not in removeWords]
   filtered_words = [w for w in filtered_words if w.isalnum()]

   words = filtered_words

   # check for valid English
   import enchant
   d = enchant.Dict("en_US")
   wordsValid = []
   for w in words:
      if d.check(w):
         wordsValid.append(w) 
      else:
         wordsValid.append(d.suggest(w)[0])	

   words = wordsValid

   return words, vocab

# import data
wordClasses_data = 'wordClassesCollapsed.csv'
master_data = 'postProcessedMaster.csv'
coded_data = 'codedData.csv'

wordClasses_dol = csvToDoLByHeaders(wordClasses_data)
header = csvToDoL(master_data)[0]
master_dol = csvToDoL(master_data)[1]
coded_dol = csvToDoL(coded_data)[1]

# compute current subset of 1400 from  master_dol based on coded dol responses
current1400_dol = dict((key,value) for key,value in master_dol.iteritems() if key in coded_dol)

# count number of class instances per descrip of:
# [action, object, color, pattern/shape, density, orientation, ordering/quantity, environmental landmark, position, perspective indicator]
counts = defaultdict(list)
for line in current1400_dol: #line is going to be index key for each line
   counts[line] = [0,0,0,0,0,0,0,0,0,0]
   description = current1400_dol[line][0]
   for idx,key in enumerate(['Action','Object','Color','Pattern/Shape','Density','Orientation','Ordering/Quantity','EnvLandmark','Position','PerspectiveIndicator']): 
      # remove blanks from class bins
      wordClasses_dol[key] = filter(None,wordClasses_dol[key])
      seenClass = False
      for word in wordClasses_dol[key]:
         #regex to remove all non-alphanumerics/spaces
         parsed_line = re.sub(r'\W+', ' ', description).lower().split()
         if word in parsed_line and  not seenClass:
            counts[line][idx] = counts[line][idx] + 1 
            seenClass = True


# find which description index (key) corresponds to each scenario, put these in a list
configShort = ['1_v1','1_v2',
            '2_v1','2_v2',
            '3_v1','3_v2',
            '4_v1','4_v2',
            '5_v1','5_v2',
            '6_v1','6_v2',
            '7_v1','7_v2',
            '8_v1','8_v2',
            '9_v1','9_v2',
            '10_v1','10_v2',
            '11_v1','11_v2',
            '12_v1','12_v2',
            '13_v1','13_v2',
            '14_v1','14_v2']
configList = ['Configuration_' + s + '.png' for s in configShort]


configCounts= [[0,0,0,0,0,0,0,0,0,0]]*28
for line in current1400_dol:
   # theres a better way to do this using dictionaries, but I'm confused, so for now the brute force hand-coded list method must suffice
   for idx,config in enumerate(configList):
      if current1400_dol[line][2] == config:
         configCounts[idx] = map(add,configCounts[idx],counts[line])
         

# munge 
rowsList = []
for idx,entry in enumerate(configCounts):
   rowsList.append([configShort[idx]] + configCounts[idx])


# export data
path = './tables/'
fileName = 'presenceCountsPerScenario.csv'

header_new = ['Configuration','Action','Object','Color','Pattern/Shape','Density','Orientation','Ordering/Quantity','EnvLandmark','Position','PerspectiveIndicator'] 
lolToCsv(rowsList,header_new,path+fileName)

IPython.embed()

