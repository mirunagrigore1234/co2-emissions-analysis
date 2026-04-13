import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error, r2_score
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

# =========================
# CONFIGURARE
# =========================
st.set_page_config(page_title="CO2 Emissons App", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
    }

    h1, h2, h3 {
        color: #1f2937;
        font-family: 'Arial';
    }

    p {
        font-size: 16px;
        color: #374151;
    }
    </style>
""", unsafe_allow_html=True)
st.title("Influenta factorilor demografici si economici asupra emisiilor CO2 la nivel global")

# =========================
# 1. INCARCARE DATE
# =========================
data = pd.read_excel("data/CO2_emissions_factors.xlsx")

st.subheader("Dataset initial")
st.write(data)

# =========================
# 2. VALORI LIPSA
# =========================
st.subheader("Tratarea valorilor lipsă")

st.write(data.isnull().sum())

st.write("""
Valorile lipsă au fost tratate prin imputare cu mediana pentru toate variabilele numerice.
Această metodă este robustă la valori extreme și păstrează distribuția reală a datelor,
fiind preferată în analiza econometrică față de media aritmetică.
""")

numeric_cols = data.select_dtypes(include=np.number).columns
for col in numeric_cols:
    data[col] = data[col].fillna(data[col].median())

st.write(data.isnull().sum())

# =========================
# 3. VALORI EXTREME (BOXPLOT)
# =========================
st.subheader("Detectarea valorilor extreme")

st.write("""
Boxplot-ul evidențiază prezența unor valori extreme, în special pentru variabila FDI.
Aceste valori reflectă diferențe semnificative între țări în ceea ce privește fluxurile de investiții.

Pentru a reduce impactul acestor valori extreme asupra analizei,
au fost aplicate transformări logaritmice și transformarea asinh,
care diminuează influența outlierilor fără a elimina observațiile.
""")

fig, ax = plt.subplots(figsize=(6,3))

sns.boxplot(data=data[numeric_cols], ax=ax)

ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)

plt.tight_layout()

st.pyplot(fig, use_container_width=True)

# =========================
# 4. ELIMINARE VARIABILA CATEGORICA
# =========================
st.subheader("Eliminare variabilă categorică")

data = data.drop(columns=["Country"])

st.write("Coloana 'Country' a fost eliminată deoarece nu are semnificație numerică.")
st.write(data.head())

# =========================
# 5. TRANSFORMARI ECONOMETRICE
# =========================
st.subheader("Transformări econometrice")

# transformari
data["log_CO2"] = np.log(data["CO2_emissions"] + 1)
data["log_GDP"] = np.log(data["gdp_pc_ppp"] + 1)
data["log_population"] = np.log(data["total_population"] + 1)
data["asinh_fdi"] = np.arcsinh(data["fdi"])

# scaling
scaler = StandardScaler()
percent_cols = ["urban_population", "trade_in_services", "renewable_energy"]
data[percent_cols] = scaler.fit_transform(data[percent_cols])

st.write("""
Pentru a îmbunătăți calitatea analizei econometrice, au fost aplicate transformări asupra datelor:

- Variabilele cu distribuții asimetrice (CO2, GDP, populație) au fost transformate logaritmic
  pentru a reduce impactul valorilor extreme și a apropia distribuția de forma normală.

- Variabila FDI, care poate conține valori negative, a fost transformată folosind funcția asinh,
  o alternativă la logaritm care permite păstrarea valorilor negative.

- Variabilele procentuale (populația urbană, comerțul cu servicii, energia regenerabilă)
  au fost standardizate pentru a aduce toate variabilele pe aceeași scară și a permite
  compararea coeficienților în model.

Aceste transformări contribuie la stabilitatea modelului și la interpretarea corectă a rezultatelor.
""")

st.write(data.head())

st.subheader("Comparatie: Inainte vs Dupa transformari")

st.subheader("Transformări logaritmice")

fig, axes = plt.subplots(2, 2, figsize=(12,8))

# CO2
sns.histplot(data["CO2_emissions"], kde=True, ax=axes[0,0])
axes[0,0].set_title("CO2 - initial")

sns.histplot(data["log_CO2"], kde=True, ax=axes[0,1])
axes[0,1].set_title("CO2 - log transform")

# GDP
sns.histplot(data["gdp_pc_ppp"], kde=True, ax=axes[1,0])
axes[1,0].set_title("GDP - initial")

sns.histplot(data["log_GDP"], kde=True, ax=axes[1,1])
axes[1,1].set_title("GDP - log transform")

plt.tight_layout()
st.pyplot(fig)

st.subheader("Transformare FDI (asinh)")

fig2, axes2 = plt.subplots(1, 2, figsize=(12,4))

sns.histplot(data["fdi"], kde=True, ax=axes2[0])
axes2[0].set_title("FDI - initial")

sns.histplot(data["asinh_fdi"], kde=True, ax=axes2[1])
axes2[1].set_title("FDI - asinh")

st.pyplot(fig2)

st.subheader("Reducerea valorilor extreme")

fig3, axes3 = plt.subplots(1, 2, figsize=(12,5))

# inainte
sns.boxplot(data=data[["CO2_emissions", "gdp_pc_ppp"]], ax=axes3[0])
axes3[0].set_title("Inainte de transformare")

# dupa
sns.boxplot(data=data[["log_CO2", "log_GDP"]], ax=axes3[1])
axes3[1].set_title("Dupa transformare")

st.pyplot(fig3)

st.write("""
Analiza comparativă înainte și după transformări arată că variabilele inițiale prezentau
distribuții puternic asimetrice și valori extreme semnificative.

Aplicarea transformărilor logaritmice și asinh a redus considerabil dispersia datelor
și a comprimat valorile extreme, fără a elimina observațiile.

După transformare, distribuțiile devin mai apropiate de forma normală,
iar influența valorilor extreme asupra modelului este diminuată.

Astfel, datele sunt mai potrivite pentru analiza econometrică,
asigurând rezultate mai stabile și interpretabile.
""")


# =========================
# 6. STATISTICI + GROUPBY
# =========================
st.subheader("Gruparea datelor")

st.write("""
Datele au fost grupate în funcție de nivelul PIB-ului folosind cuantile.
Aceasta permite compararea țărilor în funcție de nivelul de dezvoltare economică.
""")

data["GDP_Group"] = pd.qcut(data["gdp_pc_ppp"], 4)

data["GDP_Group"] = data["GDP_Group"].apply(
    lambda x: f"({int(x.left)}, {int(x.right)}]"
)

group_stats = data.groupby("GDP_Group").agg({
    "CO2_emissions": ["mean", "min", "max"],
    "total_population": ["mean"],
    "gdp_pc_ppp": ["mean"]
})

st.write(group_stats)

fig, ax = plt.subplots(figsize=(5,3))

group_stats["CO2_emissions"]["mean"].plot(kind="bar", ax=ax)

ax.set_title("Emisii CO2 medii pe niveluri GDP", fontsize=12)
ax.set_ylabel("CO2 mediu", fontsize=10)

ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=7)

ax.tick_params(axis='y', labelsize=9)

plt.tight_layout()

st.pyplot(fig, use_container_width=False)

st.write("""
Rezultatele arată că nivelul emisiilor de CO2 diferă între grupurile de țări
clasificate în funcție de PIB.

În general, țările cu PIB mai ridicat tind să aibă emisii mai mari,
ceea ce sugerează o legătură între dezvoltarea economică și impactul asupra mediului.
""")

# =========================
# 7. CORELATII
# =========================
st.subheader("Matrice corelații")

fig2, ax2 = plt.subplots(figsize=(8,5))
sns.heatmap(data.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

# =========================
# REGRESIE (TRAIN / TEST)
# =========================
st.subheader("Regresie liniară multiplă")

st.write("""
Modelul estimează relația dintre emisiile de CO2 și factorii economici.
Datele sunt împărțite în set de antrenare și test pentru a evalua performanța reală a modelului.
""")

# -----------------------
# VARIABILE
# -----------------------
X = data[[
    "log_GDP",
    "log_population",
    "asinh_fdi",
    "urban_population",
    "trade_in_services",
    "renewable_energy"
]]

y = data["log_CO2"]

# -----------------------
# TRAIN / TEST SPLIT
# -----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# -----------------------
# MODEL (OLS)
# -----------------------
X_train_sm = sm.add_constant(X_train)
X_test_sm = sm.add_constant(X_test)

model = sm.OLS(y_train, X_train_sm).fit()

# -----------------------
# PREDICTII
# -----------------------
y_train_pred = model.predict(X_train_sm)
y_test_pred = model.predict(X_test_sm)

# -----------------------
# METRICI
# -----------------------
mse = mean_squared_error(y_test, y_test_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_test_pred)
r2 = r2_score(y_test, y_test_pred)

st.subheader("Performanța modelului")

st.write(f"MSE: {mse:.3f}")
st.write(f"RMSE: {rmse:.3f}")
st.write(f"MAE: {mae:.3f}")
st.write(f"R²: {r2:.3f}")

# -----------------------
# PLOT REAL vs PREDICTED
# -----------------------

st.subheader("Test: Comparatie valori reale vs estimate")

fig, ax = plt.subplots(figsize=(5,3))

ax.scatter(y_test_pred, y_test)
ax.set_xlabel("Valori estimate")
ax.set_ylabel("Valori reale")
ax.set_title("Predicted vs Actual CO2")

# linie ideala
ax.plot([y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        color='red')

st.pyplot(fig)

st.subheader("Train: Comparatie valori reale vs estimate")

fig_train, ax_train = plt.subplots(figsize=(5,3))

ax_train.scatter(y_train_pred, y_train)
ax_train.plot([y_train.min(), y_train.max()],
              [y_train.min(), y_train.max()],
              color='red')

ax_train.set_xlabel("Valori estimate")
ax_train.set_ylabel("Valori reale")
ax_train.set_title("Predicted vs Actual CO2")

st.pyplot(fig_train)

st.subheader("Performanță Train vs Test")

# TRAIN
mse_train = mean_squared_error(y_train, y_train_pred)
rmse_train = np.sqrt(mse_train)

st.write(f"RMSE Train: {rmse_train:.3f}")
st.write(f"RMSE Test: {rmse:.3f}")

if abs(rmse_train - rmse) < 0.5:
    st.success("Modelul generalizează bine (nu există overfitting semnificativ).")
else:
    st.warning("Diferență între train și test → posibil overfitting.")


st.subheader("Analiza erorii")

residuals = y_test - y_test_pred

fig_res, ax_res = plt.subplots(figsize=(5,3))

ax_res.scatter(y_test_pred, residuals)
ax_res.axhline(0)

ax_res.set_xlabel("Valori estimate")
ax_res.set_ylabel("Eroare")
ax_res.set_title("Residual plot")

st.pyplot(fig_res)

# -----------------------
# COEFICIENTI
# -----------------------
st.subheader("Coeficienți și interpretare")

results_table = pd.DataFrame({
    "Coeficient": model.params,
    "P-value": model.pvalues
})

# semnificatie
results_table["Semnificativ"] = results_table["P-value"].apply(
    lambda x: "Semnificativ" if x < 0.05 else "Nesemnificativ"
)


# interpretare automata
def interpretare(row):
    coef = row["Coeficient"]

    if coef > 0:
        return "Efect pozitiv"
    elif coef < 0:
        return "Efect negativ"
    else:
        return "Fără efect"


results_table["Interpretare"] = results_table.apply(interpretare, axis=1)

st.write(results_table)

# -----------------------
# INTERPRETARE
# -----------------------

st.subheader("Interpretare model")

# interpretare calitativa
if r2 > 0.7:
    st.success("""
Modelul are o putere explicativă ridicată.

Rezultatele sugerează că factorii economici incluși (PIB, comerț, energie etc.)
explică în mare măsură nivelul emisiilor de CO2 între țări.
""")

elif r2 > 0.5:
    st.warning("""
Modelul are o putere explicativă moderată.

O parte semnificativă din variația emisiilor este explicată,
însă există și alți factori relevanți care nu sunt incluși în model.
""")

else:
    st.error("""
Modelul are o putere explicativă redusă.

Variabilele incluse nu sunt suficiente pentru a explica variația emisiilor de CO2,
ceea ce sugerează necesitatea includerii altor factori.
""")

st.write(f"Modelul obține un R² de {r2:.3f}, ceea ce indică faptul că aproximativ {r2*100:.1f}% din variația emisiilor de CO2 este explicată de variabilele incluse în model.")

st.write(f"Eroarea medie a predicțiilor (RMSE) este {rmse:.3f}, ceea ce arată diferența tipică dintre valorile reale și cele estimate ale log_CO2.")

st.write(f"Valoarea MAE de {mae:.3f} confirmă faptul că deviația medie absolută a predicțiilor este relativ redusă, indicând o bună acuratețe a modelului.")

st.write("""
Diferențele dintre valorile reale și cele estimate pot indica existența unor relații non-lineare
sau a unor variabile omise (ex: politici de mediu, structură industrială, consum energetic).

În ansamblu, modelul oferă o aproximare utilă a relației dintre dezvoltarea economică și impactul asupra mediului.
""")

# =========================
# 10. CLUSTERIZARE (KMEANS OPTIM)
# =========================
st.subheader("Clusterizare (KMeans - determinare k optim)")

# -----------------------
# SELECTARE DATE
# -----------------------
X_cluster = data[["log_GDP", "log_CO2"]]

# -----------------------
# 1. ELBOW METHOD (WCSS)
# -----------------------
st.write("### Elbow Method")

wcss = []
k_range = range(1, 11)

for k in k_range:
    km = KMeans(n_clusters=k, init='k-means++', random_state=42)
    km.fit(X_cluster)
    wcss.append(km.inertia_)

fig_elbow, ax_elbow = plt.subplots(figsize=(5,3))

ax_elbow.plot(k_range, wcss, marker='o')
ax_elbow.set_title("Elbow Method")
ax_elbow.set_xlabel("Număr clustere (k)")
ax_elbow.set_ylabel("WCSS")

st.pyplot(fig_elbow)

# -----------------------
# 2. SILHOUETTE SCORE
# -----------------------
st.write("### Silhouette Score")

sil_scores = []

for k in range(2, 11):
    km = KMeans(n_clusters=k, init='k-means++', random_state=42)
    labels = km.fit_predict(X_cluster)
    score = silhouette_score(X_cluster, labels)
    sil_scores.append(score)

fig_sil, ax_sil = plt.subplots(figsize=(5,3))

ax_sil.plot(range(2, 11), sil_scores, marker='o')
ax_sil.set_title("Silhouette Score vs k")
ax_sil.set_xlabel("k")
ax_sil.set_ylabel("Silhouette Score")

st.pyplot(fig_sil)

# -----------------------
# 3. ALEGERE AUTOMATA k
# -----------------------
optimal_k = range(2, 11)[np.argmax(sil_scores)]

st.success(f"Numărul optim de clustere: k = {optimal_k}")

st.write("""
Numărul optim de clustere a fost ales pe baza valorii maxime a Silhouette Score,
care măsoară cât de bine sunt separate grupurile.

Această metodă permite evitarea unei alegeri arbitrare a lui k și conduce la
un model mai robust și mai relevant din punct de vedere economic.
""")

# -----------------------
# 4. MODEL FINAL KMEANS
# -----------------------
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42)
clusters = kmeans.fit_predict(X_cluster)

data["Cluster"] = clusters

# -----------------------
# 5. VIZUALIZARE CLUSTERE
# -----------------------
st.write("### Vizualizare clustere")

fig_cluster, ax_cluster = plt.subplots(figsize=(5,3))

sns.scatterplot(
    x=data["log_GDP"],
    y=data["log_CO2"],
    hue=data["Cluster"],
    palette="Set1",
    ax=ax_cluster
)

# centroizi
centers = kmeans.cluster_centers_

ax_cluster.scatter(
    centers[:, 0],
    centers[:, 1],
    s=200,
    c='black',
    marker='X',
    label='Centroizi'
)

ax_cluster.set_title("Clusterizare țări (GDP vs CO2)")
ax_cluster.set_xlabel("log(GDP)")
ax_cluster.set_ylabel("log(CO2)")
ax_cluster.legend()

st.pyplot(fig_cluster)

# -----------------------
# 6. SILHOUETTE FINAL
# -----------------------
sil_score_final = silhouette_score(X_cluster, data["Cluster"])

st.write(f"Silhouette Score final: {round(sil_score_final, 3)}")

# interpretare
if sil_score_final > 0.7:
    st.success("Clusterele sunt foarte bine definite și clar separate.")
elif sil_score_final > 0.5:
    st.info("Clusterele sunt rezonabil bine separate, dar există suprapuneri.")
elif sil_score_final > 0.25:
    st.warning("Separarea clusterelor este slabă.")
else:
    st.error("Clusterele nu sunt bine definite.")

# -----------------------
# 7. ANALIZA PE CLUSTERE
# -----------------------
st.write("### Analiza clusterelor")

cluster_summary = data.groupby("Cluster").agg({
    "CO2_emissions": "mean",
    "gdp_pc_ppp": "mean",
    "total_population": "mean"
})

st.write(cluster_summary)

st.write("""
Analiza arată diferențele dintre grupurile de țări.

Clusterizarea confirmă existența unor tipare economice:
țările cu PIB ridicat tind să formeze grupuri distincte față de cele cu PIB scăzut,
iar emisiile de CO2 urmează aceste diferențe de dezvoltare economică.
""")

# =========================
# 12. COMPARATIE REGRESIE vs CLUSTERIZARE
# =========================
st.subheader("Analiza performanței regresiei pe clustere")

st.write("""
Această secțiune analizează modul în care performanța modelului de regresie variază între clustere.

Scopul nu este compararea directă a regresiei cu clusterizarea,
ci evaluarea stabilității modelului pe grupuri de țări cu caracteristici similare.
""")

# -----------------------
# PREDICTII
# -----------------------
X_full = sm.add_constant(X)
data["Predicted_log_CO2"] = model.predict(X_full)

# transformare inapoi
data["Predicted_CO2"] = np.exp(data["Predicted_log_CO2"]) - 1

# -----------------------
# EROARE
# -----------------------
data["Error"] = data["CO2_emissions"] - data["Predicted_CO2"]

# -----------------------
# ANALIZA PE CLUSTERE
# -----------------------
cluster_analysis = data.groupby("Cluster").agg({
    "CO2_emissions": "mean",
    "Predicted_CO2": "mean",
    "Error": ["mean", "std"]
})

st.write("Analiza pe clustere:")
st.write(cluster_analysis)

# -----------------------
# GRAFIC REAL vs ESTIMAT
# -----------------------
st.write("### CO2 real vs estimat")

fig1, ax1 = plt.subplots(figsize=(5,3))

sns.scatterplot(
    x=data["CO2_emissions"],
    y=data["Predicted_CO2"],
    hue=data["Cluster"],
    palette="Set1",
    ax=ax1
)

ax1.set_xlabel("CO2 real")
ax1.set_ylabel("CO2 estimat")
ax1.set_title("Performanța regresiei pe clustere")

st.pyplot(fig1)

st.subheader("Interpretare")

st.write("""
Analiza graficului CO2 real vs CO2 estimat arată diferențe clare între cele două clustere.

Pentru clusterul 1 (albastru), valorile estimate sunt foarte apropiate de cele reale,
fiind concentrate în jurul unei relații bine definite. Acest lucru indică faptul că modelul
funcționează foarte bine pentru țările din acest grup.
""")

st.write("""
În schimb, pentru clusterul 0 (roșu), se observă o dispersie mult mai mare a punctelor,
în special pentru valori ridicate ale emisiilor de CO2. Modelul tinde să subestimeze
sau să supraestimeze în mod semnificativ aceste valori.
""")

# -----------------------
# GRAFIC EROARE PE CLUSTERE
# -----------------------
st.write("### Distribuția erorilor pe clustere")

fig2, ax2 = plt.subplots(figsize=(5,3))

sns.boxplot(
    x=data["Cluster"],
    y=data["Error"],
    ax=ax2
)

ax2.set_title("Eroare model pe clustere")
ax2.set_xlabel("Cluster")
ax2.set_ylabel("Eroare")

st.pyplot(fig2)

st.subheader("Interpretare")

st.write("""
Conform distribuției eroriilor:

- Clusterul 1 are erori mici și compacte, ceea ce indică o bună acuratețe a modelului
- Clusterul 0 prezintă erori mult mai mari și variabile, inclusiv outlieri semnificativi
""")

st.write("""
Aceste rezultate arată că modelul de regresie nu se comportă uniform pentru toate țările.

Modelul este mai precis pentru economiile cu niveluri mai reduse și omogene ale emisiilor,
dar își pierde acuratețea pentru țările cu emisii ridicate și mai variabile.
""")

st.write("""
Acest lucru sugerează existența unei relații non-lineare sau a unor factori suplimentari
care influențează emisiile în cazul țărilor din clusterul 0.

De asemenea, poate indica faptul că un model global unic nu este suficient
pentru a descrie toate tipurile de economii.
""")

st.subheader("Concluzii")

st.write("""
În concluzie, clusterizarea evidențiază heterogenitatea datelor,
iar regresia arată că relațiile economice diferă între grupuri.

O posibilă îmbunătățire ar fi estimarea unor modele separate pentru fiecare cluster,
pentru a surprinde mai bine diferențele structurale dintre economii.
""")

# =========================
# 13. INTERPRETARE BUSINESS
# =========================
st.subheader("Implicații economice și de business")

st.write("""
Rezultatele analizei oferă perspective relevante pentru decidenții economici și de mediu.

Creșterea PIB-ului este asociată cu creșterea emisiilor de CO2,
ceea ce sugerează că dezvoltarea economică actuală este încă dependentă de resurse poluante.

În schimb, utilizarea energiei regenerabile are un efect semnificativ în reducerea emisiilor,
indicând importanța investițiilor în energie sustenabilă.
""")

st.write("""
Analiza pe clustere arată că economiile nu sunt omogene:

- Țările dezvoltate au emisii mai mari și variabilitate ridicată
- Țările mai puțin dezvoltate au emisii mai stabile și mai reduse

Modelul de regresie nu performează uniform pe toate grupurile,
ceea ce sugerează că un model global unic nu este suficient.
""")

st.write("""
Implicații practice:

- Politicile de mediu trebuie adaptate pe tipuri de economii
- Investițiile în energie regenerabilă sunt esențiale pentru reducerea emisiilor
- Modelele predictive ar trebui personalizate pe regiuni sau clustere
""")

st.write("""
În ansamblu, rezultatele indică faptul că dezvoltarea economică este asociată cu un impact semnificativ asupra mediului,
iar reducerea emisiilor depinde în mare măsură de tranziția către surse de energie sustenabile.
""")

st.info("""
Posibilă îmbunătățire:

Modele de tip Machine Learning (ex: Random Forest) pot surprinde relații non-lineare
și pot îmbunătăți predicțiile pentru economii complexe.
""")