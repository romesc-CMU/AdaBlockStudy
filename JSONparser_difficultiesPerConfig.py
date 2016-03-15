#!/usr/bin/python
import json, string
from collections import Counter
import csv
import operator
import IPython
import nltk
from datetime import datetime

data_filename = "forward_by_config.json"
parsed_data_filename = "parsed_" + data_filename

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
    test = {} 
    for config in data.keys():
      avgDiff = data[config]['difficulty_per_sentence']
      test[avgDiff] = config
    IPython.embed()
      


    #with open("output4.csv",'wb') as outFile:
    #    wr = csv.writer(outFile)

    #    headers = ['Worker ID']
    #    wr.writerow(headers)
    #    
    #    for session in data.keys():


    #        # assignID to each person/session
    #        internalID = data[session][0]

    #        # grab only the workerID from the JSON
    #        for field in data[session]:
    #            if 'worker_id' in field and len(field) >= 23:
    #                worker_id = field.split('=')[1]

    #        # parse for scenario descriptions and corresponding scenario specific data
    #        nextRow = [worker_id]
    #        wr.writerow(nextRow)

