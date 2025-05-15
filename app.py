import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Escenarios Prospectivos de Residuos")

# Parámetros
anios = np.arange(2023, 2044)
tasa_crecimiento = 0.012
g_pc_dia = 0.74  # kg/hab/día
g_pc_anual = g_pc_dia * 365 / 1000  # ton/hab/año

# Datos base
ciudades = {
    "Bogotá D.C.": {"Poblacion": 7968095, "TA_inicial": 0.4290},
    "Medellín": {"Poblacion": 2653729, "TA_inicial": 0.1460},
    "Cali": {"Poblacion": 2297230, "TA_inicial": 0.0782},
    "Barranquilla": {"Poblacion": 1327209, "TA_inicial": 0.1089},
    "Cartagena": {"Poblacion": 1065570, "TA_inicial": 0.0158},
    "Soacha": {"Poblacion": 831259, "TA_inicial": 0.2528},
    "Cúcuta": {"Poblacion": 795608, "TA_inicial": 0.0306},
    "Soledad": {"Poblacion": 692799, "TA_inicial": 0.0540},
    "Bucaramanga": {"Poblacion": 623378, "TA_inicial": 0.0386},
    "Bello": {"Poblacion": 578376, "TA_inicial": 0.1680}
}

composicion = {
    "Orgánicos": 0.47,
    "Plásticos": 0.12,
    "Vidrios": 0.04,
    "Textiles": 0.02
}

# Sidebar
st.sidebar.title("Escenarios Prospectivos por Ciudad")
seleccion_ciudad = None
for ciudad in ciudades:
    if st.sidebar.button(f"Simular {ciudad}"):
        seleccion_ciudad = ciudad

if seleccion_ciudad:
    # Simulación para la ciudad seleccionada
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

    # Visualización
    st.title("🔮 Escenarios Prospectivos de Aprovechamiento de Residuos")
    st.subheader(f"📍 Ciudad: {seleccion_ciudad} | Periodo: 2023–2043")

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

    with st.expander("🖍️ Leyenda de colores"):
        st.markdown("- 🔴 **Rojo**: Tasa < 10% (no aplica si está fuera del umbral)")
        st.markdown("- 🟠 **Naranja**: Tasa entre 10% y 20%")
        st.markdown("- 🟢 **Verde**: Tasa > 20%")
        st.markdown("Todas las gráficas usan el mismo color para armonía visual.")
else:
    st.title("📊 Escenarios Prospectivos de Residuos")
    st.write("Selecciona una ciudad en el panel izquierdo para ver su proyección de aprovechamiento de residuos.")
