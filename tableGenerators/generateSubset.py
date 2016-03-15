import pandas as pd
import IPython
import csv


master_data = 'master.csv'
outname = 'test.csv'

with open(master_data,'rb') as f:
   reader = csv.reader(f)
   data = list(reader)

out = []
out.append(data[1])
out.append(data[2])

IPython.embed()

with open(outname,'wb') as outFile:
   wr = csv.writer(outFile)
   wr.writerow(out)
