import os
import fnmatch
import numpy as np
import pandas as pd
import shutil
import random

ori_train_path = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/html_ie_train_english_processed"
output_train_path = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/NosieAddWorkSpace"
metadata_path = "/Users/aaronyu/PyFullStack/AdHoc/diagonastic_tool/resources/metadata"

fields = ["invoice_number", "invoice_total_amount", "bill_to_name", "vendor_name"]
threshold = np.arange(0.0, 1.05, 0.05)
noise_distribution = {"shrink": 0.25, "expand": 0.25, "random": 0.1, "swap": 0.2, "diff_pos": 0.2}
all_files = fnmatch.filter(os.listdir(ori_train_path), "*.html")
total_train_num = len(all_files)

for field in fields:
    ## read metadata into memory
    csv_name = field + "_change_log.csv"
    csv_file = os.path.join(metadata_path, csv_name)
    df = pd.read_csv(csv_file)
    df['Added'] = False

    ## create Train path
    field_output_path = os.path.join(output_train_path, field)
    if os.path.exists(field_output_path):
        shutil.rmtree(field_output_path)
    os.mkdir(field_output_path)

    for tmp_file in all_files:
        full_file_name = os.path.join(ori_train_path, tmp_file)
        shutil.copy(full_file_name, tmp_train_path)
    ## create Train_0 to Train_100 folder

    for noise_perc in threshold:
        tmp_train_name = "Train_" + str(noise_perc)
        tmp_train_path = os.path.join(field_output_path, tmp_train_path)
        os.mkdir(tmp_train_path)
        # copy all ori_train files to current folder
        for tmp_file in all_files:
            full_file_name = os.path.join(ori_train_path, tmp_file)
            shutil.copy(full_file_name, tmp_train_path)
        # random pick from file from
        random.seed(1)
        for key in noise_distribution.keys():
            noise_distribution[key] = round(noise_distribution[key] * total_train_num * noise_perc)







