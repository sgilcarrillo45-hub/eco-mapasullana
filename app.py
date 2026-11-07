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
st.write("Plataforma Integral de Diagnostico, Monitoreo de Focos Criticos y Simulacion Ambiental")

@st.cache_data
def obtener_datos_focos():
    return pd.DataFrame([
        {"Sector": "Rio Chira - Puente Turicarami", "lat": -4.9042, "lon": -80.6975, "Tipo": "Contaminacion Hidrica", "Nivel": "Critico", "Color": "red", "Residuos": "Plasticos PET, bolsas, basura doméstica", "Causas": "Vertimiento libre de residuos urbanos", "Consecuencias": "Eutrofizacion del agua", "Recomendacion": "Bio-barreras fluviales y patrullaje"},
        {"Sector": "Canal Via - Barrio Leticia", "lat": -4.8981, "lon": -80.6864, "Tipo": "Aguas Residuales", "Nivel": "Critico", "Color": "red", "Residuos": "Aguas servidas, plasticos duros", "Causas": "Estancamiento por pendiente deficiente", "Consecuencias": "Gases H2S y plagas de mosquitos", "Recomendacion": "Limpieza mecanizada continua"},
        {"Sector": "Botadero Municipal", "lat": -4.8850, "lon": -80.6420, "Tipo": "Quema de Basura", "Nivel": "Critico", "Color": "red", "Residuos": "Basura mixta, llantas, residuos peligrosos", "Causas": "Acopio informal a cielo abierto", "Consecuencias": "Lixiviados al subsuelo y humo toxico", "Recomendacion": "Conversion a Relleno Sanitario"},
        {"Sector": "Mercado Modelo Sullana", "lat": -4.9015, "lon": -80.6882, "Tipo": "Residuos Organicos", "Nivel": "Critico", "Color": "red", "Residuos": "Restos organicos, empaques, visceras", "Causas": "Comercio informal disperso", "Consecuencias": "Foco infeccioso y vectores", "Recomendacion": "Ruta de compostaje y acopio exclusivo"},
        {"Sector": "Camal Municipal", "lat": -4.9120, "lon": -80.6795, "Tipo": "Efluentes Organicos", "Nivel": "Moderado", "Color": "orange", "Residuos": "Sangre, lodos organicos, grasas", "Causas": "Falta de planta de tratamiento pre-vertido", "Consecuencias": "Saturacion de alcantarillado", "Recomendacion": "Biodigestores y trampas de grasa"},
        {"Sector": "Canal Via - Bellavista", "lat": -4.8912, "lon": -80.6810, "Tipo": "Residuos Inertes", "Nivel": "Critico", "Color": "red", "Residuos": "Escombros de construccion, plasticos", "Causas": "Disposicion clandestina de materiales", "Consecuencias": "Obstruccion del flujo hidraulico", "Recomendacion": "Fiscalizacion con camaras y multas"},
        {"Sector": "Urb. Santa Rosa", "lat": -4.9150, "lon": -80.6910, "Tipo": "Acumulacion Domestica", "Nivel": "Moderado", "Color": "orange", "Residuos": "Bolsas de basura, maleza, cartones", "Causas": "Baja frecuencia de camion recolector", "Consecuencias": "Microbotaderos informales", "Recomendacion": "Reestructuracion de horarios nocturnos"},
        {"Sector": "Puente Isaias Garrido", "lat": -4.9065, "lon": -80.6990, "Tipo": "Contaminacion Ribereña", "Nivel": "Moderado", "Color": "orange", "Residuos": "Empaques descartables, matorrales", "Causas": "Afluencia turistica/comercial sin tachos", "Consecuencias": "Deterioro paisajistico", "Recomendacion": "Puntos limpios ecologicos"},
        {"Sector": "Zona Industrial", "lat": -4.9220, "lon": -80.6720, "Tipo": "Efluentes Industriales", "Nivel": "Moderado", "Color": "orange", "Residuos": "Agua residual procesada, empaques", "Causas": "Descargas sin monitoreo en tiempo real", "Consecuencias": "Degradacion del suelo periferico", "Recomendacion": "Auditorias ambientales periodicas"},
        {"Sector": "Transversal Tarapaca", "lat": -4.8995, "lon": -80.6870, "Tipo": "Residuos Urbanos", "Nivel": "Leve", "Color": "green", "Residuos": "Papeles, botellas, envoltorios", "Causas": "Transito peatonal elevado", "Consecuencias": "Suciedad visual y desbordes", "Recomendacion": "Contenedores diferenciados"}
    ])

df = obtener_datos_focos()

# Metricas principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Focos", len(df))
col2.metric("Criticos", len(df[df["Nivel"] == "Critico"]))
col3.metric("Moderados", len(df[df["Nivel"] == "Moderado"]))
col4.metric("Bajo Control", len(df[df["Nivel"] == "Leve"]))

st.markdown("---")

# Las 4 Pestañas Requeridas
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Mapa Interactivo", 
    "📊 Diagnóstico de Focos", 
    "📰 Noticias & Cobertura", 
    "⚡ Simulador de Impacto"
])

with tab1:
    col_mapa, col_detalle = st.columns([2, 1])
    with col_mapa:
        st.subheader("Ubicacion Geografica")
        mapa = folium.Map(location=[-4.9010, -80.6850], zoom_start=13)
        for _, fila in df.iterrows():
            folium.Marker(
                location=[fila["lat"], fila["lon"]],
                popup=fila["Sector"],
                tooltip=fila["Sector"],
                icon=folium.Icon(color=fila["Color"])
            ).add_to(mapa)
        st_folium(mapa, width="100%", height=450, returned_objects=[])
        
    with col_detalle:
        st.subheader("🔍 Ficha Tecnica")
        foco_sel = st.selectbox("Selecciona un foco:", df["Sector"].unique())
        info = df[df["Sector"] == foco_sel].iloc[0]
        st.info(f"**Tipo:** {info['Tipo']}\n\n**Nivel:** {info['Nivel']}")
        st.markdown(f"**Causas:** {info['Causas']}")
        st.markdown(f"**Impacto:** {info['Consecuencias']}")
        st.markdown(f"**Accion:** {info['Recomendacion']}")

with tab2:
    st.subheader("📊 Matriz Completa de Evaluacion Ambiental")
    st.dataframe(df[["Sector", "Nivel", "Tipo", "Residuos", "Causas", "Consecuencias", "Recomendacion"]], use_container_width=True, hide_index=True)

with tab3:
    st.subheader("📰 Portal de Noticias Ambiental Sullana")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🌊 Cuenca Rio Chira")
        st.write("Reportes de contaminacion y proyectos ambientalistas.")
        st.link_button("Noticias Rio Chira", "https://www.google.com/search?q=noticias+rio+chira+sullana+contaminacion")
    with c2:
        st.markdown("### 🏙️ Canal Via")
        st.write("Estado de la infraestructura y limpieza en Sullana.")
        st.link_button("Noticias Canal Via", "https://www.google.com/search?q=noticias+canal+via+sullana+basura")
    with c3:
        st.markdown("### 🚜 Botadero & Residuos")
        st.write("Gestion de basura urbana y proyectos sanitarios.")
        st.link_button("Noticias Botadero", "https://www.google.com/search?q=noticias+botadero+municipal+sullana")

with tab4:
    st.subheader("⚡ Simulador Estratégico de Reducción de Impacto")
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        dias = st.slider("Frecuencia de recolección semanal (Días):", 1, 7, 4)
        educacion = st.slider("Porcentaje de participación ciudadana (%):", 10, 100, 50)
    with col_sim2:
        recol_eficiente = round((dias * 9.5) + (educacion * 0.45), 1)
        st.metric("Estimación de Reducción de Contaminante", f"{recol_eficiente}%")
        st.progress(min(int(recol_eficiente), 100))
        st.caption("Cálculo proyectado basado en frecuencia operativa y respuesta comunitaria.")
