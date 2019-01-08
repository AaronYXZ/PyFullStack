from Models.modelInfo import ModelInfo
from Models.trainResult import TrainResult
from Models.testResult import TestResult
from Models.usecaseInfo import UsecaseInfo
import os
import pandas as pd
import numpy as np


def saveToDB(form, usecase_info):
    # usecase = form.usecaseName.data
    name = form.modelName.data
    date = form.modelDate.data
    version = form.modelVersion.data
    path = form.modelPath.data
    description = form.modelDescription.data
    savedModelInfo = ModelInfo.find_by_name(name)
    ## if model name / model path is duplicate (already exists in database, delete and update)
    # ToDo show a pop up window for user to choose if model name already exists in db
    if savedModelInfo:
        savedModelInfo.delete_from_db()

    modelInfo = ModelInfo( name=name, path=path, date=date, version=version,
                          description=description, usecase_info = usecase_info)
    modelInfo.save_to_db()

    trainPath = os.path.join(path, "training/output/avg-evaluation-results.txt")
    saveTrain(trainPath, modelInfo)
    testPath = os.path.join(path, "testing/final/")
    saveTest(testPath, modelInfo)


def saveUsecaseToDB(form):
    usecaseName = form.usecaseName.data
    usecaseDate = form.usecaseDate.data
    usecaseCategory = form.usecaseCategory.data
    usecaseDescription = form.usecaseDescription.data
    usecaseInfo = UsecaseInfo(usecaseName=usecaseName, usecaseDate=usecaseDate, usecaseCategory=usecaseCategory,
                              usecaseDescription=usecaseDescription)
    usecaseInfo.save_to_db()


def saveTrain(trainpath, modelInfo):
    data = pd.read_table(trainpath)

    for i in range(data.shape[0]):
        Field = data.iloc[i, 0]
        Extracted = data.iloc[i, 1]
        Gold = data.iloc[i, 2]
        Correct = data.iloc[i, 3]
        TP = Correct
        FP = Extracted - Correct
        FN = Gold - Correct
        Precision = data.iloc[i, 4]
        Recall = data.iloc[i, 5]
        F1 = data.iloc[i, 6]
        trainResult = TrainResult(Field=Field, TP=TP, FP=FP, FN=FN, Precision=Precision, Recall=Recall, F1=F1,
                                  model_info=modelInfo)
        trainResult.save_to_db()


def saveTest(testpath, modelInfo):
    paths = os.listdir(testpath)
    for path in paths:
        if path.startswith("statistics_"):
            completePath = os.path.join(os.path.join(testpath, path), "value_based/per-field.csv")
            result_day, result_time = path.split("_")[1], path.split("_")[2]
            result_name = result_day + "_" + result_time
            data = pd.read_csv(completePath)
            for i in range(data.shape[0]):
                Field = data.iloc[i, 0]
                TP = data.iloc[i, 1]
                FP = data.iloc[i, 3]
                FN = data.iloc[i, 4]
                Precision = data.iloc[i, 5]
                Recall = data.iloc[i, 6]
                F1 = data.iloc[i, 7]
                testResult = TestResult(result_name=result_name, Field=Field, TP=TP, FP=FP, FN=FN, Precision=Precision,
                                        Recall=Recall, F1=F1,
                                        model_info=modelInfo)
                testResult.save_to_db()
# def deleteModelFromDB(modelInfo):
