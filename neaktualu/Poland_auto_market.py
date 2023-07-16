import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('../Polish_market_scrapped_on_2023 06 27.csv')

ind = df.columns[0]
orignal_df = df
#norint pasiziureti pilna sarasa stulpeliu
pd.options.display.max_columns = None
# print(pd.get_option('display.max_rows', None))
#print(df.head(2))

#sukuriu nauja stulpeli su kaina eurais
df['price_in_euro']= df['price_in_pln']/4.55
#print(df['price_in_euro'])

#print('Shape before cleaning', df.shape, '\n')

#sutvarkome mileage stulpeli:
df['mileage']=df['mileage'].str.replace(" ","")
df['mileage']=df['mileage'].str.replace('km','')
#print(df['mileage_cleaned'])

#print(df.head())

#sutvarkome metus:
# print('Values in the year column before filtering:')
# print(df['year'].unique(), '\n')
yearsToFilter = df['year'].unique()[:29]
filt = []

for i in range (df.shape[0]):
    filt.append(df['year'].iloc[i] in yearsToFilter)
df=df[filt]
# print("Values after filtering:")
# print(df['year'].unique())

#sutvarkome fuel_type:
# print('Values in the fuel_type column before filtering:')
# print(df['fuel_type'].unique(), '\n')
valid_fuels = ['Benzyna', 'Benzyna+LPG', 'Diesel', 'Hybryda','Elektryczny', 'Benzyna+CNG']
df=df[df['fuel_type'].isin(valid_fuels)]
# print("Values after filtering:")
# print(df['fuel_type'].unique(), '\n')

#pakeiciame pavadinimus, kad butu angliski, ir butu galimybe palyginti su Vokietijos rinka
df['fuel_type'] = df['fuel_type'].str.replace("Benzyna", "Petrol")
df['fuel_type'] = df['fuel_type'].str.replace("Benzyna + LPG", "LPG")
df['fuel_type'] = df['fuel_type'].str.replace("Hybryda", "Hybrid")
df['fuel_type'] = df['fuel_type'].str.replace("Elektryczny", "Electric")
df['fuel_type'] = df['fuel_type'].str.replace("Benzyna + CNG", "CNG")
#print(df['fuel_type'].unique(), '\n')


#print(df['model'].unique(), '\n')