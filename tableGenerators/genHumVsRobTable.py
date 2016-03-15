import pandas as pd
import operator
import IPython
import nltk
import numpy as np
import math
from collections import defaultdict
import csv

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
master_data = 'postProcessedMaster.csv'
coded_data = 'codedData.csv'

header = csvToDoL(master_data)[0]
master_dol = csvToDoL(master_data)[1]
coded_dol = csvToDoL(coded_data)[1]

# munge 
rowsList = []
for k in coded_dol:
   description = master_dol[k][0]
   agent = master_dol[k][3] 
   wordCount = len(description.split())
   polite = 'please' in description or 'Please' in description 
   perspective = coded_dol[k][3]
   userID = master_dol[k][20]
   rowsList.append([k, agent, wordCount, polite, perspective, userID])

# export data
path = './tables/'
fileName = 'humanVsRobot.csv'

header_new = ['Index','AgentType','WordCount','Politeness','Perspective','userID'] 
lolToCsv(rowsList,header_new,path+fileName)

IPython.embed()

