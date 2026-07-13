import pandas as pd

# Load dataset
df = pd.read_csv("data/dataset/squat_dataset.csv")

print("=" * 50)
print("DATASET INFORMATION")
print("=" * 50)

print("\nShape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum().sum())

print("\nLabel counts:")
print(df["label"].value_counts())

print("\nColumns:")
print(df.columns)