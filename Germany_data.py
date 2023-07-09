import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import psycopg2

df = pd.read_csv('Germany_autoscout24_2023.csv')
#print(df.head())
ind = df.columns[0]
orignal_df = df

#sutvarkome fuel_type stulpeli.
print('Shape before cleaning', df.shape, '\n')

for i in df.columns:
    print('{} column has {} missing values. Data type is {}'.format(i, df[i].isna().sum(), df[i].dtype))
print('')
missing_df = pd.DataFrame(df[df['fuel_consumption_l_100km'].isna()]['fuel_type'].value_counts())
missing_df.columns = ["Missing Count"]
missingCounts = df[df['fuel_consumption_l_100km'].isna()]['fuel_type'].value_counts()
totalCounts = df['fuel_type'].value_counts()
missing_df["Percent Missing"] = [round(missingCounts[i] / totalCounts[i], 2) for i in missing_df.index]

df['fuel_consumption_l_100km'] = df.apply(
        lambda row: float(0) if pd.isnull(row['fuel_consumption_l_100km']) & \
        ((row['fuel_type'] == 'Electric')  or \
         (row['fuel_type'] == 'Hydrogen')  or \
         (row['fuel_type'] == 'Ethanol')) else row['fuel_consumption_l_100km'],
    axis = 1
)

df = df[df['fuel_type'] != 'Unknown']
df = df[df['fuel_type'] != 'Other']
df = df.drop(columns = ind)
df = df.dropna()


missingCounts = df[df['fuel_consumption_l_100km'].isna()]['fuel_type'].value_counts()
totalCounts = df['fuel_type'].value_counts()
missing_df["Percent Missing After"] = [round(missingCounts[i] / totalCounts[i], 2) if i in missingCounts.index else 0 for i in missing_df.index]
#print(missing_df, '\n')

#print('Shape after cleaning',df.shape)

#sutvarkome auto metus:
#print('Values in the year column before filtering:')
#print(df['year'].unique(), '\n')
yearsToFilter = df['year'].unique()[:29] #apiribojam 29 metu reiksmemis, kadangi turime 1955-2023 laikotarpi
filt = []

for i in range(df.shape[0]):
    filt.append(df['year'].iloc[i] in yearsToFilter)
    #.iloc[i] selects the value at index i from the 'year' column. i is the loop variable that iterates over
    # the range of the number of rows in the DataFrame.
    # df['year'].iloc[i] in yearsToFilter checks whether the selected year value from the 'year' column is present
    # in the yearsToFilter list. It returns True if the value is found in the list, and False otherwise.
df = df[filt]
#print('Values after filtering:')
#print(df['year'].unique())

#auto consumption
#code appears to perform some data cleaning and filtering operations related to the 'fuel_consumption_l_100km'
# and 'fuel_type' columns in the DataFrame.


df['fuel_consumption_l_100km'] = df.apply(lambda row: float(row['fuel_consumption_g_km'][:3])
    if ('Reichweite' in row['fuel_consumption_g_km']) & (row['fuel_type'] == 'Electric') &
       ('k' not in row['fuel_consumption_g_km'][:3])
    else row['fuel_consumption_l_100km'],
    axis = 1)

filt = [(type(df['fuel_consumption_l_100km'].iloc[i]) != int) and
        (type(df['fuel_consumption_l_100km'].iloc[i]) != float)
        for i in range(len(df['fuel_consumption_l_100km']))]

df['fuel_consumption_l_100km'] = df.apply(lambda row: float((row['fuel_consumption_l_100km']
[:len(row['fuel_consumption_l_100km']) - len(' kWh/100 km')]).replace(',', '.'))
    if (' kWh/100 km' in str(row['fuel_consumption_l_100km'])) else row['fuel_consumption_l_100km'],
    axis = 1)

df['fuel_consumption_l_100km'] = df.apply(lambda row: 'To Drop'
if ((type(row['fuel_consumption_l_100km']) != float) or
    (row['fuel_consumption_l_100km'] == 0)) &
    (row['fuel_type'] == 'Electric')
else row['fuel_consumption_l_100km'],
    axis = 1)

df = df[(df['fuel_consumption_l_100km'] != 'To Drop')]
df[df['fuel_type'] == 'Electric'].head()

df['fuel_consumption_l_100km'] = df.apply(lambda row: float((row['fuel_consumption_l_100km']
[:len(row['fuel_consumption_l_100km']) - len(' l/100 km')]).replace(',', '.'))
    if (' l/100 km' in str(row['fuel_consumption_l_100km'])) else row['fuel_consumption_l_100km'],
    axis = 1)

df['fuel_consumption_l_100km'] = df.apply(
        lambda row: float((row['fuel_consumption_l_100km']
        [:len(row['fuel_consumption_l_100km']) - len(' kg/100 km')]).replace(',', '.')) \

    if (' kg/100 km' in str(row['fuel_consumption_l_100km'])) else row['fuel_consumption_l_100km'],
    axis = 1)

df = df[[type(df['fuel_consumption_l_100km'].iloc[i]) == float for i in range(df.shape[0])]]
df.head()

#sutvarkome stulpeliu duomenu tipus
df['price_in_euro'] = df['price_in_euro'].astype(int)
df['power_kw'] = df['power_kw'].astype(int)
df['fuel_consumption_l_100km'] = df['fuel_consumption_l_100km'].astype(float)
pd.options.display.max_columns = None
print(df.head(2))

db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'Auto_data',
    'user': 'postgres',
    'password': 'mamamyja'
}

def create_table():
    connection = psycopg2.connect(**db_params)
    create_table_query = """
        CREATE TABLE IF NOT EXISTS auto_market (
        id SERIAL PRIMARY KEY,
        brand VARCHAR(50),
        model VARCHAR(50),
        year VARCHAR(10),
        transmission_type VARCHAR(50),
        mileage_in_km FLOAT,
        fuel_type VARCHAR(50), 
        price_in_euro INTEGER
        )
        """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

create_table()

def insert_data():
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    for _, row in df.iterrows():
        insert_data_into_table = f"""
        INSERT INTO auto_market (brand, model, year, transmission_type, mileage_in_km, 
        fuel_type, price_in_euro)
        VALUES ('{row['brand']}','{row['model']}','{row['year']}','{row['transmission_type']}','{row['mileage_in_km']}',
        '{row['fuel_type']}','{row['price_in_euro']}')
        """
        cursor.execute(insert_data_into_table)
        connection.commit()
    cursor.close()
    connection.close()
insert_data()


for i in df.columns:
    print('{} column has {} missing values. Data type is {}'.format(i, df[i].isna().sum(), df[i].dtype))
    print(' ')