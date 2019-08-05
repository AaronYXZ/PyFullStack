output_path = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/WorkSpace/converted_features"
import pandas as pd
import os
import fnmatch

global df
for i, file in enumerate(fnmatch.filter(os.listdir(output_path), "*.csv")):
    current_file = os.path.join(output_path, file)
    current_df = pd.read_csv(current_file, low_memory=False)
    if i == 0:
        df = current_df
    else:
        df = pd.merge(df, current_df, how = "outer")
        print("Finished on {}th".format(i))

df.to_csv("final.csv")
