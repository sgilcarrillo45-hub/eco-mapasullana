import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(
    page_title="ECO-MAPA Sullana",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 ECO-MAPA SULLANA")
st.write("Plataforma de Diagnostico y Monitoreo Ambiental")

@st.cache_data
def obtener_datos():
    return pd.DataFrame([
        {"Sector": "Rio Chira", "lat": -4.9042, "lon": -80.6975, "Nivel": "Critico", "Color": "red", "Tipo": "Contaminacion Hidrica"},
        {"Sector": "Canal Via Leticia", "lat": -4.8981, "lon": -80.6864, "Nivel": "Critico", "Color": "red", "Tipo": "Aguas Residuales"},
        {"Sector": "Botadero Municipal", "lat": -4.8850, "lon": -80.6420, "Nivel": "Critico", "Color": "red", "Tipo": "Quema de Basura"},
        {"Sector": "Mercado Modelo", "lat": -4.9015, "lon": -80.6882, "Nivel": "Critico", "Color": "red", "Tipo": "Residuos Organicos"},
        {"Sector": "Camal Municipal", "lat": -4.9120, "lon": -80.6795, "Nivel": "Moderado", "Color": "orange", "Tipo": "Efluentes Organicos"},
        {"Sector": "Canal Via Bellavista", "lat": -4.8912, "lon": -80.6810, "Nivel": "Critico", "Color": "red", "Tipo": "Escombros"},
        {"Sector": "Urb. Santa Rosa", "lat": -4.9150, "lon": -80.6910, "Nivel": "Moderado", "Color": "orange", "Tipo": "Acumulacion Domestica"},
        {"Sector": "Puente Isaias Garrido", "lat": -4.9065, "lon": -80.6990, "Nivel": "Moderado", "Color": "orange", "Tipo": "Basura Ribereña"},
        {"Sector": "Zona Industrial", "lat": -4.9220, "lon": -80.6720, "Nivel": "Moderado", "Color": "orange", "Tipo": "Efluentes Industriales"},
        {"Sector": "Transversal Tarapaca", "lat": -4.8995, "lon": -80.6870, "Nivel": "Leve", "Color": "green", "Tipo": "Residuos Comerciales"}
    ])

df = obtener_datos()

col1, col2, col3 = st.columns(3)
col1.metric("Total Focos", len(df))
col2.metric("Criticos", len(df[df["Nivel"] == "Critico"]))
col3.metric("Moderados", len(df[df["Nivel"] == "Moderado"]))

st.subheader("Mapa de Focos Contaminantes")
mapa = folium.Map(location=[-4.9010, -80.6850], zoom_start=13)

for _, fila in df.iterrows():
    folium.Marker(
        location=[fila["lat"], fila["lon"]],
        popup=fila["Sector"],
        tooltip=fila["Sector"],
        icon=folium.Icon(color=fila["Color"])
    ).add_to(mapa)

st_folium(mapa, width=800, height=450)

st.subheader("Tabla de Registros")
st.dataframe(df[["Sector", "Nivel", "Tipo"]], use_container_width=True)
