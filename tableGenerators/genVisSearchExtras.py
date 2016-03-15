import pandas as pd
import operator
import IPython
import nltk
import numpy as np
import math
from collections import defaultdict
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


# remove blanks from class bins
# count number of class instances per descrip of:
# [color, shape/pattern, density, orientation, environmental landmark, ordering//quantity]
counts = defaultdict(list)
for line in master_dol: #line is going to be index key for each line
   counts[line] = [0,0]
   description = master_dol[line][0]
   for idx,key in enumerate(['Ordering/Quantity','Position']): 
      wordClasses_dol[key] = filter(None,wordClasses_dol[key])
      for word in wordClasses_dol[key]:
         #regex to remove all non-alphanumerics/spaces
         parsed_line = re.sub(r'\W+', ' ', description).lower().split()
         if word in parsed_line:
            #do this to ensure we get multiple occurances of a word per desc.
            numOcc = parsed_line.count(word)
            counts[line][idx] = counts[line][idx] + numOcc 

# munge 
rowsList = []
for k in coded_dol:
   rowsList.append([k] + counts[k])

# export data
path = './tables/'
fileName = 'wordFreqCountsExtras.csv'

header_new = ['Index','Ordering/Quantity','Position'] 
lolToCsv(rowsList,header_new,path+fileName)

IPython.embed()

