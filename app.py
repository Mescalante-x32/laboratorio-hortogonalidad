import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Configuración de la Página ---
st.set_page_config(page_title="Calculadora RMS/Promedio", layout="wide")
st.title("⚡ Calculadora Dinámica de Valor Promedio y RMS")
st.markdown("""
Esta herramienta calcula y grafica los valores fundamentales de diferentes formas de onda periódicas.
Utilice la barra lateral para seleccionar la señal y sus parámetros.
""")

# --- Barra Lateral (Controles) ---
st.sidebar.header("Parámetros de la Señal")
tipo_onda = st.sidebar.selectbox(
    "Tipo de Onda",
    ("Senoidal", "Cuadrada Simétrica", "Triangular", "Rectificada Media Onda", "Rectificada Onda Completa")
)

amplitud = st.sidebar.slider("Amplitud (A)", 0.1, 100.0, 10.0, step=0.1)
frecuencia = st.sidebar.slider("Frecuencia (f) [Hz]", 1, 120, 60)
offset_dc = st.sidebar.slider("Offset DC ($V_{dc}$)", -50.0, 50.0, 0.0, step=0.1)

# --- Cálculos y Generación de Datos ---
t = np.linspace(0, 2/frecuencia, 1000) # Graficar 2 periodos
omega = 2 * np.pi * frecuencia

if tipo_onda == "Senoidal":
    y = amplitud * np.sin(omega * t) + offset_dc
    
elif tipo_onda == "Cuadrada Simétrica":
    from scipy.signal import square
    y = amplitud * square(omega * t) + offset_dc
    
elif tipo_onda == "Triangular":
    from scipy.signal import sawtooth
    y = amplitud * sawtooth(omega * t, width=0.5) + offset_dc

elif tipo_onda == "Rectificada Media Onda":
    y_pure = amplitud * np.sin(omega * t)
    y = np.where(y_pure > 0, y_pure, 0) + offset_dc

elif tipo_onda == "Rectificada Onda Completa":
    y = np.abs(amplitud * np.sin(omega * t)) + offset_dc

# --- Cálculos Numéricos de Promedio y RMS ---
# Promedio (Media): (1/T) * integral(y dt)
valor_promedio = np.mean(y)

# RMS (Root Mean Square): sqrt( (1/T) * integral(y^2 dt) )
valor_rms = np.sqrt(np.mean(y**2))

# --- Sección de Resultados (Métricas) ---
st.header("Resultados")
col1, col2, col3 = st.columns(3)
col1.metric(label="Forma de Onda", value=tipo_onda)
col2.metric(label="Valor Promedio (DC)", value=f"{valor_promedio:.3f} V")
col3.metric(label="Valor eficaz (RMS)", value=f"{valor_rms:.3f} V")

# --- Sección de Gráficas ---
st.header("Análisis Gráfico")

fig, ax = plt.subplots(figsize=(10, 5))

# Graficar la señal principal
ax.plot(t, y, color='black', label=f'Señal: {tipo_onda}', linewidth=2)

# Graficar las líneas de referencia
ax.axhline(valor_promedio, color='blue', linestyle='--', linewidth=2, label=f'Promedio = {valor_promedio:.2f}')
ax.axhline(valor_rms, color='red', linestyle='-.', linewidth=2, label=f'RMS = {valor_rms:.2f}')

# Configuración de ejes
ax.set_title(f"Visualización de {tipo_onda} con {frecuencia}Hz", fontsize=14)
ax.set_xlabel("Tiempo [s]", fontsize=12)
ax.set_ylabel("Amplitud [V]", fontsize=12)
ax.grid(True, which='both', linestyle='--', alpha=0.5)
ax.legend(loc='upper right')

# Mostrar la gráfica en Streamlit
st.pyplot(fig)
