import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("../Dataset.csv")

# Display first 5 rows
df.head()

# Dataset shape
print("Shape:", df.shape)

# Column names
print("Columns:")
print(df.columns)
# Dataset information
df.info()

# Statistical summary
df.describe()

# Check missing values
print("Missing values:")
print(df.isnull().sum())

# Check duplicate rows
print("Duplicate rows:", df.duplicated().sum())

# Check unique values
print("Fruits:")
print(df["Fruit"].unique())

print("\nClasses:")
print(df["Class"].unique())