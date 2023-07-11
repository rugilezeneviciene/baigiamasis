import pandas as pd
import numpy as np

data = pd.read_csv('naftos kainos.csv', delimiter=';')
df = pd.DataFrame(data)

print(df.dtypes)
df['date'] = pd.to_datetime(df['date'])
df['oil']=df['oil'].str.replace(",",".")

print(df.head())