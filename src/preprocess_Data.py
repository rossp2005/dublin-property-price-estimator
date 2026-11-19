# this file is different from cleanData.py as it will also handle feature preparation
# the preprocessing is split into functions so each stage can be run and tested separately
import pandas as pd


def load_data():
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

    return df

def clean_basic_data(df):
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

    # change the price from text into a number
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    return df


def filter_dublin_data(df):
    # keep only properties in Dublin
    dublin_df = df[df["county"] == "Dublin"].copy()

    # remove sales that were not sold at full market price
    dublin_df = dublin_df[
        dublin_df["not_full_market_price"] == "No"
    ]

    return dublin_df


def add_property_type(df):
    # create a simpler property type from the property description
    def get_property_type(description):
        description = str(description).lower()

        if "new dwelling" in description:
            return "New"
        elif "second-hand" in description:
            return "Second-Hand"
        else:
            return "Unknown"

    df["property_type"] = df["property_description"].apply(get_property_type)

    # remove properties where the type could not be identified
    df = df[
        df["property_type"] != "Unknown"
    ].copy()

    return df
def get_postcode(eircode):
    # check if the eircode is missing
    if pd.isna(eircode):
        return "Unknown"

    # clean the eircode and get the first 3 characters
    postcode = str(eircode).strip().upper()[:3]

    # list of recognised Dublin postcode areas
    dublin_postcodes = [
        "D01", "D02", "D03", "D04", "D05", "D06", "D6W",
        "D07", "D08", "D09", "D10", "D11", "D12",
        "D13", "D14", "D15", "D16", "D17", "D18",
        "D20", "D22", "D24"
    ]

    # check if the postcode is in the Dublin postcode list
    if postcode in dublin_postcodes:
        return postcode
    else:
        return "Unknown"


def add_postcode(df):
    # create a new postcode column using the eircode
    df["postcode"] = df["eircode"].apply(get_postcode)

    # remove properties without a recognised Dublin postcode
    df = df[
        df["postcode"] != "Unknown"
    ].copy()

    return df

# run the preprocessing functions
df = load_data()
df = clean_basic_data(df)
dublin_df = filter_dublin_data(df)
dublin_df = add_property_type(dublin_df)

# check the finished cleaning
print("Dublin properties:", len(dublin_df))

print("\nProperty types:")
print(dublin_df["property_type"].value_counts())

print("\nDate range:")
print(dublin_df["date_of_sale"].min(), "to", dublin_df["date_of_sale"].max())
postcode_df = add_postcode(dublin_df)

# check the postcode data
print("Properties with a Dublin postcode:", len(postcode_df))

print("\nProperties in each postcode:")
print(postcode_df["postcode"].value_counts().sort_index())

print("\nProperty types:")
print(postcode_df["property_type"].value_counts())