import pandas as pd
import operator
import IPython
import nltk
import matplotlib.pyplot as plt
import numpy as np
import math
import networkx as nx


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


def repel_labels(ax, x, y, labels, k=0.01):
    G = nx.DiGraph()
    data_nodes = []
    init_pos = {}
    for xi, yi, label in zip(x, y, labels):
        data_str = 'data_{0}'.format(label)
        G.add_node(data_str)
        G.add_node(label)
        G.add_edge(label, data_str)
        data_nodes.append(data_str)
        init_pos[data_str] = (xi, yi)
        init_pos[label] = (xi, yi)

    pos = nx.spring_layout(G, pos=init_pos, fixed=data_nodes, k=k)

    # undo spring_layout's rescaling
    pos_after = np.vstack([pos[d] for d in data_nodes])
    pos_before = np.vstack([init_pos[d] for d in data_nodes])
    scale, shift_x = np.polyfit(pos_after[:,0], pos_before[:,0], 1)
    scale, shift_y = np.polyfit(pos_after[:,1], pos_before[:,1], 1)
    shift = np.array([shift_x, shift_y])
    for key, val in pos.iteritems():
        pos[key] = (val*scale) + shift

    for label, data_str in G.edges():
        ax.annotate(label,
                    xy=pos[data_str], xycoords='data',
                    xytext=pos[label], textcoords='data',
                    arrowprops=dict(arrowstyle="-",
                                    shrinkA=0, shrinkB=0,
                                    connectionstyle="arc3", 
                                    color='black'), )
    # expand limits
    all_pos = np.vstack(pos.values())
    x_span, y_span = np.ptp(all_pos, axis=0)
    mins = np.min(all_pos-x_span*0.15, 0)
    maxs = np.max(all_pos+y_span*0.15, 0)
    ax.set_xlim([mins[0], maxs[0]])
    ax.set_ylim([mins[1], maxs[1]])


master_data = 'invStudyDataset.csv'

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

# extract indices for human and robot responses
humInds = (agents == 'human')
robInds = (agents == 'robot')

humWords = descripsToWords(descrips[humInds])[0]
humVocab = descripsToWords(descrips[humInds])[1]
robWords = descripsToWords(descrips[robInds])[0]
robVocab = descripsToWords(descrips[robInds])[1]

# generate words distributions for robots and humans
fdistHum = nltk.FreqDist(humWords)
fdistRob = nltk.FreqDist(robWords)

# put all keys together to have total vocab
fdistAll = fdistHum.copy()
fdistAll.update(fdistRob)
# move dict into list of tuples sorted based on count (to show ordering of overall freq)
sorted_fdistAll = sorted(fdistAll.items(), key=operator.itemgetter(1), reverse=True)

humCountList = []
robCountList = []
vocab = []
# enumerate over keys of all words, make hum count list and rob count list
for pair in sorted_fdistAll:
   humCountList.append(fdistHum[pair[0]]) 
   robCountList.append(fdistRob[pair[0]]) 
   vocab.append(pair[0])

# find total number of words for robot and human and normalize counts for each
numHumWords = sum(humCountList)
numRobWords = sum(robCountList)
humCL_norm = [float(x*1000)/numHumWords for x in humCountList]
robCL_norm = [float(x*1000)/numRobWords for x in robCountList]



# cut off higher frequency terms
# removes 'the' and 'block'
humCL_norm = humCL_norm[2:45]
robCL_norm = robCL_norm[2:45]
vocab = vocab[2:45]

# plot
fig = plt.figure(figsize=(12,7))
ax1 = fig.add_subplot(111)
ax1.scatter(humCL_norm,robCL_norm,color='blue',s=10,edgecolor='none',zorder=10)
#ax1.set_yscale('log')
#ax1.set_xscale('log')
ax1.set_xlabel('Human relative freq')
ax1.set_ylabel('Robot relative freq')

# add annotations for each word
labels = vocab
#for label, x, y in zip(labels, humCountList, robCountList ):
#    plt.annotate(
#        label, 
#        xy = (x, y), xytext = (-20, 20),
#        textcoords = 'offset points', ha = 'right', rotation = '0', va = 'top',
#        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

##ann = []
##for i in range(0,43):
##    ann.append(ax1.annotate(labels[i], xy = (humCountList[i], robCountList[i])))
##
##mask = np.zeros(fig.canvas.get_width_height(), bool)

#plt.show()
##fig.canvas.draw()
##
##for a in ann:
##    bbox = a.get_window_extent()
##    x0 = int(bbox.x0)
##    x1 = int(math.ceil(bbox.x1))
##    y0 = int(bbox.y0)
##    y1 = int(math.ceil(bbox.y1))
##
##    s = np.s_[x0:x1+1, y0:y1+1]
##    if np.any(mask[s]):
##        a.set_visible(False)
##    else:
##        mask[s] = True

# draw word labels
repel_labels(ax1, humCL_norm, robCL_norm, labels, k=0.02)

# draw y=x line
lims = [
    np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both ax1es
    np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max1 of both ax1es
]

# now plot both limits against eachother
ax1.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
ax1.set_aspect('equal')
ax1.set_xlim(lims)
ax1.set_ylim(lims)

plt.show()

IPython.embed()

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
