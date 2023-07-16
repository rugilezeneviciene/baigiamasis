Šio projekto tikslas – išanalizuoti parduodamų automobilių rinką, laikantis tvarkingos projekto struktūros, panaudojant kursuose nagrinėtas bibliotekas.
Rugilės ir Miglės duomenų analitikos kurso baigiamasis darbas: automobilių rinkos apžvalga.

Turinys
- Duomenų pasirinkimas
- Duomenų šaltiniai
- Projekto eiga
- Naudotos bibliotekos ir įrankiai
- Duomenų analizė
- Išvados

| Valstybė  |
| --------- |
| Vokietija |
| Lenkija   | 
 
Projekto eiga
1. Atsisiųsti duomenis iš atvirų šaltinių.
2. Atlikti duomenų pasiėmimą (angl. Scrapping) iš autogidas.lt
3. Duomenų tvarkymas: tuščių eilučių pašalinimas, duomenų tipų suvienodinimas ir nustatymas, pavadinimų suvienodinimas.
4. Analizė ir grafikų braižymas
5. Prognozavimo modelio sudarymas
Naudotos bibliotekos ir įrankiai
1. Duomenų pasiėmimui iš Autogidas.lt naudojama angl. Scrappinimas.
2. Duomenų įkėlimui, tvarkymui ir atvaizdavimui kuriamos funkcijos.
3. Duomenų sujungimui iš kelių lentelių – naudojama sujungimas (merge).
4. Lentelė su Vokietijos ir Lietuvos duomenimis įsikelta į Postgress.
5. Naudojamos bibliotekos: Pandas, NumPy, Matplotlib, Seaborn, Psycopg2, Sklearn.
 
Duomenų analizė
Analizės klausimai:
1. Išanalizuoti automobilių amžiaus pasiskirstymą skirtingose šalyse. Kokio amžiaus automobiliai populiariausi?
2. Remiantis vidutine modelių kaina, išsiaiškinti, kurie automobiliai yra brangiausi ir kurie pigiausi skirtingose šalyse.
3. Įvertinti ridos ir amžiaus įtaką automobilio kainai.
4. Kuro tipo pasiskirstymas skirtingose šalyse.
5. Transmisijos tipo pasiskirstymas skirtingose šalyse.
6. Automobilių markių pasiskirstymas skirtingose šalyse.
7. Ar pasiskirstymui turi įtakos naftos kainos už barelį pokyčiai?
Išvados
1. Lietuvoje didžiausias vidutinis parduodamų automobilių amžius, o Vokietijoje mažiausias.
2. Lenkijoje ir Vokietijoje vidutiniškai brangiausia automobilio markė  - Lamborghini, Lietuvoje - Porsche. Lenkijoje ir Vokietijoje vidutiniškai brangiausia automobilio markė  - Daewoo, Lietuvoje - Moskvitch.
3. Remiantis heatmap diagrama, egzistuoja atvirkštinis ryšys tarp automobilio pagaminimo metų ir automobilio ridos, vadinasi, galima teigti, kad kuo automobilis naujesnis, tuo jo rida yra mažesnė. Tarp automobilio amžiaus ir kainos egzistuoja silpnas statistinis ryšys, o tarp ridos ir kainos silpnas atvirkštinis ryšys.
4. Lietuvoje didžiausią parduodamų automobilių dalį sudaro dyzeliu varomi automobiliai, o Lenkijoje ir Vokietijoje - benzinu. 
5. Lietuvoje ir Lenkijoje didžiausią parduodamų automobilių dalį sudaro mechaninės pavarų dėžės automobiliai, o Vokietijoje - automatinės pavarų dėžės.
6. Populiariausia parduodamų automobilių markė Lietuvoje - Volkswagen, modelis - Passat. Populiariausia parduodamų automobilių markė Vokietijoje ir Lenkijoje - Volkswagen, modelis - Golf.
7. Lietuvoje naujų ir naudotų įregistruotų automobilių skaičius  ženkliai sumažėjo COVID - 19 pandemijos pradžioje. Stipraus tiesioginio ryšio tarp naftos kainos ir Lietuvoje registruotų naujų ar naudotų automobilių nestebim
