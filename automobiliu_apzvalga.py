import pandas as pd
import requests
import brotli
from bs4 import BeautifulSoup
import psycopg2
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates


# # Surenkami duomenys iš autogidas.lt portalo
# def scrape_auto_listings():
#     auto_listings = [] #Sukuriamas tuščias sąrašas
#     website ={
#         'url': 'https://autogidas.lt/en/skelbimai/automobiliai/?f_1%5B0%5D=&f_model_14%5B0%5D=&f_215=&f_216=&f_41=&f_42=&f_376=',
#         'auto_listing_selector': 'article.list-item',
#         'city': 'h3.list_h3',
#         'brand_and_model': 'h2.item-title',
#         'price': 'div.item-price',
#         'primary_info': 'div.primary', # Pirma duomenų eilutė apie automobilį
#         'secondary_info': 'div.secondary' # Antra duomenų eilutė apie automobilį
#     }
#     i = 1 # Nurodyti puslapiui, nuo kurio gausim automobilių sąrašą
#     j=0  # Naudojamas kaip id elementų sąrašui

#     while(i < 102):   # Viena ciklo interacija lygi duomenų iš vieno puslapio ištraukimui
#         url = website['url']+'&page={}'.format(i)
#         headers = {'Cookie':'autogidas_saved_searches=64aae98d828169.14473179; saved_searches_renew=64aae98d98ca19.42157507; identifier_user=f8f2d5f6a786315d4a09360daf85273f; agLANG=lt; _gcl_au=1.1.1205022756.1688922431; _pbjs_userid_consent_data=3524755945110770; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOAmAdm%2B4A2AMwBOABzCALNykAGAKzDuckAF8gA; _pcid=%7B%22browserId%22%3A%22ljvot3y7ndnnspgy%22%7D; _gid=GA1.2.803341064.1688922431; _fbp=fb.1.1688922431620.422507603; cX_G=cx%3A1wopf747108bn7t2ckjh41j30%3A3kio64e3rrrr1; PHPSESSID=eb8edce3430fa6e901a8fc642e802c8d; _dc_gtm_UA-10312437-18=1; _dc_gtm_UA-10312437-1=1; cX_P=ljvot3y7ndnnspgy; _ga_84NDZ0GZD6=GS1.1.1688936534.2.1.1688936537.57.0.0; _ga=GA1.1.454122552.1688922431; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jul+10+2023+00%3A02%3A17+GMT%2B0300+(Ryt%C5%B3+Europos+vasaros+laikas)&version=6.17.0&hosts=&consentId=b6e76af1-3287-4667-be28-3a42a6f7127e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A0&AwaitingReconsent=false','Sec-Fetch-User':'?1','Sec-Fetch-Site':'same-site','Sec-Fetch-Mode':'navigate','Sec-Fetch-Dest':'document','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua':'"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"','Authority':'en.autoplius.lt','Cache-Control':'no-cache','Connection':'keep-alive','Path':'/ads/used-cars','Scheme':'https','Accept-Language':'en-US,en;q=0.9,lt;q=0.8','Accept-Encoding':'gzip, deflate, br','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Cookie':'','Upgrade-Insecure-Requests':'1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67','Referer':'https://autoplius.lt/skelbimai/naudoti-automobiliai'}
#         response = requests.get(url,headers=headers)

#         soup = BeautifulSoup(response.content, 'html.parser')
#         auto_elements = soup.select(website['auto_listing_selector'], limit=1000)

#         for auto_element in auto_elements: # Einama per skelbimų korteles ir surenkami duomenys
#             j+=1
#             make_elements = auto_element.select(website['brand_and_model'])
#             makes = [make.text.strip() for make in make_elements]
#             makeAndModel = '\n'.join(makes)
#             makeAndModel = makeAndModel.split(' ',1)
#             make = makeAndModel[0]
#             model = makeAndModel[1].replace("'",'')
              
              # # Imami kainų duomenys ir konvertuojami į skaičius
#             price_elements = auto_element.select(website['price'])
#             prices = [price.text.strip() for price in price_elements]
#             price = '\n'.join(prices)
#             price = ''.join(c for c in price if c.isdigit()) 

              # # Imama informacija iš dviejų eilučių ir skaidoma per kablelį
#             primary_elements = auto_element.select(website['primary_info'])
#             elements = [element.text.strip() for element in primary_elements]
#             primary_element = '\n'.join(elements)
#             primary_parameters = primary_element.split(',')
#             while(len(primary_parameters)< 5):
#                 primary_parameters.append(None)
#             if(primary_parameters[1]):
#                 primary_parameters[1] = primary_parameters[1].strip()
#             primary_parameters[2] = ''.join(c for c in primary_parameters[2] if c.isdigit())
#             if(primary_parameters[3]):
#                 primary_parameters[3] = primary_parameters[3].strip()
#             if(primary_parameters[4]):
#                 primary_parameters[4] = ''.join(c for c in primary_parameters[4] if c.isdigit())

#             secondary_elements = auto_element.select(website['secondary_info'])
#             elements = [element.text.strip() for element in secondary_elements]
#             secondary_element = '\n'.join(elements)
#             secondary_parameters = secondary_element.split(',',2)
#             while(len(secondary_parameters)< 3):
#                 secondary_parameters.append(None)
#             if(secondary_parameters[0].find('km') == -1):
#                 temp1 = secondary_parameters[0]
#                 temp2 = secondary_parameters[1]
#                 temp3 = secondary_parameters[2]
#                 secondary_parameters[0] = temp3
#                 secondary_parameters[1] = temp1
#                 secondary_parameters[2] = temp2
# #             else:
# #                 secondary_parameters[0] = ''.join(c for c in secondary_parameters[0] if c.isdigit())
            
#             auto_listings.append({
#                 'id': j,
#                 'brand': make,
#                 'model': model,
#                 'year': primary_parameters[2],
#                 'transmission_type': primary_parameters[3],
#                 'mileage_in_km': secondary_parameters[0],
#                 'fuel_type': primary_parameters[1],
#                 'price_in_euro': price,
#             })
# # #         i+=1
# # #     time.sleep(10) # Palaukia 10 sekundžių, kad nebūtų užblokuotas skelbimų portalo
# # #     return auto_listings

# # # auto_listings = scrape_auto_listings()
# # df = pd.DataFrame(auto_listings)
# # # Kainos duomenų pakeitimas i int
# # df['price_in_euro'] = df['price_in_euro'].astype(int)
# # # Kilometrų pakeitimas į skaičių su kableliu
# # df['mileage_in_km'] = df['mileage_in_km'].astype(float)
# # # Sukuriamas csv failas, kuriame bus išsaugoti scrapped data
# # df.to_csv('auto_listings7.csv', index=False)


# # # # print('Data successfully scraped and saved to "auto_listings.csv".')

# # # Sukuriama duomenų bazė
# # # db_params = {
# # #     'host': 'localhost',
# # #     'port': 5432,
# # #     'database': 'autogidas',
# # #     'user': 'postgres',
# # #     'password': 'a'
# # # }

# # # Sukuriama f-ja sukurti lentelei
# # def create_table():
# # # Prisijungiame prie duomenų bazės
# #     connection = psycopg2.connect(**db_params)
# #     create_table_query = """
# #         CREATE TABLE IF NOT EXISTS autogidas_market (
# #         id SERIAL PRIMARY KEY,
# #         brand VARCHAR(50),
# #         model VARCHAR(50),
# #         year INT,
# #         transmission_type VARCHAR(50),
# #         mileage_in_km FLOAT,
# #         fuel_type VARCHAR(50), 
# #         price_in_euro INT
# #         )
# # #         """
# #     cursor = connection.cursor()
# #     cursor.execute(create_table_query)
# #     connection.commit()
# #     cursor.close()
# #     connection.close()

# # create_table()
# # # F-ja duomenims į duomenų bazės lentelę įrašyti
# # def insert_data():
# #     connection = psycopg2.connect(**db_params)  
# #     cursor = connection.cursor()

        # # # Įterpiami duomenys į lentelę
# #     for _, row in df.iterrows():
# #         insert_data_into_table = f"""
# #         INSERT INTO autogidas_market (brand, model, year, transmission_type, mileage_in_km, 
# #         fuel_type, price_in_euro)
# #         VALUES ('{row['brand']}','{row['model']}','{row['year']}','{row['transmission_type']}','{row['mileage_in_km']}',
# #         '{row['fuel_type']}','{row['price_in_euro']}')
# #         """
# #         cursor.execute(insert_data_into_table)
# #         connection.commit()
# #     cursor.close()
# #     connection.close()
# # insert_data()

#Rugiles apsibrezimai:df_de ( Vokietija), df_pl (Lenkija), df_lt(lietuva)
### FAILU NUSKAITYMAS IR SUTVARKYMAS
#nuskaitome faila su vokietijos duomenimis.
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
# for i in df_de.columns:
#     print('{} column has {} missing values. Data type is {}'.format(i, df_de[i].isna().sum(), df_de[i].dtype))

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

# Sukuriama f-ja suskaičiuoti automobilių amžiui skirtingose valstybėse
def calculate_age(dataframe):
    for index, value in enumerate(dataframe['year']):
        try:
            dataframe.at[index, 'year'] = int(value)
            dataframe.at[index, 'age'] = 2023 - dataframe.at[index, 'year']
        except ValueError:
            dataframe.at[index, 'year'] = None
#     #print(dataframe)
    return dataframe

# Sukuriami skirtingų valstybių duomenų DataFrame su automobilių amžiumi ir duomenimis, nuskaitytais iš csv



df_lithuania = calculate_age(pd.read_csv('auto_listings.csv'))
df_germany = calculate_age(pd.read_csv('Germany_autoscout24_2023.csv'))
df_poland = calculate_age(pd.read_csv('Polish_market_scrapped_on_2023 06 27.csv'))

# Skaičiuojamas skirtingose valstybėse parduodamų automobilių amžiaus vidurkis
avg_age_lt = df_lithuania['age'].mean()
avg_age_pl = df_germany['age'].mean()
avg_age_ger = df_poland['age'].mean()
#
#
# print(avg_age_lt)
# print(avg_age_pl)
# print(avg_age_ger)

#
# # # Nubraižomas grafikas pavaizduoti vidutinį parduodamų automobilių amžių kiekvienoje šalyje
# countries = ['Lietuva', 'Vokietija', 'Lenkija']
# average_ages = avg_age_lt, avg_age_pl, avg_age_ger
# for i, v in enumerate(average_ages):
#    plt.text(i, v, "{:.0f}".format(v), ha='center', va='bottom')
# plt.bar(countries, average_ages)
# plt.xlabel('Valstybė')
# plt.ylabel('Vidutinis amžius')
# plt.title('Vidutinis parduodamų automobilių amžius Lietuvoje, Lenkijoje ir Vokietijoje', pad=20)
# plt.show()

avg_age_lt = df_lithuania['age'].mean()
avg_age_pl = df_germany['age'].mean()
avg_age_ger = df_poland['age'].mean()
#

# Nubraižomas grafikas pavaizduoti vidutinį parduodamų automobilių amžių kiekvienoje šalyje
countries = ['Lietuva', 'Vokietija', 'Lenkija']
average_ages = avg_age_lt, avg_age_pl, avg_age_ger
for i, v in enumerate(average_ages):
   plt.text(i, v, "{:.0f}".format(v), ha='center', va='bottom')
plt.bar(countries, average_ages)
plt.xlabel('Valstybė')
plt.ylabel('Vidutinis amžius')
plt.title('Vidutinis parduodamų automobilių amžius Lietuvoje, Lenkijoje ir Vokietijoje', pad=20)
plt.show()
# plt.savefig("Grafikas_Vidutinis parduodamų automobilių amžius Lietuvoje, Lenkijoje ir Vokietijoje.png")


# Sukuriama f-ja suskaičiuoti skirtingo amžiaus parduodamų automobilių skaičių kiekvienoje valstybėje
# def vehicle_ages_graph(df,country):
#     # Pašalinami nekorektiški amžiaus duomenys
#     age = df[df['age'] >= 0]['age']
#     age_counts = age.value_counts()
#     # Paimimamas automobilių amžius
#     ages = age_counts.index
#     # Paimimamas skirtingo amžiaus automobilių skaičius
#     counts = age_counts.values
#     plt.bar(ages, counts)
#     plt.xlabel('Automobilio amžius')
#     plt.ylabel('Automobilių skaičius')
#     plt.title('Parduodamų automobilių amžius '+country)
#     plt.show()
#
# vehicle_ages_graph(df_lithuania,'Lietuvoje')
# vehicle_ages_graph(df_germany,'Vokietijoje')
# vehicle_ages_graph(df_poland,'Lenkijoje')
#
#
#

### KURIO BRANDO VIDUTINE KAINA YRA DIDZIAUSIA?


#pasirasome funkcija suskaiciuoti modelius, kuriu vidutine kaina yra didziauia
def top_8_brangiausi_pagal_kainu_vidurki(data, n=8):
    average_price = data.groupby('brand')['price_in_euro'].mean()
    top_8_brands = average_price.nlargest(n)
    top_8_brands = top_8_brands.astype(int)
    return top_8_brands
#
#funkcija pritaikome kiekvienai valstybei atskirai
# top_8_brands = top_8_brangiausi_pagal_kainu_vidurki(df_de, n=8)
# print('TOP 8 Vokietijoje brangiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(top_8_brands)
# # #
# top_8_brands = top_8_brangiausi_pagal_kainu_vidurki(df_pl, n=8)
# print('TOP 8 Lenkijoje brangiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(top_8_brands)
#
# top_8_brands = top_8_brangiausi_pagal_kainu_vidurki(df_lt, n=8)
# print('TOP 8 Lietuvoje brangiausi automobiliu modeliai pagal vidutine kaina yra: ')
# print(top_8_brands)
#
#pasirasome funkcija diagramai
# def stulpeline_diagrama (data, labels, title, filename):
#     colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta']
#     plt.figure(figsize=(10,6))
#     bars = plt.bar(labels, data, color=colors)
#     plt.xlabel(' ')
#     plt.ylabel('Vidutine kaina eurais')
#     plt.title(title)
#     plt.xticks(rotation=45, ha='right')
#
#     for i, bar in enumerate(bars):
#         height = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width() / 2, height, round(data[i], 2), ha='center', va='bottom')
#
#     plt.tight_layout()
#     #plt.savefig(filename)
#     plt.show()
# def main(data, n=8):
#     average_price = data.groupby('brand')['price_in_euro'].mean()
#     top_8_brands = average_price.nlargest(n)
#     top_8_brands = top_8_brands.astype(int)
#     labels = top_8_brands.index.tolist()
#     valstybeje = input("Iveskite salies, kurios stulpeline diagrama atvaiztuojate")
#     title = (f'TOP 8 Automobiliu modeliai pagal auksciausia vidutine kaina {valstybeje}')
#     filename = f'Grafikas_TOP 8 modeliai pagal auksciausia vidutine kaina {valstybeje}'
#     stulpeline_diagrama(top_8_brands,labels,title, filename)
#
#     if __name__ == '__main__':
#         main(df_de)
# #paleidziame funkcija, ir norint pakeisti Title, priklausmai nuo to, kurios salies lentele rodome,
# #input irasome pvz.Vokietijoje
# Vokietija = main(df_de)
#
# #pasirasome funkcija suskaiciuoti modelius, kuriu vidutine kaina yra maziausia:
# def top_8_pigiausi_pagal_kainu_vidurki(data, n=8):
#     average_price = data.groupby('brand')['price_in_euro'].mean()
#     The_cheapest_8_brands = average_price.nsmallest(n)
#     return The_cheapest_8_brands

# cheapest_brands = top_8_pigiausi_pagal_kainu_vidurki(df_de, n=8)
# # print('TOP 8 Vokietijoje pigiausi automobiliu modeliai pagal vidutine kaina yra: ')
# # print(cheapest_brands)
#
# cheapest_brands = top_8_pigiausi_pagal_kainu_vidurki(df_pl, n=8)
# # print('TOP 8 Lenkijoje pigiausi automobiliu modeliai pagal vidutine kaina yra: ')
# # print(cheapest_brands)
#
# cheapest_brands = top_8_pigiausi_pagal_kainu_vidurki(df_lt, n=8)
# # print('TOP 8 Lietuvoje pigiausi automobiliu modeliai pagal vidutine kaina yra: ')
# # print(cheapest_brands)

# def main2(data, n=8):
#     average_price = data.groupby('brand')['price_in_euro'].mean()
#     top_8_brands = average_price.nsmallest(n)
#     top_8_brands = top_8_brands.astype(int)
#     labels = top_8_brands.index.tolist()
#     valstybeje = input("Iveskite salies, kurios stulpeline diagrama atvaizduojate")
#     filename = f'Grafikas_8 pigiausi automobiliai pagal vidutine kaina {valstybeje}'
#     title = (f'Pigiausi automobiliu modeliai {valstybeje}')
#     stulpeline_diagrama(top_8_brands,labels,title, filename)
#
#     if __name__ == '__main__':
#         main2(df_lt)
# Vokietija = main2(df_lt)

###  KURO PASISKIRSTYMAS PAGAL SALIS ###
#kad kiekviena salis turetu savo stulpeli, pridedame:
# df_de['Country'] = 'Germany'
# df_pl['Country'] = 'Poland'
# df_lt ['Country'] = 'Lithuania'
# #
# # #sujungiu stulpelius i viena lentele: kuro tipas ir valstybe,
# merged_by_fuel = pd.concat(
#     [df_de[['fuel_type', 'Country']],
#      df_pl[['fuel_type', 'Country']], df_lt[['fuel_type', 'Country']]], axis=0) #axis=0 jungia vert.(hor- axis=1)
# #
# # #grupuojame sujungtoje lenteleje ir skaiciuojame pasikartojimus
# grouped = merged_by_fuel.groupby(['Country', 'fuel_type']).size()
# #skaiciuojame bendra skaiciu kiekvienos salies
# total_counts = grouped.groupby(level=0).sum()
# #kadangi duomenu skaicius skiriasi, susiskaiciuojame procentaliai
# percentage=grouped/total_counts*100
# #susikuriame nauja datframe, kur saugosime rezultatus
# rezultatai_procentais = pd.DataFrame({'Percentage': percentage}).reset_index()
#
# #apsirasome, kokios konkreciai salys ieina i country stulpeli
# filtered_data=rezultatai_procentais[rezultatai_procentais['Country'].isin(['Germany', 'Poland', 'Lithuania'])]
# #tu reiksmiu, kurios labai mazos, pasirenkama nerodyt
# filtered_data = filtered_data[filtered_data['Percentage'] > 0.3]
# grouped_data = filtered_data.pivot(index='fuel_type', columns='Country', values='Percentage')
#
# #piesiame grafika
# grouped_data.plot(kind='bar', figsize=(14, 10))
#
# plt.xlabel(' ', fontsize=18)
# plt.ylabel('Procentine dalis', fontsize=18)
# plt.title('Kuro pasiskirstymas pagal salis', fontsize=24)
#
# plt.legend(title='Country', loc='upper right')
#
# # issaugome grafika
# #plt.savefig("Grafikas: kuro pasiskirstymas pagal salis")
# plt.show()
# #


### PAVARU DEZES (AUTOMATINE/MECHANINE) PASISKIRSTYMAS PAGAL SALIS ###

# Sukuriama f-ja pakeisti pavadinimus iš EN į LT
# Jei PL, naudojamas kitas pavadinimas
# def change_en_to_lt(df, salis, isPL=False):
#     transmission_column = 'transmission_type'
#     transmission_column = 'transmission_type'
#     if(isPL):
#         df[transmission_column] = df['gearbox']
#     for index, value in enumerate(df[transmission_column]):
#         df.at[index, 'country'] = salis
#         if(value.lower().strip() == 'automatic'): # Konvetuojama į  mažąsias raides
#             df.at[index, transmission_column] = 'Automatinė'
#         elif(value.lower().strip() == 'manual' or value.lower().strip() == 'mechanical'):
#             df.at[index, transmission_column] = 'Mechaninė'
#         elif(value.lower().strip() == 'semi-automatic'):
#             df.at[index, transmission_column] = 'Pusiau automatinė'
#         else:
#             df.at[index, transmission_column] = 'Kita'
#     return df
#
# # Sutvarkomi pavarų dėžių duomenys pašalinant nekorektiškas reikšmes (Kita)
# df_lithuania_in_lt = change_en_to_lt(df_lithuania,'Lietuva')
# df_lithuania_in_lt= df_lithuania_in_lt[df_lithuania_in_lt['transmission_type'] != 'Kita']
# df_poland_in_lt = change_en_to_lt(df_poland,'Lenkija',True)
# df_poland_in_lt=df_poland_in_lt[df_poland_in_lt['transmission_type'] != 'Kita']
# df_germany_in_lt = change_en_to_lt(df_germany,'Vokietija')
# df_germany_in_lt=df_germany_in_lt[df_germany_in_lt['transmission_type'] != 'Kita']
#
#
# # # Suskaičiuojamas skirtingų pavarų dėžių automobilių skaičius kiekvienoje valstybėje
# transmission_type_counts_lt = df_lithuania_in_lt['transmission_type'].value_counts()
# # print(transmission_type_counts_lt)
# transmission_type_counts_pl = df_poland_in_lt['transmission_type'].value_counts()
# df_germany_in_lt= df_germany_in_lt[df_germany_in_lt['transmission_type'] != 'Unknown']
# # print(transmission_type_counts_pl)
# transmission_type_counts_ger = df_germany_in_lt['transmission_type'].value_counts()
# # print(transmission_type_counts_ger)


# # transmission_type_counts_lt.plot(kind='pie')
# # plot = transmission_type_counts_lt.plot.pie(y='', figsize=(5, 5), autopct='%1.1f%%')
# # plt.title('Automatinės ir mechaninės pavarų dėžės pasiskirstymas Lietuvoje')
# # plt.show()

# # transmission_type_counts_pl.plot(kind='pie')
# # plot = transmission_type_counts_pl.plot.pie(y='', figsize=(5, 5), autopct='%1.1f%%')
# # plt.title('Automatinės ir mechaninės pavarų dėžės pasiskirstymas Lenkijoje')
# # plt.show()

# # transmission_type_counts_ger.plot(kind='pie')
# # plot = transmission_type_counts_ger.plot.pie(y='', figsize=(5, 5), autopct='%1.1f%%')
# # plt.title('Automatinės ir mechaninės pavarų dėžės pasiskirstymas Vokietijoje')
# # plt.show()

#
#
# ###      AUTOMATINĖS IR MECHANINĖS PAVARŲ DĖŽĖS PASISKIRSTYMAS       ####
#
# countries = ['Lietuva', 'Lenkija', 'Vokietija']
# # Sujungia trijų valstybių DataFrame į vieną
# testdf = pd.concat([df_germany_in_lt, df_lithuania_in_lt, df_poland_in_lt])
# # Sudaroma dviejų ašių lentelė
# cross_tab_prop = pd.crosstab(index=testdf['country'],
#                              columns=testdf['transmission_type'],
#                              normalize="index")
#
# cross_tab_prop.plot(kind='bar',
#                     # Kelios reik6m4s viename stulpelyje
#                     stacked=True,
#                     colormap='tab10',
#                     figsize=(10, 6))
# # Einama per reikšmes ir uždedamos duomenų etiketės
# for i, (x, y) in enumerate(cross_tab_prop.iterrows()):
#     # Nustatoma duomenų etiketės vieta diagramoje
#     plt.text(x=i-0.05, y=y.Automatinė/2, s=f"{round(y.Automatinė*100)}%")
#     plt.text(x=i-0.05, y=(y.Mechaninė/2)+y.Automatinė, s=f"{round(y.Mechaninė*100)}%")
# # Legendos vieta ir jos stulpelių skaičius
# plt.legend(loc="upper left", ncol=2)
# plt.xlabel("Valstybės")
# plt.ylabel("Dalis")
# plt.title('Automatinės ir mechaninės pavarų dėžės pasiskirstymas Lietuvoje, Vokietijoje ir Lenkijoje')
# plt.show()


###      RIDOS IR AMZIAUS POVEIKIS KAINAI        ####

#sukuriu duomenu sujungimo funkcija
# def concat_data(df_de, df_pl, df_lt, columns_to_concat, columns_to_return):
#     dataframes = [df_de[columns_to_concat], df_pl[columns_to_concat], df_lt[columns_to_concat]]
#     concatenated = pd.concat(dataframes, axis = 0)
#     return concatenated[columns_to_return]
#
# result = concat_data(df_de, df_pl, df_lt,
#         ['price_in_euro', 'mileage_in_km', 'year'],['price_in_euro', 'mileage_in_km', 'year'])
# #pasaliname eilutes, kuriose truksta reiksmiu:
# result = result.dropna(subset=['mileage_in_km'])
# #
# duomenys=result.columns
# koreliacija = result.corr()
# rodikliai=['Kaina', 'Kilometrazas', 'Pagaminimo metai']
# # #nedejo i viena lapa grafiko ir jo pavadinimo, sukuriau subplot
# fig, ax = plt.subplots()
# sns.heatmap(koreliacija, annot = True, fmt=".2f", cmap='coolwarm',
#             xticklabels=rodikliai, yticklabels=rodikliai,)
# ax.set_title("Automobilio pagaminimo metu ir kilometrazo itaka kainai", fontsize=10)
# plt.figure(figsize=(12,8))
# plt.savefig('Grafikas_Ridos_metu_kainos priklausomybe')
# plt.show()



#########################
# Sukuriama f-ja pavaizduoti populiauriausias markes skirtingose valstybėse
# def distribution_of_brands(df,salis):
#     # Markės sudedamos į sąrašą
#     makes = df['brand'].tolist()
#      # Suskaičiuojamos reikšmės, kiek kokių yra
#     make_counts = pd.Series(makes).value_counts()
#     top_7_car_makes = make_counts.head(7)
#       # Sumuojami kiti automobiliai, kurie nepapuola į TOP 7  ir nurodoma kaip Kita markė
#     for index, value in enumerate(df['brand']):
#         if(value not in top_7_car_makes):
#             df.at[index, 'brand'] = 'Kita'
#     makes = df['brand'].tolist()
#     make_counts = pd.Series(makes).value_counts()
#     top_8_car_makes = make_counts.head(8)
#     #  Nustatomas šrifto dydis
#     plt.rcParams['font.size'] = 8
#     plt.pie(make_counts, labels=top_8_car_makes.index, autopct='%1.1f%%', startangle=90)
#     # Nustatomas tarpas tarp grafiko antraštės ir grafiko vidinės dalies
#     plt.title("Populiariausios parduodamų automobilių markės "+salis,  pad=20) # Nustatomas tarpas tarp grafiko antraštės ir grafiko vidinės dalies
#     plt.axis('equal')
#     plt.show()
#     return df

# distribution_of_brands(df_lithuania, "Lietuvoje")
# distribution_of_brands(df_germany, "Vokietijoje")
# distribution_of_brands(df_poland, "Lenkijoje")


# # Sukuriama f-ja, išskirti ir nubraižyti diagramą ir atvaizduoti populiariausios markės populiariausius modelius valstybėse
# def distribution_of_models_in_most_popular_brand(df,salis):
#     makes = df['brand'].tolist()
#     make_counts = pd.Series(makes).value_counts()
#     top_car_make = make_counts.head(2)
#     k = 0
#     if(top_car_make.index[k] == 'Kita'):
#          k=1
#     df = df[df['brand'] == top_car_make.index[k]]
#     models = df['model'].tolist()
#     model_counts = pd.Series(models).value_counts()
#     top_7_brand_models = model_counts.head(7)
#     for index, value in enumerate(df['model']):
#         if(value not in top_7_brand_models):
#             df.at[index, 'model'] = 'Kita'
#     models = df['model'].tolist()
#     model_counts = pd.Series(models).value_counts()
#     top_8_brand_models = model_counts.head(8)
#     print(top_8_brand_models)
#     plt.rcParams['font.size'] = 8
#     plt.pie(top_8_brand_models.values, labels=top_8_brand_models.index, autopct='%1.1f%%', startangle=90)
#     plt.title("Populiariausios markės "+top_car_make.index[k]+" populiariausi modeliai "+salis,  pad=20)
#     plt.axis('equal')
#     plt.show()
#     plt.savefig("Populiariausios markės" + salis + ".png")
#     return df
# distribution_of_models_in_most_popular_brand(df_lithuania, "Lietuvoje")
# distribution_of_models_in_most_popular_brand(df_germany, "Vokietijoje")
# distribution_of_models_in_most_popular_brand(df_poland, "Lenkijoje")

### AUTOMOBILIU REGISTRAVIMO STATISTIKA, KURO ASPEKTU

def load_data(file_path):     #reikia nurodyti file path, kuri mes ikelsime
    data = pd.read_csv(file_path, delimiter =';', encoding="utf-8")
    return data

#perskaitome naftos kainu failiuka
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

# #breziame diagrama
# plt.plot(naftos_kainos['date'], naftos_kainos['oil'], linestyle='-', marker='o')
# plt.xlabel('Laikotarpis')
# plt.ylabel('Naftos kaina uz bareli')
# plt.title('Naftos kainos uz bareli kitimo grafikas')
# plt.xticks(rotation=45)
# plt.ylim(min_limit, max_limit)
# plt.yticks(np.arange(min_limit, max_limit + interval, interval))
# plt.savefig('Grafikas_Barelio kainos pokyciai')
# plt.show()

#atsidarome pries tai is xlx failiuku sudaryta faila (atskirame python file nuskaiciau 5 xlsx failus,
# #konvertavau juos i csv ir sujungiau i viena csv.
regitros_data = pd.read_csv('Auto registered in 2018-2023.csv')
# #issifiltruojame kad dirbsime su Naujais automobiliais
#
nauji_auto = regitros_data[regitros_data['Naudota_nauja'] == 'Nauja']
# #kadangi yra daug stulpeliu, juos apsirasau kaip columns
columns = ['2018_01', '2018_02', '2018_03', '2018_04', '2018_05', '2018_06','2018_07', '2018_08', '2018_09', '2018_10',
        '2018_11', '2018_12', '2019_01', '2019_02', '2019_03', '2019_04', '2019_05', '2019_06', '2019_07', '2019_08',
        '2019_09', '2019_10', '2019_11', '2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06',
        '2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02', '2021_03', '2021_04',
        '2021_05', '2021_06', '2021_07', '2021_08', '2021_09', '2021_10', '2021_11', '2021_12','2022_01', '2022_02',
        '2022_03', '2022_04', '2022_05', '2022_06', '2022_07', '2022_08', '2022_09', '2022_10', '2022_11', '2022_12',
        '2023_01', '2023_02', '2023_03', '2023_04', '2023_05', '2023_06']

selected_data=nauji_auto[['Degalu_rusis'] + columns]
#priskiriame nauja index(unikalus idet.),inpl = True uztikrina kad pokyciai bus atliekami dataframe selected_data
selected_data.set_index('Degalu_rusis', inplace=True)
#paverciame lentele
transposed_data_new=selected_data.transpose()

# # #pakartojame viska su naudotais automobiliais
# naudoti_auto = regitros_data[regitros_data['Naudota_nauja'] == 'Naudota']
# columns = ['2018_01', '2018_02', '2018_03', '2018_04', '2018_05', '2018_06','2018_07', '2018_08', '2018_09', '2018_10',
#         '2018_11', '2018_12', '2019_01', '2019_02', '2019_03', '2019_04', '2019_05', '2019_06', '2019_07', '2019_08',
#         '2019_09', '2019_10', '2019_11', '2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06',
#         '2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12', '2021_01', '2021_02', '2021_03', '2021_04',
#         '2021_05', '2021_06', '2021_07', '2021_08', '2021_09', '2021_10', '2021_11', '2021_12','2022_01', '2022_02',
#         '2022_03', '2022_04', '2022_05', '2022_06', '2022_07', '2022_08', '2022_09', '2022_10', '2022_11', '2022_12',
#         '2023_01', '2023_02', '2023_03', '2023_04', '2023_05', '2023_06']
#
# selected_data=naudoti_auto[['Degalu_rusis'] + columns]
# selected_data.set_index('Degalu_rusis', inplace=True)
# transposed_data_old=selected_data.transpose()

# # ###   AR EGZISTUOJA RYSYS TARP NAFTOS KAINOS UZ BARELI IR LIETUVIU VARTOTOJU IPROCIU RENKANTIS AUTOMOBILIO KURO TIPA:
# # #naudoju is anksciau sutvarkytus duomenis
# #
# # #p.s Lygiagreciai buvo padaryti grafikai su NAUJAIS ir NAUDOTAIS automobiliais
# # #kad sulyginti naftos duomenu kainas su auto registro datomis, nustatau, kad filtruotu nuo 2018-01-01
# #
naftos_kainos_filtered = naftos_kainos[naftos_kainos['date'] >='2018-01-01']
#apsirasau, kad bus du grafikai
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
#
#1  grafiko duomenys
ax1.plot(naftos_kainos_filtered['date'], naftos_kainos_filtered['oil'], linestyle='-', marker='o')
ax1.set_xlabel('Laikotarpis')
ax1.set_ylabel('Naftos kaina uz bareli')
ax1.set_title('Naftos kainos uz bareli kitimo grafikas')
#kad sutvarkyti datas, panaudoju mdates
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
#2 grafiko duomenys
transposed_data_new.plot(kind='line', ax=ax2, figsize=(10, 6))
ax2.set_xlabel('Laikotarpis')
ax2.set_ylabel('Registruoti automobiliai')
ax2.set_title('Lietuvoje registruotu NAUJU automobiliu dinamika pagal kuro tipa')

#neuzteko nurodyti loc='upper right', naudojame bbox_to_anchor(x,y)
ax2.legend(title='Degalu tipas', loc='upper right', bbox_to_anchor=(1.2, 1.08))
#nustatomas tarpas tarp lenteliu
plt.subplots_adjust(hspace=0.5)
plt.savefig('Grafikas_Nauji_auto ir barelio kainos')
plt.show()#

###  PROGNOZAVIMAS. Kokia automobiilio kaina, ivedus ridos, markes, metu reiksmes.

#ruosiame duomenis treniravimui
# X = df_de[['year', 'model', 'mileage_in_km']]
# y = df_de['price_in_euro']
# X_encoded = pd.get_dummies(X)

# #daliname duomenis i treniravimo rinkinius
# #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# #treniruojame tiesines regresijos modeli
# model = LinearRegression()
# model.fit(X_encoded, y)

# #darome spejimus testavimo rinkinyje
# y_pred = model.predict(X_encoded)
# #skaiciuojame nuokrypi
# nuokrypis = mean_squared_error(y, y_pred, squared=False)
# print('Vidutinis kvadratinis nuokrypis: ', nuokrypis)
#

# while True:
#     Metai = int(input("Iveskite automobilio pagaminimo metus:  "))
#     if str(Metai).lower() == 'exit':
#         break
#
#     Modelis = input("Iveskite automobilio modeli:  ")
#     Rida = int(input("Iveskite maksimalia automobilio rida, skaiciais   "))
#

#     Modelis = input("Iveskite automobilio modeli:  ")
#     Rida = int(input("Iveskite maksimalia automobilio rida, skaiciais   "))

#     new_data=pd.DataFrame({'year': [Metai], 'brand':[Modelis], 'mileage_in_km':[Rida]})
#     new_data_encoded = pd.get_dummies(new_data)
#     #uztikrinimui, kad new_data turi tuos pacius stulpelius kaip ir train data
#     missing_cols = set(X_encoded.columns) - set(new_data_encoded.columns)
#     for col in missing_cols:
#         new_data_encoded[col] = 0
#     #perrikiuojame stulpelius, kad atitiktu tuos pacius stulpelius per treniravima
#     new_data_encoded = new_data_encoded[X_encoded.columns]
#
#     prediction = model.predict(new_data_encoded)
#     print('Predicted price:', prediction)

#     prediction = model.predict(new_data_encoded)
#     print('Predicted price:', prediction)


