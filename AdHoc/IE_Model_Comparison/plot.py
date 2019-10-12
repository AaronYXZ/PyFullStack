import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set(font_scale=1.2)
colors = sns.color_palette("husl")

df = pd.read_csv("/Users/aaronyu/Desktop/Project16_IEmodel/Result/IE model summary by field.csv")
df_clean = df.dropna()
# print(df_clean.head())

def barplot(result_df: pd.DataFrame, output_path: str):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.barplot(x="FIELD", y="P",hue = "Model", data=result_df, ax=ax)
    plt.title("Precision comparison")
    plt.xlabel("Field")
    ax.figure.set_size_inches(18.5, 10.5)
    ax.figure.savefig(os.path.join(output_path, "Precision.png"))
    # plt.show()

    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.barplot(x="FIELD", y="R",hue = "Model", data=result_df, ax=ax)
    plt.title("Recal comparison")
    plt.xlabel("Field")
    ax.figure.set_size_inches(18.5, 10.5)
    ax.figure.savefig(os.path.join(output_path, "Recall.png"))

    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.barplot(x="FIELD", y="F1",hue = "Model", data=result_df, ax=ax)
    plt.title("F1 comparison")
    plt.xlabel("Field")
    ax.figure.set_size_inches(18.5, 10.5)
    ax.figure.savefig(os.path.join(output_path, "F1.png"))
    # plt.show()

barplot(df_clean, "/Users/aaronyu/Desktop/Project16_IEmodel/Result")