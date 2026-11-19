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


# run the function to check that the data loads
df = load_data()

print("Rows loaded:", len(df))
print("Columns:", df.columns.tolist())