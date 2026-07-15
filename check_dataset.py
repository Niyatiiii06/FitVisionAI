import pandas as pd

df = pd.read_csv("data/dataset/pushup_dataset.csv")
print(df["label"].value_counts())