import pandas as pd
import operator
import IPython
import nltk
import enchant

master_data = 'master.csv'
df = pd.read_csv(master_data)

descrips = df.Description 
scenarios = df.Scenario 
agents = df.AgentType 
diffs = df.Difficulty 
times = df.TimeToComplete 
strategy = df.Strategy 
chalComms = df.Challenging 
genComms = df.GeneralComments 
ages = df.Age 
occs = df.Occupation 
compUsages = df.ComputerUsage 
hands = df.DominantHand 
engs = df.EnglishAsFirst 
expRobs = df.ExpWithRobots 
expRCs = df.ExpWithRCCars 
expFPSs = df.ExpWithFPS 
expRTSs = df.ExpWithRTS 
expRobComms = df.ExpWithRobotComments 
usrIDs = df.InternalUserID 


# intial parsing
tokens = nltk.wordpunct_tokenize(descrips[235])
text = nltk.Text(tokens)
words = [w.lower() for w in text]
vocab = sorted(set(words))


# check for valid English
d = enchant.Dict("en_US")
wordsValid = []
for w in words:
   if d.check(w):
      wordsValid.append(w) 
   else:
      wordsValid.append(d.suggest(w)[0])	

words = wordsValid

IPython.embed()

