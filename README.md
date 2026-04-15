# Influența factorilor economici și demografici asupra emisiilor de CO2 

Aplicație interactivă pentru analiza influenței factorilor economici și demografici asupra emisiilor de CO2 la nivel global.

## Demo

Aplicația este disponibilă aici: https://co2-emissions-analysis.streamlit.app/

## Rezultate principale

- PIB-ul are un impact pozitiv semnificativ asupra emisiilor de CO2
- Energia regenerabilă contribuie la reducerea emisiilor
- Țările pot fi grupate în clustere economice distincte

## Context și problemă

În contextul schimbărilor climatice, înțelegerea relației dintre dezvoltarea economică și impactul asupra mediului este esențială pentru formularea unor politici sustenabile.

Acest proiect analizează modul în care factori precum PIB-ul, populația, investițiile străine și utilizarea energiei regenerabile influențează nivelul emisiilor de CO2.

Scopul este identificarea relațiilor economice relevante și evidențierea unor tipare globale între țări.

## Obiective
- Analiza relației dintre dezvoltarea economică și emisiile de CO2
- Identificarea variabilelor cu impact semnificativ asupra emisiilor
- Evaluarea performanței unui model econometric
- Gruparea țărilor în funcție de caracteristici economice și de mediu
- Crearea unei aplicații interactive pentru explorarea datelor

## Setul de date

Datele utilizate includ indicatori economici și demografici globali:

- Emisii de CO2
- PIB pe cap de locuitor (GDP)
- Populație totală
- Investiții străine directe (FDI)
- Energie regenerabilă
- Populație urbană

## Surse date

Datele utilizate în acest proiect provin din surse publice internaționale:

- Trade in services as share of GDP (%)  
  Our World in Data  
  https://ourworldindata.org/grapher/service-exports-and-imports-gdp

- CO2 emissions (metric tons per capita)  
  The World Bank  
  https://data.worldbank.org/indicator/EN.ATM.CO2E.PC

- GDP per capita, PPP (current international $)  
  The World Bank  
  https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD

- Urban population (% of total population)  
  The World Bank  
  https://data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS

- Population, total  
  The World Bank  
  https://data.worldbank.org/indicator/SP.POP.TOTL

- Foreign direct investment, net inflows (BoP, current US$)  
  The World Bank  
  https://data.worldbank.org/indicator/BX.KLT.DINV.CD.WD

- Renewable energy consumption (% of total final energy consumption)  
  The World Bank  
  https://data.worldbank.org/indicator/EG.FEC.RNEW.ZS

## Metodologie

### 1. Prelucrarea datelor
- Tratarea valorilor lipsă prin imputare cu mediana
- Identificarea valorilor extreme (outlieri) folosind boxplot
- Eliminarea variabilelor nerelevante (ex: Country)

### 2. Transformări econometrice
- Transformare logaritmică pentru variabilele asimetrice (CO2, GDP, populație)
- Transformare asinh pentru FDI (permite valori negative)
- Standardizare pentru variabile procentuale

Aceste transformări reduc impactul valorilor extreme și îmbunătățesc stabilitatea modelului.

### 3. Analiză exploratorie (EDA)
- Distribuții ale variabilelor
- Matrice de corelații
- Analiză grafică

### 4. Gruparea datelor
- Clasificarea țărilor în funcție de PIB folosind cuantile (qcut)
- Analiză comparativă între grupuri

### 5. Model econometric

A fost utilizat un model de regresie liniară multiplă (OLS – Ordinary Least Squares).

- Regresie liniară multiplă (OLS – Ordinary Least Squares)
- Variabilă dependentă: log_CO2
- Evaluare folosind:
  - R²
  - RMSE
  - MAE

Modelul permite interpretarea economică prin coeficienți și p-values.

### 6. Clusterizare

- Algoritm utilizat: KMeans
- Determinarea numărului optim de clustere:
- Elbow Method
- Silhouette Score

Permite identificarea unor grupuri de țări cu caracteristici similare.

## Interpretare economică

- Economiile dezvoltate generează emisii mai ridicate datorită industrializării și consumului energetic crescut
- Țările cu un nivel ridicat de utilizare a energiei regenerabile au emisii mai reduse
- Există heterogenitate între economii, ceea ce sugerează că un model global poate să nu surprindă complet diferențele structurale

Acest lucru evidențiază necesitatea unor politici diferențiate de mediu.

## Implicații practice

Rezultatele analizei pot fi utilizate pentru:

- formularea politicilor publice de mediu
- evaluarea impactului dezvoltării economice asupra emisiilor
- identificarea țărilor cu risc ridicat de poluare
- prioritizarea investițiilor în energie regenerabilă

## Aplicație

Proiectul include o aplicație interactivă realizată în Streamlit, care permite:
- vizualizarea datelor
- explorarea relațiilor dintre variabile
- analiza performanței modelului
- interpretarea rezultatelor

##  Tehnologii utilizate

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib / Seaborn
- Scikit-learn
- Statsmodels

## Structura proiectului

```
project/
├── app/
│ └── app.py
├── data/
├── notebooks/
├── requirements.txt
├── README.md
```

## Rulare

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Limitări și direcții viitoare

Modelul de regresie liniară nu captează complet relațiile non-lineare din date, în special pentru economiile cu emisii ridicate.

De asemenea, modelul este estimat la nivel global, fără a diferenția între tipuri de economii sau regiuni, ceea ce poate reduce acuratețea în anumite cazuri.

Direcții de îmbunătățire:

- Integrarea unor variabile suplimentare (ex: politici de mediu, consum energetic)
- Utilizarea unor modele mai complexe (ex: Random Forest, Gradient Boosting)
- Analiză separată pe regiuni geografice sau clustere
- Compararea performanței mai multor modele predictive

Aceste îmbunătățiri pot conduce la modele mai precise și mai relevante pentru analiza impactului economic asupra mediului.

## Concluzie

Analiza evidențiază o relație puternică între dezvoltarea economică și nivelul emisiilor de CO2.

Rezultatele sugerează că dezvoltarea economică, deși esențială, vine cu un cost asupra mediului, subliniind necesitatea unor strategii sustenabile pentru reducerea emisiilor și protejarea mediului.

## Echipa

- Ana-Miruna Grigore  
- Mara-Catinca Marinescu  

**Profesor coordonator:** Ene Gabriela 

## Note

Acest proiect a fost realizat în cadrul unui curs universitar și se concentrează pe analiza datelor, modelare econometrică și utilizarea tehnicilor de machine learning pentru studierea emisiilor de CO2.

De asemenea, proiectul pune accent pe interpretarea rezultatelor și înțelegerea relațiilor dintre factorii economici și impactul asupra mediului.

Este destinat scopurilor educaționale și pentru portofoliu.
