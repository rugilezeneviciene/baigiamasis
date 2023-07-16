import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df = pd.read_csv('Germany_autoscout24_2023.csv')
ind = df.columns[0]
orignal_df = df

#sutvarkome fuel_type stulpeli.

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
df['brand'] = df['brand'].astype(str)
#cia kad rodytu visus stulpelius
pd.options.display.max_columns = None

# for i in df.columns:
#     print('{} column has {} missing values. Data type is {}'.format(i, df[i].isna().sum(), df[i].dtype))
# prooblema su KIA CEED pavadimu, bandau taisyti:
df['model'] = df['model'].str.replace("'", "")

#ruosiame duomenis treniravimui
X = df[['year', 'model', 'mileage_in_km']]
y = df['price_in_euro']
X_encoded = pd.get_dummies(X)

#daliname duomenis i treniravimo rinkinius
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#treniruojame tiesines regresijos modeli
model = LinearRegression()
model.fit(X_encoded, y)

#darome spejimus testavimo rinkinyje
y_pred = model.predict(X_encoded)
#skaiciuojame nuokrypi
nuokrypis = mean_squared_error(y, y_pred, squared=False)
print('Vidutinis kvadratinis nuokrypis: ', nuokrypis)

while True:
    Metai = int(input("Iveskite automobilio pagaminimo metus:  "))
    if str(Metai).lower() == 'exit':
        break

    Modelis = input("Iveskite automobilio modeli:  ")
    Rida = int(input("Iveskite maksimalia automobilio rida, skaiciais   "))

    new_data=pd.DataFrame({'year': [Metai], 'brand':[Modelis], 'mileage_in_km':[Rida]})
    new_data_encoded = pd.get_dummies(new_data)
    #uztikrinimui, kad new_data turi tuos pacius stulpelius kaip ir train data
    missing_cols = set(X_encoded.columns) - set(new_data_encoded.columns)
    for col in missing_cols:
        new_data_encoded[col] = 0
    #perrikiuojame stulpelius, kad atitiktu tuos pacius stulpelius per treniravima
    new_data_encoded = new_data_encoded[X_encoded.columns]

    prediction = model.predict(new_data_encoded)
    print('Predicted price:', prediction)




