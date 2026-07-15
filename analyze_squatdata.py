import pandas as pd

df = pd.read_csv("data/dataset/squat_dataset.csv")

print(df.shape)
print(df["label"].value_counts())