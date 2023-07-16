import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import seaborn as sns
import psycopg2

#nuskaitome faila su vokietijos duomenimis
df_de = pd.read_csv('Germany_autoscout24_2023.csv')
ind = df_de.columns[0]
orignal_df_de = df_de

#sutvarkome fuel_type stulpeli.
df_de = df_de[df_de['fuel_type'] != 'Unknown']
df_de = df_de[df_de['fuel_type'] != 'Other']
df_de = df_de.drop(columns = ind)
df_de = df_de.dropna()

#sutvakome stulpeli 'year' . Apsiribojam 29 metu reiksmemis, kadangi turime 1995-2023 laikotarpi
yearsToFilter = df_de['year'].unique()[:29]
filt = []

#reikia patikrinti, ar is year stulpelio parenkta reiksme yra sarase yearToFiter
for i in range(df_de.shape[0]):
    filt.append(df_de['year'].iloc[i] in yearsToFilter)

df_de = df_de[filt]

#sutvarkome stulpeliu duomenu tipus
df_de['price_in_euro'] = df_de['price_in_euro'].astype(int)
df_de['brand'] = df_de['brand'].astype(str)
#  problema su KIA CEED pavadinimu, sutvarkau:
df_de['model'] = df_de['model'].str.replace("'", "")
#pasiziurejimui visu duomenu
pd.options.display.max_columns = None

#suskaiciavimui kiek truksta reiksmiu stulpeliuose, tipo nustatymui, info isspausdinimui
#SITA REIKES ATKOMENTUOTI
# for i in df_de.columns:
#     print('{} column has {} missing values. Data type is {}'.format(i, df_de[i].isna().sum(), df_de[i].dtype))

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
#     for _, row in df_de.iterrows():
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
#priskiriame pirmojo stulpelio antraštę kintamajam "ind"
ind = df_pl.columns[0]
#sukuriame naują DataFrame "original_df_pl",
#kuris nurodo tą pačią informaciją kaip ir "df_pl".
orignal_df_pl = df_pl
#norint pasiziureti pilna sarasa stulpeliu
pd.options.display.max_columns = None

#sukuriu nauja stulpeli su kaina eurais
df_pl['price_in_euro']= df_pl['price_in_pln']/4.55

#sutvarkome mileage stulpeli:
df_pl['mileage']=df_pl['mileage'].str.replace(" ","")
df_pl['mileage']=df_pl['mileage'].str.replace('km','')

#sutvarkome mielage stulpelio pavadinima kad suvienodinti su kitomis salimis
df_pl= df_pl.rename(columns={'mileage': 'mileage_in_km'})
#sulyginame kainu stulpelio duomenu tipus:
df_pl['price_in_euro']=df_pl['price_in_euro'].astype('int64')

df_pl = df_pl.drop(df_pl[df_pl['mileage_in_km'] == 'Elektryczny'].index)
df_pl = df_pl.drop(df_pl[df_pl['mileage_in_km'] == 'Benzyna'].index)
#sutvarkome metus:

yearsToFilter = df_pl['year'].unique()[:29]
filt = []

for i in range (df_pl.shape[0]):
    filt.append(df_pl['year'].iloc[i] in yearsToFilter)
df_pl=df_pl[filt]

#sutvarkome fuel_type:

valid_fuels = ['Benzyna', 'Benzyna+LPG', 'Diesel', 'Hybryda','Elektryczny', 'Benzyna+CNG']
df_pl=df_pl[df_pl['fuel_type'].isin(valid_fuels)]

#pakeiciame pavadinimus, kad butu angliski, ir butu galimybe palyginti su Vokietijos rinka
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Benzyna", "Petrol")
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Benzyna + LPG", "LPG")
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Hybryda", "Hybrid")
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Elektryczny", "Electric")
df_pl['fuel_type'] = df_pl['fuel_type'].str.replace("Benzyna + CNG", "CNG")

#kilometrazui parenkamas float.
df_pl['mileage_in_km']=df_pl['mileage_in_km'].astype('float64')


#nuskaitome LT nuscrapinta faila
df_lt = pd.read_csv('auto_listings.csv', encoding="utf8")

df_lt = pd.DataFrame(df_lt)

#sutvarkome kad fuel_type butu tvarkingi duomenys. su replace sutvarkyti nepavyko, nereagavo,
#todel panaudojau contains, kuris veikia kaip boolean, randa kWh ir pakeicia
df_lt.loc[df_lt['fuel_type'].str.contains(r"\d+ kWh"), 'fuel_type'] = "Electric"
# LT duomenyse istrinta reiksme, kuri neatitinka kuro pavadinimo
df_lt = df_lt.drop(df_lt[df_lt['fuel_type'] == '2020 y'].index)
#nesutapo kuro pasiskirstymas, todel suvienodinu is lt duomenu Gasoline i Petrol
df_lt['fuel_type'] = df_lt['fuel_type'].str.replace("Gasoline", "Petrol")



#KURIO BRANDO VIDUTINE KAINA YRA DIDZIAUSIA?

#pasirasome funkcija suskaiciuoti modelius, kuriu vidutine kaina yra didziauia
def top_8_brangiausi_pagal_kainu_vidurki(data, n=8):
    average_price = data.groupby('brand')['price_in_euro'].mean()
    top_8_brands = average_price.nlargest(n)
    top_8_brands = top_8_brands.astype(int)
    return top_8_brands

#funkcija pritaikome kiekvienai valstybei atskirai
# top_8_brands = top_8_brangiausi_pagal_kainu_vidurki(df_de, n=8)
# print('TOP 8 Vokietijoje brangiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(top_8_brands)
#
# top_8_brands = top_8_brangiausi_pagal_kainu_vidurki(df_pl, n=8)
# print('TOP 8 Lenkijoje brangiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(top_8_brands)
#
# top_8_brands = top_8_brangiausi_pagal_kainu_vidurki(df_lt, n=8)
# print('TOP 8 Lietuvoje brangiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(top_8_brands)

#pasirasome funkcija diagramai
def stulpeline_diagrama (data, labels, title):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta']
    plt.figure(figsize=(10,6))
    bars = plt.bar(labels, data, color=colors)
    plt.xlabel(' ')
    plt.ylabel('Vidutine kaina eurais')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')

    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, round(data[i], 2), ha='center', va='bottom')


    plt.tight_layout()
    plt.savefig('Stulpeline diagrama')
    plt.show()
def main(data, n=8):
    average_price = data.groupby('brand')['price_in_euro'].mean()
    top_8_brands = average_price.nlargest(n)
    top_8_brands = top_8_brands.astype(int)
    labels = top_8_brands.index.tolist()
    valstybeje = input("Iveskite salies, kurios skrituline diagrama atvaiztuojate")
    title = (f'TOP 8 Automobiliu modeliai pagal auksciausia vidutine kaina {valstybeje}')
    stulpeline_diagrama(top_8_brands,labels,title)

    if __name__ == '__main__':
        main(df_de)
#paleidziame funkcija, ir norint pakeisti Title, priklausmai nuo to, kurios salies lentele rodome,
# input irasome pvz.Vokietijoje
#Vokietija = main(df_lt)

#pasirasome funkcija suskaiciuoti modelius, kuriu vidutine kaina yra maziausia:
def top_8_pigiausi_pagal_kainu_vidurki(data, n=8):
    average_price = data.groupby('brand')['price_in_euro'].mean()
    The_cheapest_8_brands = average_price.nsmallest(n)
    return The_cheapest_8_brands

cheapest_brands = top_8_pigiausi_pagal_kainu_vidurki(df_de, n=8)
# print('TOP 8 Vokietijoje pigiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(cheapest_brands)

cheapest_brands = top_8_pigiausi_pagal_kainu_vidurki(df_pl, n=8)
# print('TOP 8 Lenkijoje pigiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(cheapest_brands)

cheapest_brands = top_8_pigiausi_pagal_kainu_vidurki(df_lt, n=8)
# print('TOP 8 Lietuvoje pigiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(cheapest_brands)

# def main2(data, n=8):
#     average_price = data.groupby('brand')['price_in_euro'].mean()
#     top_8_brands = average_price.nsmallest(n)
#     top_8_brands = top_8_brands.astype(int)
#     labels = top_8_brands.index.tolist()
#     valstybeje = input("Iveskite salies, kurios skrituline diagrama atvaiztuojate")
#     title = (f'Pigiausi automobiliu modeliai {valstybeje}')
#     stulpeline_diagrama(top_8_brands,labels,title)
#
#     if __name__ == '__main__':
#         main2(df_de)
# Vokietija = main2(df_de)



# Kuro pasiskirstymas pagal salis
#kad kiekviena salis turetu savo stulpeli, pridedame:
df_de['Country'] = 'Germany'
df_pl['Country'] = 'Poland'
df_lt ['Country'] = 'Lithuania'

#sujungiu stulpelius i viena lentele: kuro tipas ir valstybe,
merged_by_fuel = pd.concat(
    [df_de[['fuel_type', 'Country']],
     df_pl[['fuel_type', 'Country']], df_lt[['fuel_type', 'Country']]], axis=0) #axis=0 jungia vert.(hor- axis=1)

#grupuojame sujungtoje lenteleje ir skaiciuojame pasikartojimus
grouped = merged_by_fuel.groupby(['Country', 'fuel_type']).size()
#skaiciuojame bendra skaiciu kiekvienos salies
total_counts = grouped.groupby(level=0).sum()
#kadangi duomenu skaicius skiriasi, susiskaiciuojame procentaliai
percentage=grouped/total_counts*100
#susikuriame nauja datframe, kur saugosime rezultatus
rezultatai_procentais = pd.DataFrame({'Percentage': percentage}).reset_index()

#apsirasome, kokios konkreciai salys ieina i country stulpeli
filtered_data=rezultatai_procentais[rezultatai_procentais['Country'].isin(['Germany', 'Poland', 'Lithuania'])]
#tu reiksmiu, kurios labai mazos, pasirenkama nerodyt
filtered_data = filtered_data[filtered_data['Percentage'] > 0.3]
grouped_data = filtered_data.pivot(index='fuel_type', columns='Country', values='Percentage')

#piesiame grafika
grouped_data.plot(kind='bar', figsize=(14, 10))

plt.xlabel(' ', fontsize=18)
plt.ylabel('Procentine dalis', fontsize=18)
plt.title('Kuro pasiskirstymas pagal salis', fontsize=24)

plt.legend(title='Country', loc='upper right')

# issaugome grafika
plt.savefig("Grafikas_kuro pasiskirstymas pagal salis")
plt.show()

#Ridos poveikis kainai
#sukuriu duomenu sujungimo funkcija
def concat_data(df_de, df_pl, df_lt, columns_to_concat, columns_to_return):
    dataframes = [df_de[columns_to_concat], df_pl[columns_to_concat], df_lt[columns_to_concat]]
    concatenated = pd.concat(dataframes, axis = 0)
    return concatenated[columns_to_return]

# result = concat_data(df_de, df_pl, df_lt,
#         ['price_in_euro', 'mileage_in_km', 'year'],['price_in_euro', 'mileage_in_km', 'year'])
# #pasaliname eilutes, kuriose truksta reiksmiu:
# result = result.dropna(subset=['mileage_in_km'])
# #
# duomenys=result.columns
# koreliacija = result.corr()
# rodikliai=['Kaina', 'Kilometrazas', 'Amzius']
# # #nedejo i viena lapa grafiko ir jo pavadinimo, sukuriau subplot
# fig, ax = plt.subplots()
# sns.heatmap(koreliacija, xticklabels=rodikliai, yticklabels=rodikliai, cmap='coolwarm')
# ax.set_title("Automobilio amziaus ir kilometrazo itaka kainai", fontsize=10)
# plt.figure(figsize=(12,8))
# plt.show()

####### Naftos kainos , Lietuvoje registrtuotu automobiliu dinamika
def load_data(file_path):     #reikia nurodyti file path, kuri mes ikelsime
    data = pd.read_csv(file_path, delimiter =';', encoding="utf-8")
    return data

naftos_kainos=load_data('naftos kainos.csv')
#sutvarkome duomenis
naftos_kainos['date'] = pd.to_datetime(naftos_kainos['date'], format='%m/%d/%y')
naftos_kainos['oil']=naftos_kainos['oil'].str.replace(",",".")
#neteisingai braize grafika, reikia patikrinti, koks 'oil' stulpelio duomenu tipas
naftos_kainos['oil']=naftos_kainos['oil'].astype(float).round(2)
#kad diagramoje nustatyti tikslesnius rezius, noriu suzinoti max ir min kainu reiksmes.
max_kaina = np.amax(naftos_kainos['oil'])
min_kaina = np.amin(naftos_kainos['oil'])
#kad atrodytu tvarkingai, sukuriu intervalus
interval = 20

max_limit = np.ceil(max_kaina/interval) * interval
min_limit = np.floor(min_kaina/interval) * interval

#breziame diagrama
plt.plot(naftos_kainos['date'], naftos_kainos['oil'], linestyle='-', marker='o')
plt.xlabel('Laikotarpis')
plt.ylabel('Naftos kaina uz bareli')
plt.title('Naftos kainos uz bareli kitimo grafikas')
plt.xticks(rotation=45)
plt.ylim(min_limit, max_limit)
plt.yticks(np.arange(min_limit, max_limit + interval, interval))
#plt.show()

#####Automobiliu pagal kuro tipa registravimo statistika Lietuvoje
#atsidarome pries tai is xlx failiuku sudaryta faila (atskirame python file nuskaiciau 5 xlsx failus,
#konvertavau juos i csv ir sujungiau i viena csv.

regitros_data = pd.read_csv('Auto registered in 2018-2023.csv')
#issifiltruojame kad dirbsime su Naujais automobiliai

# nauji_auto = regitros_data[regitros_data['Naudota_nauja'] == 'Nauja']
# kadangi yra daug stulpeliu, juos apsirasau kaip columns
# columns = ['2018_01', '2018_02', '2018_03', '2018_04', '2018_05', '2018_06','2018_07', '2018_08', '2018_09', '2018_10',
#         '2018_11', '2018_12', '2019_01', '2019_02', '2019_03', '2019_04', '2019_05', '2019_06', '2019_07', '2019_08',
#         '2019_09', '2019_10', '2019_11', '2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06',
#         '2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02', '2021_03', '2021_04',
#         '2021_05', '2021_06', '2021_07', '2021_08', '2021_09', '2021_10', '2021_11', '2021_12','2022_01', '2022_02',
#         '2022_03', '2022_04', '2022_05', '2022_06', '2022_07', '2022_08', '2022_09', '2022_10', '2022_11', '2022_12',
#         '2023_01', '2023_02', '2023_03', '2023_04', '2023_05', '2023_06']
#
# selected_data=nauji_auto[['Degalu_rusis'] + columns]
#priskiriame nauja index(unikalus idet.),inpl = True uztikrina kad pokyciai bus atliekami dataframe selected_data
# selected_data.set_index('Degalu_rusis', inplace=True)
# paverciame lentele
# transposed_data=selected_data.transpose()
# transposed_data.plot(kind='line', figsize=(10,6))
# plt.xlabel('Laikotarpis')
# plt.ylabel('Registruoti automobiliai')
# plt.title('Lietuvoje registruotu NAUJU automobiliu dinamika pagal kuro tipa')

#plt.show()
#pakartojame viska su naudotais automobiliais
naudoti_auto = regitros_data[regitros_data['Naudota_nauja'] == 'Naudota']
columns = ['2018_01', '2018_02', '2018_03', '2018_04', '2018_05', '2018_06','2018_07', '2018_08', '2018_09', '2018_10',
        '2018_11', '2018_12', '2019_01', '2019_02', '2019_03', '2019_04', '2019_05', '2019_06', '2019_07', '2019_08',
        '2019_09', '2019_10', '2019_11', '2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06',
        '2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02', '2021_03', '2021_04',
        '2021_05', '2021_06', '2021_07', '2021_08', '2021_09', '2021_10', '2021_11', '2021_12','2022_01', '2022_02',
        '2022_03', '2022_04', '2022_05', '2022_06', '2022_07', '2022_08', '2022_09', '2022_10', '2022_11', '2022_12',
        '2023_01', '2023_02', '2023_03', '2023_04', '2023_05', '2023_06']

selected_data=naudoti_auto[['Degalu_rusis'] + columns]

selected_data.set_index('Degalu_rusis', inplace=True)
transposed_data=selected_data.transpose()

transposed_data.plot(kind='line', figsize=(10,6))
plt.xlabel('Laikotarpis')
plt.ylabel('Registruoti automobiliai')
plt.title('Lietuvoje registruotu NAUDOTU automobiliu dinamika pagal kuro tipa')
plt.legend(title='Degalu tipas')
plt.show()

#Ar egzistuoja rysys tarp naftos kainos uz bareli ir Lietuviu vartotoju iprociai renkatis automobilio kuro tipa:
#naudoju is anksciau sutvarkytus duomenis
#p.s Lygiagreciai buvo padaryti grafikai su NAUJAIS ir NAUDOTAIS automobiliais
#kad sulyginti naftos duomenu kainas su auto registro datomis, nustatau, kad filtruotu nuo 2018-01-01

naftos_kainos_filtered = naftos_kainos[naftos_kainos['date'] >='2018-01-01']
#apsirasau, kad bus du grafikai
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

#1  grafiko duomenys
ax1.plot(naftos_kainos_filtered['date'], naftos_kainos_filtered['oil'], linestyle='-', marker='o')
ax1.set_xlabel('Laikotarpis')
ax1.set_ylabel('Naftos kaina uz bareli')
ax1.set_title('Naftos kainos uz bareli kitimo grafikas')
#kad sutvarkyti datas, panaudoju mdates
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
#2 grafiko duomenys
transposed_data.plot(kind='line', ax=ax2, figsize=(10, 6))
ax2.set_xlabel('Laikotarpis')
ax2.set_ylabel('Registruoti automobiliai')
ax2.set_title('Lietuvoje registruotu NAUDOTU automobiliu dinamika pagal kuro tipa')
#neuzteko nuro dyti loc='upper right', naudojame bbox_to_anchor(x,y)
ax2.legend(title='Degalu tipas', loc='upper right', bbox_to_anchor=(1.2, 1.08))
#nustatomas tarpas tarp lenteliu
plt.subplots_adjust(hspace=0.5)

#plt.show()#
