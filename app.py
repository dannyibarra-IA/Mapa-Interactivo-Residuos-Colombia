
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide", page_title="Escenarios Prospectivos de Residuos")

# Datos y parámetros
anios = np.arange(2023, 2044)
tasa_crecimiento = 0.012
g_pc_dia = 0.74  # kg/hab/día
g_pc_anual = g_pc_dia * 365 / 1000  # ton/hab/año

ciudades = {
    "Bogotá D.C.": {"Poblacion": 7968095, "TA_inicial": 0.4290, "Lat": 4.7110, "Lon": -74.0721},
    "Medellín": {"Poblacion": 2653729, "TA_inicial": 0.1460, "Lat": 6.2518, "Lon": -75.5636},
    "Cali": {"Poblacion": 2297230, "TA_inicial": 0.0782, "Lat": 3.4516, "Lon": -76.5319},
    "Barranquilla": {"Poblacion": 1327209, "TA_inicial": 0.1089, "Lat": 10.9639, "Lon": -74.7964},
    "Cartagena": {"Poblacion": 1065570, "TA_inicial": 0.0158, "Lat": 10.3910, "Lon": -75.4794},
    "Soacha": {"Poblacion": 831259, "TA_inicial": 0.2528, "Lat": 4.5793, "Lon": -74.2144},
    "Cúcuta": {"Poblacion": 795608, "TA_inicial": 0.0306, "Lat": 7.8891, "Lon": -72.4967},
    "Soledad": {"Poblacion": 692799, "TA_inicial": 0.0540, "Lat": 10.9184, "Lon": -74.7673},
    "Bucaramanga": {"Poblacion": 623378, "TA_inicial": 0.0386, "Lat": 7.1193, "Lon": -73.1227},
    "Bello": {"Poblacion": 578376, "TA_inicial": 0.1680, "Lat": 6.3389, "Lon": -75.5628}
}

composicion = {
    "Orgánicos": 0.47,
    "Plásticos": 0.12,
    "Vidrios": 0.04,
    "Textiles": 0.02
}

# MAPA
st.title("🗺️ Mapa de ciudades con datos de aprovechamiento")
mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=6, tiles="CartoDB positron")

for ciudad, datos in ciudades.items():
    info = f"<b>{ciudad}</b><br>Población: {datos['Poblacion']:,}<br>Tasa inicial de aprovechamiento: {datos['TA_inicial']*100:.1f}%"
    folium.CircleMarker(
        location=[datos["Lat"], datos["Lon"]],
        radius=8,
        color="blue",
        fill=True,
        fill_color="green" if datos["TA_inicial"] > 0.2 else "orange" if datos["TA_inicial"] > 0.1 else "red",
        fill_opacity=0.7,
        popup=folium.Popup(info, max_width=250),
        tooltip=ciudad
    ).add_to(mapa)

folium_static(mapa)

# LEYENDA
with st.expander("🖍️ Leyenda de colores"):
    st.markdown("- 🔴 **Rojo**: Tasa < 10%")
    st.markdown("- 🟠 **Naranja**: Tasa entre 10% y 20%")
    st.markdown("- 🟢 **Verde**: Tasa > 20%")

# SIMULACIÓN
st.sidebar.title("Escenarios Prospectivos por Ciudad")
seleccion_ciudad = None
for ciudad in ciudades:
    if st.sidebar.button(f"Simular {ciudad}"):
        seleccion_ciudad = ciudad

if seleccion_ciudad:
    df_ciudad = pd.DataFrame(index=anios, columns=composicion.keys())
    poblacion = ciudades[seleccion_ciudad]["Poblacion"]
    ta = ciudades[seleccion_ciudad]["TA_inicial"]

    for anio in anios:
        poblacion_anio = poblacion * ((1 + tasa_crecimiento) ** (anio - 2023))
        if anio % 5 == 3 and anio != 2023:
            if seleccion_ciudad == "Bogotá D.C.":
                ta = min(ta + 0.10, 1.0)
            elif ta < 0.20:
                ta = min(ta * 2, 1.0)

        for tipo, fraccion in composicion.items():
            total_residuos = poblacion_anio * g_pc_anual * fraccion
            df_ciudad.loc[anio, tipo] = total_residuos * ta

    df_ciudad = df_ciudad.astype(float)

    st.header(f"📈 Simulación 2023–2043: {seleccion_ciudad}")
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))
    axs = axs.ravel()

    for i, tipo in enumerate(composicion.keys()):
        axs[i].plot(df_ciudad.index, df_ciudad[tipo], color="green", linewidth=2)
        axs[i].set_title(f"Aprovechamiento de {tipo}", fontsize=10)
        axs[i].set_xlabel("Año")
        axs[i].set_ylabel("Toneladas")
        axs[i].grid(True)

    plt.tight_layout()
    st.pyplot(fig)
