from Models.info import ModelInfo
from Models.result import ModelResult
import os
import pandas as pd

def saveToDB(form):
    name = form.modelName.data
    date = form.modelDate.data
    version = form.modelVersion.data
    path = form.modelPath.data
    category = form.modelCategory.data
    description = form.modelDescription.data
    modelInfo = ModelInfo(name, path, date, version, category, description)
    modelInfo.save_to_db()


    wholePath = os.path.join(path, "training/output/avg-evaluation-results.txt")
    data = pd.read_table(wholePath)

    for i in range(data.shape[0]):
        Tag = data.iloc[i, 0]
        Extracted = data.iloc[i, 1]
        Gold = data.iloc[i, 2]
        Correct = data.iloc[i, 3]
        TP = Correct
        FP = Extracted - Correct
        FN = Gold - Correct
        Precision = data.iloc[i, 4]
        Recall = data.iloc[i, 5]
        F1 = data.iloc[i, 6]
        modelResult = ModelResult(Tag, TP, FP, FN, Precision, Recall, F1)
        modelResult.save_to_db()





