import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(
    page_title="ECO-MAPA | Monitoreo Ambiental Sullana",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
        color: #111111 !important;
        font-weight: 600 !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #111111 !important;
    }
    .card-banner {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetricValue"] > div {
        color: #1b5e20 !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
    }
    div[data-testid="stMetricLabel"] > label {
        color: #333333 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    button[data-baseweb="tab"] p {
        color: #222222 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    button[aria-selected="true"] p {
        color: #1b5e20 !important;
    }
    .news-card {
        background-color: #f4f6f4;
        border-left: 5px solid #1b5e20;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def obtener_datos_focos():
    datos = [
        {
            "Sector": "Rio Chira - Puente Turicarami",
            "lat": -4.9042, "lon": -80.6975,
            "Tipo": "Contaminacion Hidrica y Plasticos",
            "Nivel": "Critico", "Color": "red",
            "Residuos": "Plasticos PET, bolsas, basura domestica",
            "Causas": "Vertimiento libre de residuos urbanos y arrastre de corriente.",
            "Consecuencias": "Eutrofizacion del agua y riesgo biologico en cuenca.",
            "Recomendacion": "Colocacion de bio-barreras fluviales y patrullaje de campo."
        },
        {
            "Sector": "Canal Via - Barrio Leticia",
            "lat": -4.8981, "lon": -80.6864,
            "Tipo": "Aguas Residuales y Residuos Solidos",
            "Nivel": "Critico", "Color": "red",
            "Residuos": "Aguas servidas, plasticos duros, desmonte",
            "Causas": "Estancamiento por pendiente deficiente y colapso de desagues.",
            "Consecuencias": "Emision de gases H2S, plagas de mosquitos y olores fetidos.",
            "Recomendacion": "Limpieza mecanizada continua y encajonamiento tecnico."
        },
        {
            "Sector": "Botadero Municipal - Carretera Tambogrande",
            "lat": -4.8850, "lon": -80.6420,
            "Tipo": "Quema de Basura y Suelo",
            "Nivel": "Critico", "Color": "red",
            "Residuos": "Basura mixta, llantas, residuos peligrosos",
            "Causas": "Acopio informal a cielo abierto sin compactado tecnico.",
            "Consecuencias": "Generacion de lixiviados al subsuelo y humo toxico.",
            "Recomendacion": "Clausura progresiva y conversion a Relleno Sanitario."
        },
        {
            "Sector": "Mercado Modelo Sullana",
            "lat": -4.9015, "lon": -80.6882,
            "Tipo": "Residuos Organicos Comerciales",
            "Nivel": "Critico", "Color": "red",
            "Residuos": "Restos organicos, empaques, visceras",
            "Causas": "Comercio informal disperso y recoleccion a destiempo.",
            "Consecuencias": "Foco infeccioso y vectores en zonas de comida.",
            "Recomendacion": "Implementacion de ruta de compostaje y acopio exclusivo."
        },
        {
            "Sector": "Camal Municipal de Sullana",
            "lat": -4.9120, "lon": -80.6795,
            "Tipo": "Efluentes Organicos de Faenado",
            "Nivel": "Moderado", "Color": "orange",
            "Residuos": "Sangre, lodos organicos, grasas",
            "Causas": "Falta de planta de tratamiento pre-vertido.",
            "Consecuencias": "Saturacion del alcantarillado y malos olores locales.",
            "Recomendacion": "Instalacion de biodigestores y trampas de grasa industrial."
        },
        {
            "Sector": "Canal Via - Sector Bellavista",
            "lat": -4.8912, "lon": -80.6810,
            "Tipo": "Residuos Urbanos e Inertes",
            "Nivel": "Critico", "Color": "red",
            "Residuos": "Escombros de construccion, plasticos",
            "Causas": "Disposicion clandestina de materiales por vehiculos menores.",
            "Consecuencias": "Obstruccion del flujo hidraulico ante lluvias.",
            "Recomendacion": "Fiscalizacion con camaras y multas por arrojo de escombros."
        },
        {
            "Sector": "Urb. Santa Rosa - Zonas Descampadas",
            "lat": -4.9150, "lon": -80.6910,
            "Tipo": "Acumulacion Domestica",
            "Nivel": "Moderado", "Color": "orange",
            "Residuos": "Bolsas de basura, maleza, cartones",
            "Causas": "Baja frecuencia de paso del camion recolector.",
            "Consecuencias": "Microbotaderos informales en esquinas comunitarias.",
            "Recomendacion": "Reestructuracion de horarios de rutas nocturnas."
        },
        {
            "Sector": "Puente Isaias Garrido (Viejo)",
            "lat": -4.9065, "lon": -80.6990,
            "Tipo": "Contaminacion de Rivera",
            "Nivel": "Moderado", "Color": "orange",
            "Residuos": "Empaques descartables, matorrales quemados",
            "Causas": "Afluencia turistica/comercial sin tachos integrados.",
            "Consecuencias": "Deterioro paisajistico e impacto ribereño.",
            "Recomendacion": "Puntos limpios ecologicos y señaletica ambiental."
        },
        {
            "Sector": "Zona Industrial - Salida a Piura",
            "lat": -4.9220, "lon": -80.6720,
            "Tipo": "Efluentes Industriales",
            "Nivel": "Moderado", "Color": "orange",
            "Residuos": "Agua residual procesada, empaques masivos",
            "Causas": "Descargas puntuales sin monitoreo en tiempo real.",
            "Consecuencias": "Degradacion del suelo periferico.",
            "Recomendacion": "Auditorias ambientales periodicas a empresas operadoras."
        },
        {
            "Sector": "Transversal Tarapaca - Zona Comercial",
            "lat": -4.8995, "lon": -80.6870,
            "Tipo": "Residuos Solidos Urbanos",
            "Nivel": "Leve", "Color": "green",
            "Residuos": "Papeles, botellas de plastico, envoltorios",
            "Causas": "Transito peatonal elevado en horario comercial.",
            "Consecuencias": "Suciedad visual y desbordes puntuales de depositos.",
            "Recomendacion": "Instalacion de contenedores diferenciados de reciclaje."
        }
    ]
    return pd.DataFrame(datos)

df = obtener_datos_focos()

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/892/892926.png", width=80)
st.sidebar.title("ECO-MAPA Panel")

dispositivo = st.sidebar.radio(
    "Dispositivo de acceso:",
    ["Laptop / Computadora", "Smartphone / Celular"],
    index=0
)

if dispositivo == "Smartphone / Celular
