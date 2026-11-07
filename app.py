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
            "Recomendación": "Instalación de contenedores diferenciados de reciclaje."
        }
    ])

df = obtener_datos_focos()

# 4. Panel Lateral con Adaptabilidad de Dispositivo
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/892/892926.png", width=80)
st.sidebar.title("ECO-MAPA Panel")

dispositivo = st.sidebar.radio(
    "💻 / 📱 Dispositivo de acceso:",
    ["Laptop / Computadora", "Smartphone / Celular"],
    index=0
)

if dispositivo == "Smartphone / Celular":
    st.warning("📱 **Aviso de visualización móvil:** Para visualizar los mapas interactivos y las tablas con la mejor cobertura de pantalla, gira tu dispositivo horizontalmente.")

st.sidebar.markdown("---")

niveles_seleccionados = st.sidebar.multiselect(
    "Filtrar por Gravedad:",
    options=["Crítico", "Moderado", "Leve"],
    default=["Crítico", "Moderado", "Leve"]
)

df_filtrado = df[df["Nivel"].isin(niveles_seleccionados)]

# 5. Encabezado principal
st.markdown("""
<div class="card-banner">
    <h1 style="color: #ffffff !important; margin: 0; font-weight: 800;">🌱 ECO-MAPA SULLANA</h1>
    <p style="color: #e8f5e9 !important; margin-top: 6px; font-size: 1.1rem;">Plataforma Integral de Diagnóstico, Monitoreo de Focos Críticos y Simulación Ambiental</p>
</div>
""", unsafe_allow_html=True)

# 6. Métricas de Resumen Visibles
col1, col2, col3, col4 = st.columns(4)
col1.metric("📍 Total Focos Monitorizados", len(df_filtrado))
col2.metric("🚨 Puntos Críticos", len(df_filtrado[df_filtrado["Nivel"] == "Crítico"]))
col3.metric("⚠️ Puntos Moderados", len(df_filtrado[df_filtrado["Nivel"] == "Moderado"]))
col4.metric("✅ Puntos Bajo Control", len(df_filtrado[df_filtrado["Nivel"] == "Leve"]))

st.markdown("---")

# 7. Pestañas Principales
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Mapa Interactivo", 
    "📊 Diagnóstico de Focos", 
    "📰 Noticias & Cobertura", 
    "⚡ Simulador de Impacto"
])

with tab1:
    col_mapa, col_detalle = st.columns([2, 1])
    
    with col_mapa:
        st.subheader("Ubicación Geográfica en Tiempo Real")
        mapa = folium.Map(location=[-4.9010, -80.6850], zoom_start=13, tiles="OpenStreetMap")
        
        for _, fila in df_filtrado.iterrows():
            html_popup = f"""
            <div style="font-family: Arial; width: 180px; color: #000000;">
                <h4 style="color:#1b5e20; margin-bottom:3px;">{fila['Sector']}</h4>
                <b>Estado:</b> <span style="color:{fila['Color']};">{fila['Nivel']}</span><br>
                <b>Tipo:</b> {fila['Tipo']}<br>
                <hr style="margin:5px 0;">
                <small>{fila['Residuos']}</small>
            </div>
            """
            folium.Marker(
                location=[fila["lat"], fila["lon"]],
                popup=folium.Popup(html_popup, max_width=220),
                tooltip=fila["Sector"],
                icon=folium.Icon(color=fila["Color"], icon="info-sign")
            ).add_to(mapa)
            
        # returned_objects=[] agiliza la respuesta al no intercambiar eventos pesados por cada movimiento del mapa
        st_folium(mapa, width="100%", height=450, returned_objects=[])
        
    with col_detalle:
        st.subheader("🔍 Ficha Técnica por Foco")
        foco_sel = st.selectbox("Selecciona un foco ambiental:", df_filtrado["Sector"].unique())
        info = df[df["Sector"] == foco_sel].iloc[0]
        
        st.info(f"**Categoría:** {info['Tipo']}\n\n**Nivel de Riesgo:** {info['Nivel']}")
        st.markdown(f"**🚨 Causas principales:**\n{info['Causas']}")
        st.markdown(f"**☣️ Impacto:**\n{info['Consecuencias']}")
        st.markdown(f"**🌱 Acción recomendada:**\n{info['Recomendación']}")

with tab2:
    st.subheader("📊 Matriz Completa de Evaluación Ambiental")
    st.dataframe(
        df_filtrado[["Sector", "Nivel", "Tipo", "Residuos", "Causas", "Consecuencias", "Recomendación"]],
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.subheader("📰 Portal Ambiental de Sullana")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="news-card"><h3>🌊 Cuenca Río Chira</h3><p>Reportes de contaminación y proyectos de recuperación ambiental.</p></div>', unsafe_allow_html=True)
        st.link_button("Noticias Río Chira", "https://www.google.com/search?q=noticias+rio+chira+sullana+contaminacion")
    with c2:
        st.markdown('<div class="news-card"><h3>🏙️ Canal Vía</h3><p>Estado de la infraestructura, limpieza y drenajes en Sullana.</p></div>', unsafe_allow_html=True)
        st.link_button("Noticias Canal Vía", "https://www.google.com/search?q=noticias+canal+via+sullana+basura")
    with c3:
        st.markdown('<div class="news-card"><h3>🚜 Botadero & Residuos</h3><p>Gestión de basura urbana y proyectos sanitarios provinciales.</p></div>', unsafe_allow_html=True)
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
