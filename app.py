import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square, sawtooth
import pandas as pd

# --- Configuración Global ---
st.set_page_config(page_title="Laboratorio Dr. Escalante", layout="wide")

# --- Menú de Navegación Lateral ---
st.sidebar.title("📚 Temario del Curso")
tema = st.sidebar.radio(
    "Seleccione el Módulo:",
    ("1. Ortogonalidad de Señales", "2. Valores RMS y Promedio")
)

st.sidebar.markdown("---")
st.sidebar.info("Desarrollado para el curso de Electrónica de Potencia Aplicada.")

# --- NUEVA FUNCIÓN DE DESCARGA FLEXIBLE ---
def preparar_descarga(dict_datos):
    """
    Recibe un diccionario donde las llaves son los nombres de las columnas
    y los valores son los arreglos de datos (numpy arrays).
    """
    df = pd.DataFrame(dict_datos)
    # 'utf-8-sig' permite que Excel reconozca el formato inmediatamente
    return df.to_csv(index=False).encode('utf-8-sig')

# ==========================================
# MÓDULO 1: ORTOGONALIDAD
# ==========================================
if tema == "1. Ortogonalidad de Señales":
    st.header("Módulo 1: Análisis de Ortogonalidad en CA")
    
    col_ctrl, col_graph = st.columns([1, 3])
    
    with col_ctrl:
        n = st.slider("Frecuencia Voltaje (n)", 1, 10, 1)
        m = st.slider("Frecuencia Corriente (m)", 1, 10, 2)
        phi = st.slider("Desfase (grados)", 0, 360, 0)
    
    t = np.linspace(0, 1, 1000)
    v = np.sin(2 * np.pi * n * t)
    i = np.sin(2 * np.pi * m * t + np.radians(phi))
    p = v * i
    p_avg = np.mean(p)

    fig, ax = plt.subplots(2, 1, figsize=(10, 7))
    ax[0].plot(t, v, label="v(t)")
    ax[0].plot(t, i, label="i(t)", linestyle="--")
    ax[0].legend(); ax[0].grid(True)
    
    ax[1].plot(t, p, color="black", label="p(t)")
    ax[1].fill_between(t, p, 0, where=(p>=0), color='green', alpha=0.3)
    ax[1].fill_between(t, p, 0, where=(p<0), color='orange', alpha=0.3)
    ax[1].axhline(p_avg, color='purple', linewidth=2, label=f'P_prom = {p_avg:.4f}')
    ax[1].legend(); ax[1].grid(True)
    
    with col_graph:
        st.pyplot(fig)
        
        # PREPARAR TODAS LAS COLUMNAS PARA EL MÓDULO 1
        datos_m1 = {
            'Tiempo [s]': t,
            'Voltaje [V]': v,
            'Corriente [A]': i,
            'Potencia_Instantanea [W]': p
        }
        csv_m1 = preparar_descarga(datos_m1)
        
        st.download_button(
            label="📥 Descargar Laboratorio Completo (v, i, p) en CSV",
            data=csv_m1,
            file_name='analisis_ortogonalidad_completo.csv',
            mime='text/csv',
        )

# ==========================================
# MÓDULO 2: VALORES RMS Y PROMEDIO
# ==========================================
elif tema == "2. Valores RMS y Promedio":
    st.header("Módulo 2: Cálculo de Valores Eficaces (RMS) y DC")
    
    tipo_onda = st.sidebar.selectbox(
        "Forma de Onda",
        ("Senoidal", "Cuadrada", "Triangular", "Rectificada Media Onda", "Rectificada Onda Completa")
    )
    
    amp = st.sidebar.number_input("Amplitud [V]", value=10.0)
    freq = st.sidebar.number_input("Frecuencia [Hz]", value=60)
    
    t = np.linspace(0, 2/freq, 1000)
    w = 2 * np.pi * freq
    
    if tipo_onda == "Senoidal": y = amp * np.sin(w * t)
    elif tipo_onda == "Cuadrada": y = amp * square(w * t)
    elif tipo_onda == "Triangular": y = amp * sawtooth(w * t, width=0.5)
    elif tipo_onda == "Rectificada Media Onda": y = np.where(amp*np.sin(w*t) > 0, amp*np.sin(w*t), 0)
    elif tipo_onda == "Rectificada Onda Completa": y = np.abs(amp * np.sin(w * t))
    
    v_prom = np.mean(y)
    v_rms = np.sqrt(np.mean(y**2))
    
    c1, c2 = st.columns(2)
    c1.metric("Valor Promedio (Vdc)", f"{v_prom:.3f} V")
    c2.metric("Valor RMS (Vrms)", f"{v_rms:.3f} V")
    
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(t, y, color='black', linewidth=2)
    ax2.axhline(v_prom, color='blue', linestyle='--', label=f'V_dc = {v_prom:.2f}')
    ax2.axhline(v_rms, color='red', linestyle='-.', label=f'V_rms = {v_rms:.2f}')
    ax2.legend(); ax2.grid(True)
    st.pyplot(fig2)
    
    # PREPARAR DATOS PARA EL MÓDULO 2
    # Aquí incluimos la señal y los valores calculados como columnas constantes para referencia
    datos_m2 = {
        'Tiempo [s]': t,
        'Amplitud_Onda [V]': y,
        'Referencia_DC [V]': np.full_like(t, v_prom),
        'Referencia_RMS [V]': np.full_like(t, v_rms)
    }
    csv_m2 = preparar_descarga(datos_m2)
    
    st.download_button(
        label=f"📥 Descargar Datos de {tipo_onda} (CSV)",
        data=csv_m2,
        file_name=f'analisis_{tipo_onda.lower()}.csv',
        mime='text/csv',
    )
