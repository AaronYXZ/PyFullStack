import pandas as pd
import os
import numpy as np

def Adjusted():
    pass


def read_data(path, name):
    full_name = os.path.join(path, name)
    df = pd.read_csv(path)
    df["GOLD_LABEL"] = ["Account Maintance" if x == "Account_Maintance" else x for x in df["GOLD_LABEL"].values.tolist()]
    return df

def modify_df(df, threshold):
    """

    :param threshold:
    :param df:
    :return: a copy of the original dataFrame, modifed extracted label and result
    """
    df_result = df.copy()
    n = df_result.shape[0]
    for i in range(n):
        if df.loc[i, "PROB"] < threshold:
            df.loc[i, "EXTRACTED_LABEL"] = "Not In Class"
            df.loc[i, "RESULT"] = "FP,FN"
    return df_result

def calculate_PR(df, thresh):
    unique_labels = np.unique(df['EXTRACTED_LABEL'])
    result = []
    for label in unique_labels:
        temp_dic = {}
        temp_dic['label'] = label
        temp_dic['threshold'] = thresh
        TP = df.loc[df["EXTRACTED_LABEL"] == label & df['RESULT'] == "TP"].shape[0]
        FP = df.loc[df["EXTRACTED_LABEL"] == label & df['RESULT'] == "FP,FN"].shape[0]
        FN = df.loc[df["GOLD_LABEL"] == label & df['RESULT'] == "FP,FN"].shape[0]
        Precision = TP / (TP + FP)
        Recall = TP / (TP + FN)
        F1 = 2 * Precision * Recall / (Precision + Recall)
        temp_dic['TP'] = TP
        temp_dic['FP'] = FP
        temp_dic['FN'] = FN
        temp_dic['P'] = Precision
        temp_dic["R"] = Recall
        temp_dic['F1'] = F1
        result.append(temp_dic)
    return result




def collect_result(df, min_thresh, max_thresh, step):
    result_df = []
    for thresh in np.arrange(min_thresh, max_thresh, step):
        df_result = modify_df(df, thresh)
        tmp_list = calculate_PR(df, thresh)
        result_df.extend(tmp_list)
    df = pd.DataFrame(result_df)
    return df





