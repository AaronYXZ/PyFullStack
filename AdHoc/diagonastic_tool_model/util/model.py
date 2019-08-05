from multiprocessing import process
import time
import pandas as pd

global df

start = time.time()
for i, chunk in enumerate(pd.read_csv("final.csv", chunksize= 1000, low_memory=False)):
    print("working on {}th chunk, current time is {}".format(i, time.time()))
    print("Working on {}th".format(i))
    if i == 0:
        df = chunk.T
    else:
        df = pd.concat([df, chunk.T])

end = time.time()
print(df.shape)
print(end - start)
