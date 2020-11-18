import pandas as pd
import os
import plotly.express as px

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/Analysis/Baseball_results.csv")


df['Datetime'] = pd.to_datetime(df["Datetime"])
print(type(df['Datetime']
           ))
x = df['Datetime'].resample('Q', label='right').sum()
print(x)

# fig = px.scatter(x=df['Datetime'].resample('Q', label='right').sum(),
#                  y=df['Actual'],
#                  # hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
#                  )
#
# fig.show()
