import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import psycopg2

df = pd.read_csv('Germany_autoscout24_2023.csv')
ind = df.columns[0]
orignal_df = df

#sutvarkome fuel_type stulpeli.
print('Shape before cleaning', df.shape, '\n')

df = df[df['fuel_type'] != 'Unknown']
df = df[df['fuel_type'] != 'Other']
df = df.drop(columns = ind)
df = df.dropna()
#apiribojam 29 metu reiksmemis, kadangi turime 1995-2023 laikotarpi
yearsToFilter = df['year'].unique()[:29]
filt = []

for i in range(df.shape[0]):
    filt.append(df['year'].iloc[i] in yearsToFilter)
    #.iloc[i] selects the value at index i from the 'year' column. i is the loop variable that iterates over
    # the range of the number of rows in the DataFrame.
    # df['year'].iloc[i] in yearsToFilter checks whether the selected year value from the 'year' column is present
    # in the yearsToFilter list. It returns True if the value is found in the list, and False otherwise.
df = df[filt]

#sutvarkome stulpeliu duomenu tipus
df['price_in_euro'] = df['price_in_euro'].astype(int)

pd.options.display.max_columns = None
print(df.head(2))
#SITA REIKES ATKOMENTUOTI
# for i in df.columns:
#     print('{} column has {} missing values. Data type is {}'.format(i, df[i].isna().sum(), df[i].dtype))
#     prooblema su KIA CEED pavadimu, bandau taisyti:
df['model'] = df['model'].str.replace("'", "")
#Isikeliame lentele i Postgress
# db_params = {
#     'host': 'localhost',
#     'port': 5432,
#     'database': 'Auto_data',
#     'user': 'postgres',
#     'password': 'mamamyja'
# }

# def create_table():
#     connection = psycopg2.connect(**db_params)
#     create_table_query = """
#         CREATE TABLE IF NOT EXISTS auto_market (
#         id SERIAL PRIMARY KEY,
#         brand VARCHAR(50),
#         model VARCHAR(50),
#         year VARCHAR(10),
#         transmission_type VARCHAR(50),
#         mileage_in_km FLOAT,
#         fuel_type VARCHAR(50),
#         price_in_euro INTEGER
#         )
#         """
#     cursor = connection.cursor()
#     cursor.execute(create_table_query)
#     connection.commit()
#     cursor.close()
#     connection.close()
#
# create_table()
#
# def insert_data():
#     connection = psycopg2.connect(**db_params)
#     cursor = connection.cursor()
#     for _, row in df.iterrows():
#         insert_data_into_table = f"""
#         INSERT INTO auto_market (brand, model, year, transmission_type, mileage_in_km,
#         fuel_type, price_in_euro)
#         VALUES ('{row['brand']}','{row['model']}','{row['year']}','{row['transmission_type']}','{row['mileage_in_km']}',
#         '{row['fuel_type']}','{row['price_in_euro']}')
#         """
#         cursor.execute(insert_data_into_table)
#         connection.commit()
#     cursor.close()
#     connection.close()
# insert_data()

#isikeliame Lenkijos duomenis

df_pl = pd.read_csv('Polish_market_scrapped_on_2023 06 27.csv')

ind = df_pl.columns[0]
orignal_df_pl = df_pl
#norint pasiziureti pilna sarasa stulpeliu
pd.options.display.max_columns = None

#sukuriu nauja stulpeli su kaina eurais
df_pl['price_in_euro']= df_pl['price_in_pln']/4.55

#print('Shape before cleaning', df.shape, '\n')

#sutvarkome mileage stulpeli:
df_pl['mileage']=df_pl['mileage'].str.replace(" ","")
df_pl['mileage']=df_pl['mileage'].str.replace('km','')

#sutvarkome metus:
# print('Values in the year column before filtering:')
# print(df['year'].unique(), '\n')
yearsToFilter = df_pl['year'].unique()[:29]
filt = []

for i in range (df_pl.shape[0]):
    filt.append(df_pl['year'].iloc[i] in yearsToFilter)
df_pl=df_pl[filt]
# print("Values after filtering:")
# print(df['year'].unique())

#sutvarkome fuel_type:
# print('Values in the fuel_type column before filtering:')
# print(df['fuel_type'].unique(), '\n')
valid_fuels = ['Benzyna', 'Benzyna+LPG', 'Diesel', 'Hybryda','Elektryczny', 'Benzyna+CNG']
df_pl=df_pl[df_pl['fuel_type'].isin(valid_fuels)]
# print("Values after filtering:")
# print(df['fuel_type'].unique(), '\n')

#pakeiciame pavadinimus, kad butu angliski, ir butu galimybe palyginti su Vokietijos rinka
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Benzyna", "Petrol")
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Benzyna + LPG", "LPG")
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Hybryda", "Hybrid")
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Elektryczny", "Electric")
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Benzyna + CNG", "CNG")


df_lt = pd.read_csv('auto_listings.csv', encoding="utf8")




#Kurio brando vidutine kaina yra didziausia?
# VOKIETIJA
grouped = df.groupby('brand')['price_in_euro'].mean()
sorted_groups = grouped.sort_values(ascending=False)
top_8_brands = sorted_groups.head(8)
print(top_8_brands)
#lenkija
grouped = df_pl.groupby('brand')['price_in_euro'].mean()
sorted_groups = grouped.sort_values(ascending=False)
top_8_brands = sorted_groups.head(8)
print(top_8_brands)