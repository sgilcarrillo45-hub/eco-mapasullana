import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# 1. Configuración de página
st.set_page_config(
    page_title="ECO-MAPA | Monitoreo Ambiental Sullana",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS de Alto Contraste (Cuerpo y Panel Lateral Forzados a Claro)
st.markdown("""
    <style>
    /* Forzar fondo blanco y texto oscuro global */
    .stApp, [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #111111 !important;
    }
    
    /* Forzar textos del Sidebar a color visible */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
        color: #111111 !important;
        font-weight: 600 !important;
    }
    
    /* Textos principales del cuerpo */
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #111111 !important;
    }
    
    /* Banner principal */
    .card-banner {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Tarjetas de métricas */
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
    
    /* Pestañas */
    button[data-baseweb="tab"] p {
        color: #222222 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    button[aria-selected="true"] p {
        color: #1b5e20 !important;
    }

    /* Noticias */
    .news-card {
        background-color: #f4f6f4;
        border-left: 5px solid #1b5e20;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Almacenamiento en Caché para Optimizar Velocidad de Carga
@st.cache_data
def obtener_datos_focos():
    return pd.DataFrame([
        {
            "Sector": "Río Chira - Puente Turicarami",
            "lat": -4.9042, "lon": -80.6975,
            "Tipo": "Contaminación Hídrica y Plásticos",
            "Nivel": "Crítico", "Color": "red",
            "Residuos": "Plásticos PET, bolsas, basura doméstica",
            "Causas": "Vertimiento libre de residuos urbanos y arrastre de corriente.",
            "Consecuencias": "Eutrofización del agua y riesgo biológico en cuenca.",
            "Recomendación": "Colocación de bio-barreras fluviales y patrullaje de campo."
        },
        {
            "Sector": "Canal Vía - Barrio Leticia",
            "lat": -4.8981, "lon": -80.6864,
            "Tipo": "Aguas Residuales y Residuos Sólidos",
            "Nivel": "Crítico", "Color": "red",
            "Residuos": "Aguas servidas, plásticos duros, desmonte",
            "Causas": "Estancamiento por pendiente deficiente y colapso de desagües.",
            "Consecuencias": "Emisión de gases H2S, plagas de mosquitos y olores fétidos.",
            "Recomendación": "Limpieza mecanizada continua y encajonamiento técnico."
        },
        {
            "Sector": "Botadero Municipal - Carretera Tambogrande",
            "lat": -4.8850, "lon": -80.6420,
            "Tipo": "Quema de Basura y Suelo",
            "Nivel": "Crítico", "Color": "red",
            "Residuos": "Basura mixta, llantas, residuos peligrosos",
            "Causas": "Acopio informal a cielo abierto sin compactado técnico.",
            "Consecuencias": "Generación de lixiviados al subsuelo y humo tóxico.",
            "Recomendación": "Clausura progresiva y conversión a Relleno Sanitario."
        },
        {
            "Sector": "Mercado Modelo Sullana",
            "lat": -4.9015, "lon": -80.6882,
            "Tipo": "Residuos Orgánicos Comerciales",
            "Nivel": "Crítico", "Color": "red",
            "Residuos": "Restos orgánicos, empaques, vísceras",
            "Causas": "Comercio informal disperso y recolección a destiempo.",
            "Consecuencias": "Foco infeccioso y vectores en zonas de comida.",
            "Recomendación": "Implementación de ruta de compostaje y acopio exclusivo."
        },
        {
            "Sector": "Camal Municipal de Sullana",
            "lat": -4.9120, "lon": -80.6795,
            "Tipo": "Efluentes Orgánicos de Faenado",
            "Nivel": "Moderado", "Color": "orange",
            "Residuos": "Sangre, lodos orgánicos, grasas",
            "Causas": "Falta de planta de tratamiento pre-vertido.",
            "Consecuencias": "Saturación del alcantarillado y malos olores locales.",
            "Recomendación": "Instalación de biodigestores y trampas de grasa industrial."
        },
        {
            "Sector": "Canal Vía - Sector Bellavista",
            "lat": -4.8912, "lon": -80.6810,
            "Tipo": "Residuos Urbanos e Inertes",
            "Nivel": "Crítico", "Color": "red",
            "Residuos": "Escombros de construcción, plásticos",
            "Causas": "Disposición clandestina de materiales por vehículos menores.",
            "Consecuencias": "Obstrucción del flujo hidráulico ante lluvias.",
            "Recomendación": "Fiscalización con cámaras y multas por arrojo de escombros."
        },
        {
            "Sector": "Urb. Santa Rosa - Zonas Descampadas",
            "lat": -4.9150, "lon": -80.6910,
            "Tipo": "Acumulación Doméstica",
            "Nivel": "Moderado", "Color": "orange",
            "Residuos": "Bolsas de basura, maleza, cartones",
            "Causas": "Baja frecuencia de paso del camión recolector.",
            "Consecuencias": "Microbotaderos informales en esquinas comunitarias.",
            "Recomendación": "Reestructuración de horarios de rutas nocturnas."
        },
        {
            "Sector": "Puente Isaías Garrido (Viejo)",
            "lat": -4.9065, "lon": -80.6990,
            "Tipo": "Contaminación de Rivera",
            "Nivel": "Moderado", "Color": "orange",
            "Residuos": "Empaques descartables, matorrales quemados",
            "Causas": "Afluencia turística/comercial sin tachos integrados.",
            "Consecuencias": "Deterioro paisajístico e impacto ribereño.",
            "Recomendación": "Puntos limpios ecológicos y señalética ambiental."
        },
        {
            "Sector": "Zona Industrial - Salida a Piura",
            "lat": -4.9220, "lon": -80.6720,
            "Tipo": "Efluentes Industriales",
            "Nivel": "Moderado", "Color": "orange",
            "Residuos": "Agua residual procesada, empaques masivos",
            "Causas": "Descargas puntuales sin monitoreo en tiempo real.",
            "Consecuencias": "Degradación del suelo periférico.",
            "Recomendación": "Auditorías ambientales periódicas a empresas operadoras."
        },
        {
            "Sector": "Transversal Tarapacá - Zona Comercial",
            "lat": -4.8995, "lon": -80.6870,
            "Tipo": "Residuos Sólidos Urbanos",
            "Nivel": "Leve", "Color": "green",
            "Residuos": "Papeles, botellas de plástico, envoltorios",
            "Causas": "Tránsito peatonal elevado en horario comercial.",
            "Consecuencias": "Suciedad visual y desbordes puntuales de depósitos.",
            "Recomend
