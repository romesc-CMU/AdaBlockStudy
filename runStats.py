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

# current index for block configuration (scenario)
for c1 in range(1,15):
   for c2 in range(1,3):
      confInds = (scenarios == 'Configuration_'+ str(c1) +'_v'+ str(c2) +'.png')



      # intial parsing
      tokens = nltk.wordpunct_tokenize(' '.join(descrips[confInds]))
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

      # remove stop words
      filtered_words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]

      words = filtered_words

      # generate word distributions
      fdist1 = nltk.FreqDist(filtered_words)
      top25words = fdist1.most_common(25)


      # make plot of fdist (like word cloud maybe)

      # compute avg time to complete giving answer
      scenarioTimes = times[confInds]
      scenarioTimes = scenarioTimes.str.slice(5,10).apply(float)
      avgTime = round(scenarioTimes.mean(axis=0),2)

      # compute avg difficulty for scenario
      avgDiff = round(diffs[confInds].mean(0),2)

      # write top25 words to csv
      csvFrame = pd.DataFrame(top25words, columns=['Word','Freq'])
      appendFrame = pd.DataFrame([[avgDiff, avgTime]], columns=['Word', 'Freq'])
      csvFrame = csvFrame.append(appendFrame, ignore_index=True)  

      path = './configCSVs/'
      csvFrame.to_csv(path + 'Config_'+ str(c1) +'_v'+ str(c2) +'.csv')

IPython.embed()
