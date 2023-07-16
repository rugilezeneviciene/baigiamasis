import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('naftos kainos.csv', delimiter=';')
df = pd.DataFrame(data)

print(df.dtypes)
df['date'] = pd.to_datetime(df['date'])
df['oil']=df['oil'].str.replace(",",".")
df['oil']= df['oil'].astype(float).round(2)

naftos_kaina = np.array(df['oil'])
data = np.array(df['date'].astype('int64'))
kainos_kaita = (naftos_kaina[1:] - naftos_kaina[:-1])/naftos_kaina[:-1]*100
print(kainos_kaita)

plt.plot(data[1:], kainos_kaita, marker='o', color='brown')
plt.xlabel('Data')
plt.ylabel('Pokytis')
plt.title('Naftos kainos uz bareli kaita')
tendencija = np.polyfit(data[1:], kainos_kaita, 1)

prognoze = np.polyval(tendencija, data[1:])

plt.plot(data[1:], prognoze, color='red', label='prognoze')
plt.legend()
plt.savefig('naftos_kainos_pokyciai.png')
plt.show()
