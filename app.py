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
    (
        "1. Ortogonalidad de Señales", 
        "2. Valores RMS y Promedio", 
        "3. Evaluación de Conceptos",
        "4. Circuitos RC y RL (Transitorios)"
    )
)

st.sidebar.markdown("---")
st.sidebar.info("Plataforma interactiva para el curso de Electrónica de Potencia.")

# --- Función de Descarga Universal ---
def preparar_descarga(dict_datos):
    df = pd.DataFrame(dict_datos)
    return df.to_csv(index=False).encode('utf-8-sig')

# ==========================================
# MÓDULO 1: ORTOGONALIDAD
# ==========================================
if tema == "1. Ortogonalidad de Señales":
    st.header("Módulo 1: Análisis de Ortogonalidad en CA")
    col_ctrl, col_graph = st.columns([1, 3])
    with col_ctrl:
        n = st.slider("Armónico Voltaje (n)", 1, 10, 1)
        m = st.slider("Armónico Corriente (m)", 1, 10, 2)
        phi = st.slider("Desfase (grados)", 0, 360, 0)
    
    t = np.linspace(0, 1, 1000)
    v = np.sin(2 * np.pi * n * t)
    i = np.sin(2 * np.pi * m * t + np.radians(phi))
    p = v * i
    p_avg = np.mean(p)

    fig1, ax1 = plt.subplots(2, 1, figsize=(10, 7))
    ax1[0].plot(t, v, label="v(t)"); ax1[0].plot(t, i, "--", label="i(t)")
    ax1[0].legend(); ax1[0].grid(True)
    ax1[1].plot(t, p, color="black", label="p(t)")
    ax1[1].fill_between(t, p, 0, where=(p>=0), color='green', alpha=0.3)
    ax1[1].fill_between(t, p, 0, where=(p<0), color='orange', alpha=0.3)
    ax1[1].axhline(p_avg, color='purple', linewidth=2, label=f'P_prom = {p_avg:.4f}')
    ax1[1].legend(); ax1[1].grid(True)
    
    with col_graph:
        st.pyplot(fig1)
        csv_m1 = preparar_descarga({'Tiempo[s]': t, 'V[V]': v, 'I[A]': i, 'P[W]': p})
        st.download_button("📥 Descargar Datos", csv_m1, "ortogonalidad.csv", "text/csv")

# ==========================================
# MÓDULO 2: VALORES RMS Y PROMEDIO
# ==========================================
elif tema == "2. Valores RMS y Promedio":
    st.header("Módulo 2: Cálculo de Valores Eficaces (RMS) y DC")
    tipo_onda = st.sidebar.selectbox("Forma de Onda", ("Senoidal", "Cuadrada", "Triangular", "Rectificada Media Onda", "Rectificada Onda Completa"))
    amp = st.sidebar.number_input("Amplitud [V]", value=10.0)
    freq = st.sidebar.number_input("Frecuencia [Hz]", value=60)
    
    t = np.linspace(0, 2/freq, 1000)
    w = 2 * np.pi * freq
    if tipo_onda == "Senoidal": y = amp * np.sin(w * t)
    elif tipo_onda == "Cuadrada": y = amp * square(w * t)
    elif tipo_onda == "Triangular": y = amp * sawtooth(w * t, width=0.5)
    elif tipo_onda == "Rectificada Media Onda": y = np.where(amp*np.sin(w*t)>0, amp*np.sin(w*t), 0)
    elif tipo_onda == "Rectificada Onda Completa": y = np.abs(amp * np.sin(w * t))
    
    v_prom, v_rms = np.mean(y), np.sqrt(np.mean(y**2))
    c1, c2 = st.columns(2)
    c1.metric("Valor Promedio (Vdc)", f"{v_prom:.3f} V")
    c2.metric("Valor RMS (Vrms)", f"{v_rms:.3f} V")
    
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(t, y, 'k'); ax2.axhline(v_prom, color='b', ls='--', label='V_dc'); ax2.axhline(v_rms, color='r', ls='-.', label='V_rms')
    ax2.legend(); ax2.grid(True); st.pyplot(fig2)
    
    csv_m2 = preparar_descarga({'T[s]': t, 'V[V]': y, 'Vdc': np.full_like(t, v_prom), 'Vrms': np.full_like(t, v_rms)})
    st.download_button("📥 Descargar Datos", csv_m2, "analisis_rms.csv", "text/csv")

# ==========================================
# MÓDULO 3: EVALUACIÓN
# ==========================================
elif tema == "3. Evaluación de Conceptos":
    st.header("📝 Autoevaluación")
    with st.form("examen"):
        q1 = st.radio("1. Si dos ondas tienen frecuencias diferentes (n=1, m=2), ¿su potencia promedio es?", ("Máxima", "Mínima", "Cero", "Igual al voltaje"))
        q2 = st.radio("2. En una onda senoidal pura de amplitud 10V, ¿el valor RMS es?", ("10 V", "7.07 V", "5 V", "0 V"))
        enviado = st.form_submit_button("Calificar")
        if enviado:
            res1 = "✅" if q1 == "Cero" else "❌"
            res2 = "✅" if q2 == "7.07 V" else "❌"
            st.write(f"Pregunta 1: {res1}"); st.write(f"Pregunta 2: {res2}")
            if q1 == "Cero" and q2 == "7.07 V": st.balloons()

# ==========================================
# MÓDULO 4: CIRCUITOS RC Y RL (TRANSITORIOS)
# ==========================================
elif tema == "4. Circuitos RC y RL (Transitorios)":
    st.header("Módulo 4: Respuesta Transitoria en Circuitos de Primer Orden")
    
    tipo_circuito = st.sidebar.selectbox("Configuración", ("RC Serie (Fuente V)", "RL Serie (Fuente V)", "RC Paralelo (Fuente I)"))
    
    col_p, col_g = st.columns([1, 3])
    with col_p:
        st.subheader("Parámetros")
        val_r = st.number_input("Resistencia R [Ω]", value=1000.0, step=100.0)
        if "RC" in tipo_circuito:
            val_c = st.number_input("Capacitancia C [µF]", value=100.0, step=10.0)
            tau = val_r * (val_c * 1e-6); label_tau = "RC"
        else:
            val_l = st.number_input("Inductancia L [mH]", value=100.0, step=10.0)
            tau = (val_l * 1e-3) / val_r; label_tau = "L/R"
        
        fuente = st.slider("Valor de la Fuente", 1, 50, 10)
        t = np.linspace(0, 5*tau, 1000)

    # Cálculo de respuesta
    if tipo_circuito == "RC Serie (Fuente V)":
        y = fuente * (1 - np.exp(-t/tau)); ylabel = "Voltaje en C [V]"
    elif tipo_circuito == "RL Serie (Fuente V)":
        y = (fuente/val_r) * (1 - np.exp(-t/tau)); ylabel = "Corriente en L [A]"
    elif tipo_circuito == "RC Paralelo (Fuente I)":
        y = (fuente * val_r) * (1 - np.exp(-t/tau)); ylabel = "Voltaje en Nodo [V]"

    with col_g:
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.plot(t*1000, y, 'r', lw=2, label="Respuesta")
        ax4.axvline(tau*1000, color='gray', ls='--', label=f'τ = {tau*1000:.2f}ms')
        ax4.set_xlabel("Tiempo [ms]"); ax4.set_ylabel(ylabel); ax4.legend(); ax4.grid(True)
        st.pyplot(fig4)
        
        # Tabla informativa
        st.write("**Valores clave en el tiempo:**")
        df_claves = pd.DataFrame({
            'Tiempo': ['1τ', '2τ', '3τ', '4τ', '5τ'],
            'Valor': [f"{y[np.abs(t-tau).argmin()]:.3f}", f"{y[np.abs(t-2*tau).argmin()]:.3f}", f"{y[np.abs(t-3*tau).argmin()]:.3f}", f"{y[np.abs(t-4*tau).argmin()]:.3f}", f"{y[np.abs(t-5*tau).argmin()]:.3f}"],
            '% del Final': ['63.2%', '86.5%', '95.0%', '98.2%', '99.3%']
        })
        st.table(df_claves)
