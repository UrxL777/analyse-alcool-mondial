import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Analyse Mondiale de la Consommation d'Alcool",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background-color: #FFF8F0;
    }
    [data-testid="stSidebar"] {
        background-color: #F5E6D3;
    }
    h1 {
        color: goldenrod;
    }
    [data-testid="stMetric"] {
        background-color: white !important;
        border: 2px solid goldenrod !important;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


  
# Chargement des données
# Variable Colonne gardé
# Colonne renommé

uriel = "alcohol-consumption-world-6a1dcc4a19341808431342.csv"
df = pd.read_csv(uriel)

cg = df[["ParentLocationCode", "ParentLocation", "SpatialDimValueCode", "Location", "Period", "IsLatestYear", "FactValueNumeric", "FactValueNumericLow", "FactValueNumericHigh"]]

cg = cg.rename(columns={"ParentLocationCode": "Code_Region", "ParentLocation": "Regions", "SpatialDimValueCode": "Code_Pays", "Location": "Pays", "Period": "Annees", "IsLatestYear": "Annee_Recentes", "FactValueNumeric": "Conso_Litres", "FactValueNumericLow": "Conso_Litres_Min", "FactValueNumericHigh": "Conso_Litres_Max"})

# Titre principal
st.markdown(f"""
    <h1> 
        <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="goldenrod">
            <path d="M280-280h80v-200h-80v200Zm320 0h80v-400h-80v400Zm-160 0h80v-120h-80v120Zm0-200h80v-80h-80v80ZM200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/>
        </svg>
        Analyse Mondiale de la consommation d'Alcool
    </h1>      
""", unsafe_allow_html=True)
st.markdown("**Source : OMS — SDG Indicator 3.5.2 | Période : 2000 - 2022 | 188 pays**")

# Slicers
st.sidebar.title("Filtres")

regions_list = ["Toutes"] + sorted(cg["Regions"].unique().tolist())
region_selectionnee = st.sidebar.selectbox("Région", regions_list)

annee_min, annee_max = st.sidebar.slider("Période",
                                          min_value=int(cg["Annees"].min()),
                                          max_value=int(cg["Annees"].max()),
                                          value=(2000, 2022))

pays_list = ["Tous"] + sorted(cg[cg["Regions"] == region_selectionnee]["Pays"].unique().tolist()) if region_selectionnee != "Toutes" else ["Tous"] + sorted(cg["Pays"].unique().tolist())
pays_selectionne = st.sidebar.selectbox("Pays", pays_list)

# Infos automatiques quand un pays est sélectionné
if pays_selectionne != "Tous":
    region_auto = cg[cg["Pays"] == pays_selectionne]["Regions"].values[0]
    annees_dispo = cg[cg["Pays"] == pays_selectionne]["Annees"]
    st.sidebar.info(f"Région : {region_auto}")
    st.sidebar.info(f"Années disponibles : {int(annees_dispo.min())} - {int(annees_dispo.max())}")

# Appliquer les filtres
if region_selectionnee == "Toutes":
    df_filtre = cg[(cg["Annees"] >= annee_min) & (cg["Annees"] <= annee_max)]
else:
    df_filtre = cg[(cg["Annees"] >= annee_min) & (cg["Annees"] <= annee_max) & (cg["Regions"] == region_selectionnee)]

if pays_selectionne != "Tous":
    df_filtre = df_filtre[df_filtre["Pays"] == pays_selectionne]

# KPIs
st.subheader("Indicateurs Clés")
col1, col2, col3, col4 = st.columns(4)

moyenne = round(df_filtre["Conso_Litres"].mean(), 2)
nb_pays = df_filtre["Pays"].nunique()
max_conso = round(df_filtre["Conso_Litres"].max(), 2)
nb_annees = df_filtre["Annees"].nunique()

col1.markdown(f"""
    <div style="background:white;border:2px solid goldenrod;border-radius:10px;padding:15px;box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="blue">
            <path d="M480-80q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-7-.5-14.5T799-507q-5 29-27 48t-52 19h-80q-33 0-56.5-23.5T560-520v-40H400v-80q0-33 23.5-56.5T480-720h40q0-23 12.5-40.5T563-789q-20-5-40.5-8t-42.5-3q-134 0-227 93t-93 227h200q66 0 113 47t47 113v40H400v110q20 5 39.5 7.5T480-160Z"/>
        </svg>
        <p style="margin:5px 0;font-size:13px;color:saddlebrown;">Moyenne Mondiale (L)</p>
        <p style="margin:0;font-size:28px;font-weight:700;color:#2C1810;">{moyenne}</p>
    </div>
""", unsafe_allow_html=True)

col2.markdown(f"""
    <div style="background:white;border:2px solid goldenrod;border-radius:10px;padding:15px;box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="goldenrod">
            <path d="M200-120v-680h360l16 80h224v400H520l-16-80H280v280h-80Zm300-440Zm86 160h134v-240H510l-16-80H280v240h290l16 80Z"/>
        </svg>
        <p style="margin:5px 0;font-size:13px;color:saddlebrown;">Nombre de Pays</p>
        <p style="margin:0;font-size:28px;font-weight:700;color:#2C1810;">{nb_pays}</p>
    </div>
""", unsafe_allow_html=True)

col3.markdown(f"""
    <div style="background:white;border:2px solid goldenrod;border-radius:10px;padding:15px;box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="red">
            <path d="m136-240-56-56 296-298 160 160 208-206H640v-80h240v240h-80v-104L536-320 376-480 136-240Z"/>
        </svg>
        <p style="margin:5px 0;font-size:13px;color:saddlebrown;">Max Enregistré (L)</p>
        <p style="margin:0;font-size:28px;font-weight:700;color:#2C1810;">{max_conso}</p>
    </div>
""", unsafe_allow_html=True)

col4.markdown(f"""
    <div style="background:white;border:2px solid goldenrod;border-radius:10px;padding:15px;box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="green">
            <path d="M200-80q-33 0-56.5-23.5T120-160v-560q0-33 23.5-56.5T200-800h40v-80h80v80h320v-80h80v80h40q33 0 56.5 23.5T840-720v560q0 33-23.5 56.5T760-80H200Zm0-80h560v-400H200v400Zm0-480h560v-80H200v80Zm0 0v-80 80Z"/>
        </svg>
        <p style="margin:5px 0;font-size:13px;color:saddlebrown;">Années Analysées</p>
        <p style="margin:0;font-size:28px;font-weight:700;color:#2C1810;">{nb_annees}</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Visuels ligne 1 — Top 10 et Donut côte à côte
col_a, col_b = st.columns(2)

with col_a:
    top10 = df_filtre.groupby("Pays")["Conso_Litres"].mean().sort_values(ascending=False).head(10).reset_index().sort_values("Conso_Litres", ascending=True)
    fig1 = px.bar(top10, x="Conso_Litres", y="Pays", orientation="h",
                  title="Top 10 pays consommateurs",
                  color="Conso_Litres", color_continuous_scale="Oranges")
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    regions = df_filtre.groupby("Regions")["Conso_Litres"].mean().reset_index()
    fig2 = px.pie(regions, values="Conso_Litres", names="Regions",
                  title="Consommation moyenne par région",
                  hole=0.5)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Visuels ligne 2 — Courbes d'évolution
st.subheader("Évolution Temporelle")

annees = df_filtre.groupby("Annees")["Conso_Litres"].mean().reset_index()
fig3 = px.area(annees, x="Annees", y="Conso_Litres",
               title="Évolution mondiale de la consommation d'alcool",
               color_discrete_sequence=["goldenrod"], markers=True)
fig3.update_xaxes(dtick=1)
st.plotly_chart(fig3, use_container_width=True)

evo_region = df_filtre.groupby(["Annees", "Regions"])["Conso_Litres"].mean().reset_index()
fig4 = px.line(evo_region, x="Annees", y="Conso_Litres", color="Regions",
               title="Évolution de la consommation par région",
               markers=True)
fig4.update_xaxes(dtick=1)
st.plotly_chart(fig4, use_container_width=True)  

st.divider()
st.markdown("""
     <div style="text-align:center; color:saddlebrown; font-size:13px; padding:10px;">
        <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="goldenrod">
            <path d="M640-160v-280h160v280H640Zm-240 0v-640h160v640H400Zm-240 0v-440h160v440H160Z"/>
        </svg>
        Analyse réalisée dans le cadre du projet OIVS | SIMPLON-CI
        Source : OMS — SDG Indicator 3.5.2 |
        Données : 2000 - 2022 |
        188 pays analysés
    </div>
""", unsafe_allow_html=True)

