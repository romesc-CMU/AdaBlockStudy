import pandas as pd
import operator
import IPython
import nltk

master_data = 'master.csv'

df = pd.read_csv(master_data)
saved_column = df.Configuration #you can also use df['column_name']

IPython.embed()