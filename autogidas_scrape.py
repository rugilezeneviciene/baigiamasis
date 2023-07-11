import pandas as pd
import requests
import brotli
from bs4 import BeautifulSoup
import psycopg2
import time

def scrape_auto_listings():
    auto_listings = []
    website ={
        'url': 'https://autogidas.lt/en/skelbimai/automobiliai/?f_1%5B0%5D=&f_model_14%5B0%5D=&f_215=&f_216=&f_41=&f_42=&f_376=',
        'auto_listing_selector': 'article.list-item',
        'city': 'h3.list_h3',
        'brand_and_model': 'h2.item-title',
        'price': 'div.item-price',
        'primary_info': 'div.primary', # pirma eilute duomenu apie automobili
        'secondary_info': 'div.secondary' # antra eilute duomenu apie automobili
    }
    i = 1 # naudosim puslapiui nurodyti, is kurio gausim automobiliu sarasa
    j=0  # naudosim kaip id elementu sarasui

    while(i < 2):
        url = website['url']+'&page={}'.format(i)
        headers = {'Cookie':'autogidas_saved_searches=64aae98d828169.14473179; saved_searches_renew=64aae98d98ca19.42157507; identifier_user=f8f2d5f6a786315d4a09360daf85273f; agLANG=lt; _gcl_au=1.1.1205022756.1688922431; _pbjs_userid_consent_data=3524755945110770; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOAmAdm%2B4A2AMwBOABzCALNykAGAKzDuckAF8gA; _pcid=%7B%22browserId%22%3A%22ljvot3y7ndnnspgy%22%7D; _gid=GA1.2.803341064.1688922431; _fbp=fb.1.1688922431620.422507603; cX_G=cx%3A1wopf747108bn7t2ckjh41j30%3A3kio64e3rrrr1; PHPSESSID=eb8edce3430fa6e901a8fc642e802c8d; _dc_gtm_UA-10312437-18=1; _dc_gtm_UA-10312437-1=1; cX_P=ljvot3y7ndnnspgy; _ga_84NDZ0GZD6=GS1.1.1688936534.2.1.1688936537.57.0.0; _ga=GA1.1.454122552.1688922431; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jul+10+2023+00%3A02%3A17+GMT%2B0300+(Ryt%C5%B3+Europos+vasaros+laikas)&version=6.17.0&hosts=&consentId=b6e76af1-3287-4667-be28-3a42a6f7127e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A0&AwaitingReconsent=false','Sec-Fetch-User':'?1','Sec-Fetch-Site':'same-site','Sec-Fetch-Mode':'navigate','Sec-Fetch-Dest':'document','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua':'"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"','Authority':'en.autoplius.lt','Cache-Control':'no-cache','Connection':'keep-alive','Path':'/ads/used-cars','Scheme':'https','Accept-Language':'en-US,en;q=0.9,lt;q=0.8','Accept-Encoding':'gzip, deflate, br','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Cookie':'','Upgrade-Insecure-Requests':'1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67','Referer':'https://autoplius.lt/skelbimai/naudoti-automobiliai'}
        response = requests.get(url,headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')
        auto_elements = soup.select(website['auto_listing_selector'], limit=1000)

        for auto_element in auto_elements:
            j+=1
            make_elements = auto_element.select(website['brand_and_model'])
            makes = [make.text.strip() for make in make_elements]
            makeAndModel = '\n'.join(makes)
            makeAndModel = makeAndModel.split(' ',1)
            make = makeAndModel[0]
            model = makeAndModel[1]

            price_elements = auto_element.select(website['price'])
            prices = [price.text.strip() for price in price_elements]
            price = '\n'.join(prices)
            price = ''.join(c for c in price if c.isdigit())



            primary_elements = auto_element.select(website['primary_info'])
            elements = [element.text.strip() for element in primary_elements]
            primary_element = '\n'.join(elements)
            primary_parameters = primary_element.split(',')
            while(len(primary_parameters)< 5):
                primary_parameters.append(None)
            if(primary_parameters[1]):
                primary_parameters[1] = primary_parameters[1].strip()
            primary_parameters[2] = ''.join(c for c in primary_parameters[2] if c.isdigit())
            if(primary_parameters[3]):
                primary_parameters[3] = primary_parameters[3].strip()
            if(primary_parameters[4]):
                primary_parameters[4] = ''.join(c for c in primary_parameters[4] if c.isdigit())

            secondary_elements = auto_element.select(website['secondary_info'])
            elements = [element.text.strip() for element in secondary_elements]
            secondary_element = '\n'.join(elements)
            secondary_parameters = secondary_element.split(',',2)
            while(len(secondary_parameters)< 3):
                secondary_parameters.append(None)
            if(secondary_parameters[0].find('km') == -1):
                temp1 = secondary_parameters[0]
                temp2 = secondary_parameters[1]
                temp3 = secondary_parameters[2]
                secondary_parameters[0] = temp3
                secondary_parameters[1] = temp1
                secondary_parameters[2] = temp2
            else:
                secondary_parameters[0] = ''.join(c for c in secondary_parameters[0] if c.isdigit())
            
            auto_listings.append({
                'id': j,
                'brand': make,
                'model': model,
                'year': primary_parameters[2],
                'transmission_type': primary_parameters[3],
                'mileage_in_km': secondary_parameters[0],
                'fuel_type': primary_parameters[1],
                'price_in_euro': price,
            })
        i+=1
    time.sleep(10) # palaukia 10 sekundziu, kad nenumustu skelbimu portalo
    return auto_listings

auto_listings = scrape_auto_listings()
df = pd.DataFrame(auto_listings)
df['price_in_euro'] = df['price_in_euro'].astype(int)
df['mileage_in_km'] = df['mileage_in_km'].astype(float)
df.to_csv('auto_listings.csv', index=False)


# print('Data successfully scraped and saved to "auto_listings.csv".')

db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'autogidas',
    'user': 'postgres',
    'password': 'a'
}

def create_table():
    connection = psycopg2.connect(**db_params)
    create_table_query = """
        CREATE TABLE IF NOT EXISTS autogidas_market (
        id SERIAL PRIMARY KEY,
        brand VARCHAR(50),
        model VARCHAR(50),
        year VARCHAR(10),
        transmission_type VARCHAR(50),
        mileage_in_km FLOAT,
        fuel_type VARCHAR(50), 
        price_in_euro INT
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
        INSERT INTO autogidas_market (brand, model, year, transmission_type, mileage_in_km, 
        fuel_type, price_in_euro)
        VALUES ('{row['brand']}','{row['model']}','{row['year']}','{row['transmission_type']}','{row['mileage_in_km']}',
        '{row['fuel_type']}','{row['price_in_euro']}')
        """
        cursor.execute(insert_data_into_table)
        connection.commit()
    cursor.close()
    connection.close()
insert_data()