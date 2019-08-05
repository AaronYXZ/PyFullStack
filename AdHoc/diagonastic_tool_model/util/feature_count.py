import os
import fnmatch
import json


feature_path = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/WorkSpace/feature_converter/features"
feature_path = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/WorkSpace/Baseline/training/output/model/invoice_number/features"

# file = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/WorkSpace/feature_converter/1907937.html.fe"

all_features = set()

for file in fnmatch.filter(os.listdir(feature_path), "*.fe"):
    full_file_name = os.path.join(feature_path, file)
    print("===================================")
    print(file)
    with open(full_file_name, "r") as tmp_file:
        for line in tmp_file:
            token = json.loads(line)
            features = token['fs']
            for fe in features:
                name = fe['n']
                value = fe['v']
                all_features.add(name)
    print(len(all_features))

print("*******************************************************************")
print("*******************************************************************")
print("*******************************************************************")
print(len(all_features))
