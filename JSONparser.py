#!/usr/bin/python
import json, string
from collections import Counter
import csv
import operator
import IPython
import nltk
from datetime import datetime

data_filename = "trimmed_merged_data.json"
parsed_data_filename = "parsed_" + data_filename

# remove the elements without a 'success' tag
def incomplete_data_filter(data):
    for k in data.keys():
        if data[k][-1] != 'success':
            del data[k]

# field should be string like "occupation"
def outputField(data,field):
    count = 0
    statements = []
    for k in data.keys():
        for j in data[k]:
            if field in j:
                statements.append(j.split("=")[1])
                count = count + 1
    return (statements, count)                          

def init_parsed_data():
    parsed_data = {}
    from os import listdir
    from os.path import isfile, join
    mypath = '../images/images/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # print onlyfiles
    for f in onlyfiles:
        f = f[:-4]
        parsed_data[f] = {"avg_time": 0.0, "num_of_users": 0, "robot_words": {}, "human_words": {}, "metadata": []}
    # print parsed_data
    return parsed_data

def write_to_json(parsed_data):
    with open(parsed_data_filename, 'w') as fp:
        json.dump(parsed_data, fp)

# I had used states[0] to write initially
def write_to_csv(data):
    outFile = open("output.csv",'wb')
    wr = csv.writer(outFile)
    wr.writerows(data)

def time_elapsed(start_time_, end_time_):
    start_time = datetime.strptime(start_time_, '%Y-%m-%d %H:%M:%S.%f')
    # print start_time
    end_time = datetime.strptime(end_time_, '%Y-%m-%d %H:%M:%S.%f')
    # print end_time
    time = end_time - start_time
    # print time
    return time

def oldFindWordFreq():
    counter = Counter()
    for line in states[0]:
        tokens += sorted(set(line.split(' ')))
        counter += Counter(tokens)

def getDescCondOnRobot(data, wantRobot):
    if wantRobot:
        cond = 'robot'
    else:
        cond = 'human'

    count = 0
    statements = []
    for k in data.keys():
        for j in data[k]:
            if cond in data[k]:
                if 'image_desc' in j:
                    count = count + 1
                    statements.append(j.split("=")[1])

    return (statements, count)

def getDescForScenario(data, scenario):

    count = 0
    statements = []
    for session in data.keys():
        for idx, line in enumerate(data[session]):
            if 'image_name=Configuration_'+scenario+'.png' in line:
                if 'image_desc' in data[session][idx+1]:
                    count = count + 1
                    statements.append(data[session][idx+1].split("=")[1])

    return (statements, count)

def negToNone(value):
    if value == '-1':
        return None
    else:
        return int(value)




if __name__ == "__main__":
    with open(data_filename) as data_file:
        data = json.load(data_file)

    



    with open("output.csv",'wb') as outFile:
        wr = csv.writer(outFile)

        headers = ['Description','Scenario','AgentType','Difficulty','TimeToComplete','Strategy','Challenging?','General Comments','Age','Gender','Occupation','ComputerUsage','DominantHand','EnglishAsFirst','ExpWithRobots','ExpWithRCCars','ExpWithFPS','ExpWithRTS','ExpWithRobotComments','InternalUserID']
        wr.writerow(headers)
        
        for session in data.keys():

            # parse once per session entries
            agent, strat, challenge, comments, age, gender, occupation, compUse, hand, eng, expRobot, expCar, expVGFPS, expVGRTS, seenRobotExp = \
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

            # assignID to each person/session
            internalID = data[session][0]

            for field in data[session]:
                if 'human' in field and len(field) < 7:
                    agent = 'human'
                elif 'robot' in field and len(field) < 7:
                    agent = 'robot'
                if 'comment_strategy' in field:
                    strat = field.split('=')[1]
                if 'comment_challenging' in field:
                    challenge = field.split('=')[1]
                if 'comment_comment' in field:
                    comments = field.split('=')[1]
                if 'age' in field and len(field) < 7:
                    age = negToNone(field.split('=')[1])
                if 'gender' in field:
                    gender = field.split('=')[1]
                if 'occupation' in field:
                    occupation = field.split('=')[1]
                if 'computerUsage' in field:
                    compUse = field.split('=')[1]
                if 'handness' in field:
                    hand = field.split('=')[1]
                if 'english' in field:
                    eng = negToNone(field.split('=')[1])
                if 'expRobotRate' in field:
                    expRobot = negToNone(field.split('=')[1])
                if 'expCarRate' in field:
                    expCar = negToNone(field.split('=')[1])
                if 'expVGameRate' in field:
                    expVGFPS = negToNone(field.split('=')[1])
                if 'expSGameRate' in field:
                    expVGRTS = negToNone(field.split('=')[1])
                if 'seenRobotExp' in field:
                    seenRobotExp = field.split('=')[1]


            # parse for scenario descriptions and corresponding scenario specific data
            for idx, field in enumerate(data[session]):
                if 'image_desc' in field:
                    desc = field.split('=')[1]
                    config = data[session][idx-1].split('=')[1]
                    difficulty = negToNone(data[session][idx+1].split('=')[1])
                    time = time_elapsed(data[session][idx-2].split('=')[1], data[session][idx+2].split('=')[1])
                    nextRow = [desc, config, agent, difficulty, time, strat, challenge, comments, age, gender, occupation, compUse, hand, eng, expRobot, expCar, expVGFPS, expVGRTS, seenRobotExp, internalID]
                    wr.writerow(nextRow)



                # if  in j:
                #     statements.append(j.split("=")[1])
                #     count = count + 1

            # for desc in descriptions:
            #     nextRows.append(desc,config)
            # wr.writerows(nextRows)




    

    IPython.embed()


    # get image descriptions (list @states[0] holds a string with each description)

    # states = outputField(data,'image_desc')   #get overall
    # states = getDescCondOnRobot(data, True) #get robot
    # states = getDescCondOnRobot(data, False) #get human
    states = getDescForScenario(data, '1_v2') #get scenarios


    tokens = nltk.wordpunct_tokenize(' '.join(states[0]))
    text = nltk.Text(tokens)
    words = [w.lower() for w in text]
    vocab = sorted(set(words))

    # remove stop words, specified words in removeWords, and punctuation
    removeWords = {'rosario'}
    filtered_words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]
    filtered_words = [word for word in filtered_words if word not in removeWords]
    filtered_words = [w for w in filtered_words if w.isalnum()]

    #check for valid English
    # import enchant
    # d = enchant.Dict("en_US")
    # d.check("Hello")
    # d.check("Helo")
    # d.suggest("Helo")


    fdist1 = nltk.FreqDist(filtered_words)
    fdist1.most_common(50)
    fdist1.plot(50)


























    #incomplete_data_filter(data)
    # print len(data)
    #    parsed_data = {}
#     if os.path.isfile(parsed_data_filename):
        # if os.stat(parsed_data_filename).st_size == 0:
            # parsed_data = init_parsed_data()
            # print "new file"
            # write_to_file(parsed_data)
        # else:
            # with open(parsed_data_filename) as parsed_data_file:
                # parsed_data = json.load(parsed_data_file)
            # print "read file"
    # else:
        # parsed_data = init_parsed_data()
        # print "new file"
        # write_to_file(parsed_data)
    # # print len(parsed_data)

    # for k in data.keys():
    #     user_id = data[k][0]
    #     robot = data[k][2]
    #     example_time = time_elapsed(data[k][3][14:], data[k][5][12:])

    #     i = 0
    #     while 6+i*5<len(data[k])-14:
    #         image_index = int(data[k][6+i*5][16:])
    #         # print image_index
    #         image_start = data[k][7+i*5][12:]
    #         # print image_start
    #         image_end = data[k][10+i*5][10:]
    #         # print image_end
    #         time = time_elapsed(image_start, image_end)
    #         image_name = data[k][8+i*5][11:-4]
    #         # print image_name
    #         image_desc = data[k][9+i*5][11:]
    #         # print image_desc

    #         if image_name not in parsed_data:
    #             parsed_data[image_name] = {"avg_time": 0.0, "num_of_users": 0, "robot_words": {}, "human_words": {}, "metadata": []}

    #         # dict_ = {"user_id": user_id, "robot": robot, "time": str(time), "desc": image_desc}
    #         dict_ = {"user_id": user_id, "robot": robot, "time": time.total_seconds(), "desc": image_desc}
    #         parsed_data[image_name]["metadata"].append(dict_)

    #         image_words = image_desc.split()
    #         # print image_words
    #         # remove punctuations
    #         image_words = [''.join(c for c in s if c not in string.punctuation) for s in image_words]
    #         # print image_words
    #         # remove empty strings
    #         image_words = [s for s in image_words if s]
    #         # print image_words

    #         parsed_data[image_name]["avg_time"] += time.total_seconds()
    #         parsed_data[image_name]["num_of_users"] += 1

    #         for word in image_words:
    #             if robot == "robot":
    #                 if word in parsed_data[image_name]["robot_words"]:
    #                     parsed_data[image_name]["robot_words"][word] += 1
    #                 else:
    #                     parsed_data[image_name]["robot_words"][word] = 1
    #             else:
    #                 if word in parsed_data[image_name]["human_words"]:
    #                     parsed_data[image_name]["human_words"][word] += 1
    #                 else:
    #                     parsed_data[image_name]["human_words"][word] = 1
    #         i += 1

    # for k in parsed_data.keys():
    #     parsed_data[k]["avg_time"] /= float(parsed_data[k]["num_of_users"])

    # write_to_file(parsed_data)











