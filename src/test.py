import pandas as pd


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/Analysis/Baseball_results.csv")


print(type(df["Datetime"][0]))

