import pandas as pd

# load the raw property price register data
file_path = "data/raw/PPR-ALL/PPR-ALL.csv"

df = pd.read_csv(
    file_path,
    encoding="cp1252",
    low_memory=False
)

# make the column names easier to use
df.columns = [
    "date_of_sale",
    "address",
    "county",
    "eircode",
    "price",
    "not_full_market_price",
    "vat_exclusive",
    "property_description",
    "property_size_description"
]

# turn the sale date into a proper date
df["date_of_sale"] = pd.to_datetime(
    df["date_of_sale"],
    format="%d/%m/%Y",
    errors="coerce"
)

# remove the euro sign and commas from the price
df["price"] = (
    df["price"]
    .str.replace("€", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

# change price from text into a number
df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

# check that the cleaning worked
print("Rows and columns:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nDate range:")
print(df["date_of_sale"].min())
print(df["date_of_sale"].max())

print("\nPrice summary:")
print(df["price"].describe())

print("\nData types:")
print(df.dtypes)
# get only the Dublin houses
dublin_df = df[df["county"] == "Dublin"]

# see how much Dublin data there is
print("\nDublin rows and columns:")
print(dublin_df.shape)

# check the Dublin prices
print("\nDublin price summary:")
print(dublin_df["price"].describe())

# check missing Dublin data
print("\nDublin missing values:")
print(dublin_df.isnull().sum())