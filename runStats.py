import pandas as pd
import operator
import IPython
import nltk

master_data = 'master.csv'
df = pd.read_csv(master_data)

descrips = df.Description 
scenarios = df.Scenario 
agents = df.AgentType 
diffs = df.Difficulty 
times = df.TimeToComplete 
strategy = df.Strategy 
times = df.Challenging 
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

IPython.embed()
