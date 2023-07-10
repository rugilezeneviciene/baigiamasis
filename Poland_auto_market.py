import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Polish_market_scrapped_on_2023 06 27.csv')

ind = df.columns[0]
orignal_df = df

pd.options.display.max_columns = None
# print(pd.get_option('display.max_rows', None))
print(df.head(2))

