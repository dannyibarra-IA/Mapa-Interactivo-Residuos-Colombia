
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide", page_title="Mapa de Residuos en Colombia")

# Datos base
data = [
    {"Ciudad": "Bogotá D.C.", "Lat": 4.7110, "Lon": -74.0721, "Población": 7968095, "Disposición": 6270.48, "Aprovechamiento": 4710.86, "Tasa": 42.9, "Relleno": "Doña Juana"},
    {"Ciudad": "Medellín", "Lat": 6.2518, "Lon": -75.5636, "Población": 2653729, "Disposición": 1887.03, "Aprovechamiento": 322.60, "Tasa": 14.6, "Relleno": "La Pradera"},
    {"Ciudad": "Cali", "Lat": 3.4516, "Lon": -76.5319, "Población": 2297230, "Disposición": 1650.67, "Aprovechamiento": 129.63, "Tasa": 7.28, "Relleno": "Colomba - El Guabal"},
    {"Ciudad": "Barranquilla", "Lat": 10.9639, "Lon": -74.7964, "Población": 1327209, "Disposición": 1563.53, "Aprovechamiento": 191.02, "Tasa": 10.89, "Relleno": "Los Pocitos"},
    {"Ciudad": "Cartagena", "Lat": 10.3910, "Lon": -75.4794, "Población": 1065570, "Disposición": 1404.52, "Aprovechamiento": 22.61, "Tasa": 1.58, "Relleno": "Loma de los Cocos"},
    {"Ciudad": "Soacha", "Lat": 4.5793, "Lon": -74.2144, "Población": 831259, "Disposición": 475.28, "Aprovechamiento": 160.84, "Tasa": 25.28, "Relleno": "Nuevo Mondoñedo"},
    {"Ciudad": "Cúcuta", "Lat": 7.8891, "Lon": -72.4967, "Población": 795608, "Disposición": 703.66, "Aprovechamiento": 22.23, "Tasa": 3.06, "Relleno": "Guayabal"},
    {"Ciudad": "Soledad", "Lat": 10.9184, "Lon": -74.7673, "Población": 692799, "Disposición": 591.13, "Aprovechamiento": 33.74, "Tasa": 5.40, "Relleno": "Los Pocitos"},
    {"Ciudad": "Bucaramanga", "Lat": 7.1193, "Lon": -73.1227, "Población": 623378, "Disposición": 500.17, "Aprovechamiento": 20.06, "Tasa": 3.86, "Relleno": "El Carrasco"},
    {"Ciudad": "Bello", "Lat": 6.3389, "Lon": -75.5628, "Población": 578376, "Disposición": 330.61, "Aprovechamiento": 66.76, "Tasa": 16.80, "Relleno": "La Pradera"}
]
df = pd.DataFrame(data)

# Sidebar
st.sidebar.title("Filtros")
ciudades_seleccionadas = st.sidebar.multiselect("Selecciona ciudades", df["Ciudad"].tolist(), default=df["Ciudad"].tolist())
umbral_500 = st.sidebar.checkbox("Solo mostrar ciudades con > 500 toneladas/día")
umbral_1000 = st.sidebar.checkbox("Mostrar ciudades con > 1000 toneladas/día")
umbral_2000 = st.sidebar.checkbox("Mostrar ciudades con > 2000 toneladas/día")

# Filtro de datos
df_filtrado = df[df["Ciudad"].isin(ciudades_seleccionadas)]
if umbral_500:
    df_filtrado = df_filtrado[df_filtrado["Disposición"] > 500]
if umbral_1000:
    df_filtrado = df_filtrado[df_filtrado["Disposición"] > 1000]
if umbral_2000:
    df_filtrado = df_filtrado[df_filtrado["Disposición"] > 2000]

# Layout principal
st.title("📍 Mapa de Residuos en las 10 Ciudades más Pobladas de Colombia")
st.subheader("📊 Resumen de ciudades seleccionadas")
st.dataframe(df_filtrado[["Ciudad", "Disposición", "Aprovechamiento", "Tasa"]], use_container_width=True)

# Crear mapa
mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=6, tiles="CartoDB positron")
for _, row in df_filtrado.iterrows():
    info = f"<b>{row['Ciudad']}</b><br>Disposición: {row['Disposición']} ton/día<br>Aprovechamiento: {row['Aprovechamiento']} ton/día<br>Tasa: {row['Tasa']}%<br>Relleno: {row['Relleno']}"
    color = "green" if row["Tasa"] > 20 else "orange" if row["Tasa"] > 10 else "red"
    folium.CircleMarker(
        location=[row["Lat"], row["Lon"]],
        radius=10,
        color="blue",
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(info, max_width=250),
        tooltip=row["Ciudad"]
    ).add_to(mapa)

# Mostrar mapa
folium_static(mapa)

# Leyenda visual
with st.expander("🖍️ Ver leyenda de colores"):
    st.markdown("- 🔴 **Rojo**: Tasa de aprovechamiento < 10%")
    st.markdown("- 🟠 **Naranja**: Tasa de aprovechamiento entre 10% y 20%")
    st.markdown("- 🟢 **Verde**: Tasa de aprovechamiento > 20%")
