import pandas as pd


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/Analysis/Baseball_results.csv")


df['Datetime'] = pd.to_datetime(df["Datetime"])
print(type(df['Datetime']))
print(df['Datetime'][105].hour)


