import pandas as pd

#funkcija duomenu ikelimui
def load_data(file_path):     #reikia nurodyti file path, kuri mes ikelsime
    data = pd.read_csv(file_path, delimiter=';')
    return data

#funkcija duomenu isvalymui
def clean_data(data, column_names):
    data = data.dropna(how='all', axis=0)
    data = data.dropna(how='all', axis=1)
    data.columns = column_names
    data = data[2:]
    data['Degalu_rusis']=data['Degalu_rusis'].str.replace(" ","")
    return data

def main():

    file_path_2023 = '2023 auto pardavimai.csv'
    column_names_2023 = ['Naudota_nauja', 'Degalu_rusis', '2023_01', '2023_02', '2023_03','2023_04','2023_05','2023_06']
    data_2023 = load_data(file_path_2023)
    data_2023 = clean_data(data_2023, column_names_2023)


    file_path_2022 = '2022 auto pardavimai.csv'
    column_names_2022 = ['Naudota_nauja', 'Degalu_rusis', '2022_01', '2022_02', '2022_03', '2022_04', '2022_05', '2022_06',
                    '2022_07', '2022_08', '2022_09', '2022_10', '2022_11', '2022_12']
    data_2022 = load_data(file_path_2022)
    data_2022 = clean_data(data_2022, column_names_2022)


    file_path_2021 = '2021 auto pardavimai.csv'
    column_names_2021 = ['Naudota_nauja', 'Degalu_rusis', '2021_01', '2021_02', '2021_03', '2021_04', '2021_05',
                         '2021_06','2021_07', '2021_08', '2021_09', '2021_10', '2021_11', '2021_12']
    data_2021 = load_data(file_path_2021)
    data_2021 = clean_data(data_2021, column_names_2021)

    file_path_2020 = '2020 auto pardavimai.csv'
    column_names_2020 = ['Naudota_nauja', 'Degalu_rusis', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05',
                         '2020_06','2020_07', '2020_08', '2020_09', '2020_10', '2020_11', '2020_12']
    data_2020 = load_data(file_path_2020)
    data_2020 = clean_data(data_2020, column_names_2020)


    file_path_2019 = '2019 auto pardavimai.csv'
    column_names_2019 = ['Naudota_nauja', 'Degalu_rusis', '2019_01', '2019_02', '2019_03', '2019_04', '2019_05',
                         '2019_06','2019_07', '2019_08', '2019_09', '2019_10', '2019_11', '2019_12']
    data_2019 = load_data(file_path_2019)
    data_2019 = clean_data(data_2019, column_names_2019)


    file_path_2018 = '2018 auto pardavimai.csv'
    column_names_2018 = ['Naudota_nauja', 'Degalu_rusis', '2018_01', '2018_02', '2018_03', '2018_04', '2018_05',
                         '2018_06','2018_07', '2018_08', '2018_09', '2018_10', '2018_11', '2018_12']
    data_2018 = load_data(file_path_2018)
    data_2018 = clean_data(data_2018, column_names_2018)
    data_2018 = data_2018[1:]

    joined_data = pd.merge(data_2018, data_2019, on=['Naudota_nauja', 'Degalu_rusis'], how='inner' )

    joined_data2 = pd.merge(data_2020, data_2021, on=['Naudota_nauja', 'Degalu_rusis'], how='inner')

    joined_data3 = pd.merge(data_2022, data_2023, on=['Naudota_nauja', 'Degalu_rusis'], how='inner')

    joined_data4 = pd.merge(joined_data, joined_data2, on=['Naudota_nauja', 'Degalu_rusis'], how='outer')

    joined_data5 = pd.merge(joined_data4, joined_data3, on=['Naudota_nauja', 'Degalu_rusis'], how='outer')
    print(joined_data5)
    return joined_data5

if __name__ == '__main__':
    joined_data5 = main()

    if joined_data5 is None:
        print("Duomenu nera")
    else:
        df = pd.DataFrame(joined_data5)
        df.to_csv('Auto registered in 2018-2023.csv', index=False)
        print('Data successfully  saved to "Auto registered in 2018-2023.csv".')



