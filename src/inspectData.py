# checking the raw Irish Property Price Register data before cleaning it
import pandas as pd

# path to the raw PPR file
file_path = "data/raw/PPR-ALL/PPR-ALL.csv"

# read the csv file
# latin1 is needed because utf-8 gave an error
df = pd.read_csv(file_path, encoding="cp1252")

# check how big the dataset is
print("Number of rows and columns:")
print(df.shape)

# see what columns are in the data
print("\nColumn names:")
print(df.columns.tolist())

# look at the first few rows
print("\nFirst 5 rows:")
print(df.head())

# check what type each column is
print("\nData types:")
print(df.dtypes)

# see how many missing values there are
print("\nMissing values:")
print(df.isnull().sum())