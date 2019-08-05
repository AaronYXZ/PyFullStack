import os
import fnmatch
import json
import pandas as pd
import numpy as np

feature_path = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/WorkSpace/feature_converter/features"
feature_path = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/WorkSpace/Baseline/training/output/model/invoice_number/features"
output_path = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/WorkSpace/converted_features"
# file = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/WorkSpace/feature_converter/1907937.html.fe"
feature_dict = {}

if not os.path.exists(output_path):
    os.makedirs(output_path)

for i, file in enumerate(fnmatch.filter(os.listdir(feature_path), "*.fe")):

    full_file_name = os.path.join(feature_path, file)
    if  (i + 1) % 20 == 0:
        print("-" * 80)
        print("Working on {}th file".format(i + 1))
        feature_df = pd.DataFrame(feature_dict).reset_index().fillna(0.0)
        output_file = os.path.join(output_path, "group" + str(i+1) + "_" + "feature.csv")
        feature_df.to_csv(output_file, index = False)
        feature_dict = {}
    with open(full_file_name, "r") as tmp_file:
        for line in tmp_file:
            token = json.loads(line)
            sr_values = []
            sr_index = []
            # unique_identifer
            unique_token = file.split(".")[0] + "_" + token['t'] + "_" + str(token['b'])

            # create document id
            sr_values.append(file)
            sr_index.append("document_id")
            # create token value
            sr_values.append(token['t'])
            sr_index.append("token")
            # create token label - gold or out
            sr_values.append(token['o'])
            sr_index.append("label")
            features = token['fs']
            features = [ dict(tup) for tup in set(tuple(item.items()) for item in features)]
            ## https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
            for fe in features:
                name = fe['n']
                value = fe['v']
                sr_index.append(name)
                sr_values.append(value)
                # if not name in sr_index:
                #     sr_index.append(name)
                #     sr_values.append(value)

            token_series = pd.Series(sr_values, index=sr_index)
            feature_dict[unique_token] = token_series

            ## check if duplicate index exists
            if len(sr_index) != len(set(sr_index)):
                print("Found duplicate index for token {}".format(unique_token))
                print([x for x in sr_index if sr_index.count(x) > 1])

print("Done")
