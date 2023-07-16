import pandas as pd
import requests
import brotli
from bs4 import BeautifulSoup
import psycopg2
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

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
# # #     time.sleep(10) # palaukia 10 sekundziu, kad nebutu uzblokuotas skelbimu portalo
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

print(avg_age_lt)
print(avg_age_pl)
print(avg_age_ger)

# # Nubraižomas grafikas pavaizduoti vidutinį parduodamų automobilių amžių kiekvienoje šalyje
countries = ['Lietuva', 'Vokietija', 'Lenkija']
average_ages = avg_age_lt, avg_age_pl, avg_age_ger
for i, v in enumerate(average_ages):
   plt.text(i, v, "{:.0f}".format(v), ha='center', va='bottom')
plt.bar(countries, average_ages)
plt.xlabel('Valstybė')
plt.ylabel('Vidutinis amžius')
plt.title('Vidutinis parduodamų automobilių amžius Lietuvoje, Lenkijoje ir Vokietijoje', pad=20)
plt.show()


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
#     plt.ylabel('Automobilio skaičius')
#     plt.title('Parduodamų automobilių amžius '+country)
#     plt.show()

# vehicle_ages_graph(df_lithuania,'Lietuvoje')
# vehicle_ages_graph(df_germany,'Vokietijoje')
# vehicle_ages_graph(df_poland,'Lenkijoje')

# Sukuriama f-ja pakeisti pavadinimus iš EN į LT
# Jei PL, naudojamas kitas pavadinimas
def change_en_to_lt(df, salis, isPL=False):
    transmission_column = 'transmission_type'
    transmission_column = 'transmission_type'
    if(isPL):
        df[transmission_column] = df['gearbox']
    for index, value in enumerate(df[transmission_column]):
        df.at[index, 'country'] = salis
        if(value.lower().strip() == 'automatic'): # Konvetuojama į  mažąsias raides
            df.at[index, transmission_column] = 'Automatinė'
        elif(value.lower().strip() == 'manual' or value.lower().strip() == 'mechanical'):
            df.at[index, transmission_column] = 'Mechaninė'
        elif(value.lower().strip() == 'semi-automatic'):
            df.at[index, transmission_column] = 'Pusiau automatinė'
        else:
            df.at[index, transmission_column] = 'Kita'
    return df
# Sutvarkomi pavarų dėžių duomenys pašalinant nekorektiškas reikšmes (Kita)
df_lithuania_in_lt = change_en_to_lt(df_lithuania,'Lietuva')
df_lithuania_in_lt= df_lithuania_in_lt[df_lithuania_in_lt['transmission_type'] != 'Kita']
df_poland_in_lt = change_en_to_lt(df_poland,'Lenkija',True)
df_poland_in_lt=df_poland_in_lt[df_poland_in_lt['transmission_type'] != 'Kita']
df_germany_in_lt = change_en_to_lt(df_germany,'Vokietija')
df_germany_in_lt=df_germany_in_lt[df_germany_in_lt['transmission_type'] != 'Kita']


# # Suskaičiuojamas skirtingų pavarų dėžių automobilių skaičius kiekvienoje valstybėje
transmission_type_counts_lt = df_lithuania_in_lt['transmission_type'].value_counts()
# print(transmission_type_counts_lt)
transmission_type_counts_pl = df_poland_in_lt['transmission_type'].value_counts()
df_germany_in_lt= df_germany_in_lt[df_germany_in_lt['transmission_type'] != 'Unknown']
# print(transmission_type_counts_pl)
transmission_type_counts_ger = df_germany_in_lt['transmission_type'].value_counts()
# print(transmission_type_counts_ger)



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

countries = ['Lietuva', 'Lenkija', 'Vokietija']
# Sujungia trijų valstybių DataFrame į vieną
testdf = pd.concat([df_germany_in_lt, df_lithuania_in_lt, df_poland_in_lt])
# Sudaroma dviejų ašių lentelė
cross_tab_prop = pd.crosstab(index=testdf['country'],
                             columns=testdf['transmission_type'],
                             normalize="index")

cross_tab_prop.plot(kind='bar',
                    # Kelios reik6m4s viename stulpelyje
                    stacked=True,
                    colormap='tab10',
                    figsize=(10, 6))
# Einama per reikšmes ir uždedamos duomenų etiketės
for i, (x, y) in enumerate(cross_tab_prop.iterrows()):
    # Nustatoma duomenų etiketės vieta diagramoje
    plt.text(x=i-0.05, y=y.Automatinė/2, s=f"{round(y.Automatinė*100)}%")
    plt.text(x=i-0.05, y=(y.Mechaninė/2)+y.Automatinė, s=f"{round(y.Mechaninė*100)}%")
# Legendos vieta ir jos stulplių skaičius
plt.legend(loc="upper left", ncol=2)
plt.xlabel("Valstybės")
plt.ylabel("Dalis")
plt.show()

#########################
# # Surkuriama f-ja pavaizduoti populiauriausias markes skirtingose valstyb4se
# def distribution_of_brands(df,salis):
      # Markės sudedamos į sąrašą
#     makes = df['brand'].tolist() 
      # Suskaičiuojamos reikšmės, kiek kokių yra
#     make_counts = pd.Series(makes).value_counts()
#     top_7_car_makes = make_counts.head(7)
      # Sumuojami kiti automobiliai, kurie nepapuola į TOP 7  ir nurodoma kaip Kita markė
#     for index, value in enumerate(df['brand']):
#         if(value not in top_7_car_makes): 
#             df.at[index, 'brand'] = 'Kita'
#     makes = df['brand'].tolist()
#     make_counts = pd.Series(makes).value_counts()
#     top_8_car_makes = make_counts.head(8)
      # Nustatomas šrifto dydis 
#     plt.rcParams['font.size'] = 8 
#     plt.pie(make_counts, labels=top_8_car_makes.index, autopct='%1.1f%%', startangle=90)
      # Nustatomas tarpas tarp grafiko antraštės ir grafiko vidinės dalies
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
#     top_car_make = make_counts.head(1)
#     df = df[df['brand'] == top_car_make.index[0]]
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
#     plt.title("Populiariausios markės "+top_car_make.index[0]+" populiariausi modeliai "+salis,  pad=20)
#     plt.axis('equal')
#     plt.show()
#     return df

# distribution_of_models_in_most_popular_brand(df_lithuania, "Lietuvoje")
# distribution_of_models_in_most_popular_brand(df_germany, "Vokietijoje")
# distribution_of_models_in_most_popular_brand(df_poland, "Lenkijoje")