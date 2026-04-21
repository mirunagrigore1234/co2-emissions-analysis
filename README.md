# Influence of Economic and Demographic Factors on CO₂ Emissions

Interactive application for analyzing the influence of economic and demographic factors on global CO₂ emissions.

## Demo

The application is available here: https://co2-emissions-analysis.streamlit.app/

## Rezultate principale

- GDP has a significant positive impact on CO₂ emissions
- Renewable energy contributes to reducing emissions
- Countries can be grouped into distinct economic clusters

## Context and Problem

In the context of climate change, understanding the relationship between economic development and environmental impact is essential for designing sustainable policies.

This project analyzes how factors such as GDP, population, foreign direct investment, and renewable energy usage influence CO₂ emission levels.

The goal is to identify relevant economic relationships and highlight global patterns across countries.

## Objectives

- Analyze the relationship between economic development and CO₂ emissions
- Identify variables with a significant impact on emissions
- Evaluate the performance of an econometric model
- Group countries based on economic and environmental characteristics
- Create an interactive application for data exploration

## Dataset

The data used includes global economic and demographic indicators:

- CO₂ emissions
- GDP per capita
- Total population
- Foreign direct investment (FDI)
- Renewable energy
- Urban population

## Data Sources

The data used in this project comes from international public sources:

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

## Methodology

### 1. Data Preprocessing

- Handling missing values using median imputation
- Identifying outliers using boxplots
- Removing irrelevant variables (e.g., Country)

### 2. Econometric Transformations

- Log transformation for skewed variables (CO₂, GDP, population)
- asinh transformation for FDI (allows negative values)
- Standardization for percentage variables

These transformations reduce the impact of extreme values and improve model stability.

### 3. Exploratory Data Analysis (EDA)

- Variable distributions
- Correlation matrix
- Graphical analysis

### 4. Data Grouping

- Classifying countries based on GDP using quantiles (qcut)
- Comparative analysis between groups

### 5. Econometric Model

A multiple linear regression model (OLS – Ordinary Least Squares) was used.

- Dependent variable: log_CO2
- Evaluation metrics:
  - R²
  - RMSE
  - MAE

The model allows economic interpretation through coefficients and p-values.

### 6. Clustering

- Algorithm used: KMeans
- Determining the optimal number of clusters:
  - Elbow Method
  - Silhouette Score

Permite identificarea unor grupuri de țări cu caracteristici similare.

## Economic Interpretation

- Developed economies generate higher emissions due to industrialization and increased energy consumption
- Countries with higher renewable energy usage tend to have lower emissions
- There is heterogeneity across economies, suggesting that a global model may not fully capture structural differences

This highlights the need for differentiated environmental policies.

## Implicații practice

The analysis results can be used for:

- designing environmental public policies
- evaluating the impact of economic development on emissions
- identifying high-risk countries for pollution
- prioritizing investments in renewable energy

## Application

The project includes an interactive application built with Streamlit, allowing:
- data visualization
- exploration of relationships between variables
- model performance analysis
- interpretation of results

##  Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib / Seaborn
- Scikit-learn
- Statsmodels

## Project Structure

```
project/
├── app/
│ └── app.py
├── data/
├── notebooks/
├── requirements.txt
├── README.md
```

## Running the Project

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Limitations and Future Directions

The linear regression model does not fully capture non-linear relationships in the data, especially for high-emission economies.

Additionally, the model is estimated at a global level without distinguishing between types of economies or regions, which may reduce accuracy in some cases.

Possible improvements:

- Adding additional variables (e.g., environmental policies, energy consumption)
- Using more complex models (e.g., Random Forest, Gradient Boosting)
- Conducting region-specific or cluster-based analysis
- Comparing the performance of multiple predictive models

These improvements could lead to more accurate and relevant models for analyzing the economic impact on the environment.

## Conclusions

The analysis highlights a strong relationship between economic development and CO₂ emissions.

The results suggest that while economic growth is essential, it comes with environmental costs, emphasizing the need for sustainable strategies to reduce emissions and protect the environment.

## Team

- Ana-Miruna Grigore  
- Mara-Catinca Marinescu  

**Supervisor:** Ene Gabriela 

## Notes

This project was developed as part of a university course and focuses on data analysis, econometric modeling, and the use of machine learning techniques to study CO₂ emissions.

It also emphasizes result interpretation and understanding the relationships between economic factors and environmental impact.

It is intended for educational and portfolio purposes.


