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
        "4. Circuitos RC y RL (Transitorios)",
        "5. Circuitos CA (Carga R-L)",
        "6. Corrección del Factor de Potencia",
        "7. Parámetros No Sinusoidales",
        "8. Autoevaluación de CA y Armónicos"
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

# ==========================================
# MÓDULO 5: CIRCUITOS CA (CARGA R-L)
# ==========================================
elif tema == "5. Circuitos CA (Carga R-L)":
    st.header("Módulo 5: Análisis de Circuitos CA en Carga Serie R-L")
    st.write("Análisis de voltajes, corrientes y potencias en régimen permanente.")

    with st.sidebar:
        st.subheader("Parámetros del Circuito")
        V_rms = st.number_input("Voltaje de Fuente (Vrms)", value=120.0, step=10.0)
        f = st.number_input("Frecuencia (Hz)", value=60.0, step=1.0)
        R = st.number_input("Resistencia R [Ω]", value=10.0, min_value=0.1)
        L_mH = st.number_input("Inductancia L [mH]", value=20.0, min_value=0.1)

    # --- Cálculos Eléctricos ---
    L = L_mH / 1000
    w = 2 * np.pi * f
    XL = w * L
    Z_mag = np.sqrt(R**2 + XL**2)
    phi_rad = np.arctan2(XL, R)
    phi_deg = np.degrees(phi_rad)
    
    # Valores de Corriente y Potencia
    I_rms = V_rms / Z_mag
    S = V_rms * I_rms         # Potencia Aparente [VA]
    P = S * np.cos(phi_rad)    # Potencia Activa [W]
    Q = S * np.sin(phi_rad)    # Potencia Reactiva [VAR]
    FP = np.cos(phi_rad)       # Factor de Potencia
    
    # --- Métricas de Resultados ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Impedancia |Z|", f"{Z_mag:.2f} Ω")
    c2.metric("Ángulo φ", f"{phi_deg:.1f}°")
    c3.metric("I rms", f"{I_rms:.2f} A")
    c4.metric("Factor de Potencia", f"{FP:.3f}")

    c5, c6, c7 = st.columns(3)
    c5.metric("Potencia Activa (P)", f"{P:.1f} W")
    c6.metric("Potencia Reactiva (Q)", f"{Q:.1f} VAR")
    c7.metric("Potencia Aparente (S)", f"{S:.1f} VA")

    # --- Generación de Gráficas ---
    t = np.linspace(0, 2/f, 1000) # 2 ciclos
    V_pico = V_rms * np.sqrt(2)
    I_pico = I_rms * np.sqrt(2)
    
    v_t = V_pico * np.sin(w * t)
    i_t = I_pico * np.sin(w * t - phi_rad)
    
    # Voltajes en componentes
    vr_t = i_t * R
    vl_t = I_pico * XL * np.sin(w * t - phi_rad + np.pi/2)

    st.subheader("Formas de Onda Instantáneas")
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    ax5.plot(t*1000, v_t, 'b', label="v(t) Fuente", lw=2)
    ax5.plot(t*1000, i_t * (V_pico/I_pico * 0.5), 'r--', label="i(t) (Escalada)")
    ax5.plot(t*1000, vl_t, 'g:', label="v_L(t) Inductor")
    ax5.set_xlabel("Tiempo [ms]"); ax5.set_ylabel("Amplitud"); ax5.legend(); ax5.grid(True)
    st.pyplot(fig5)

    # --- Triángulo de Potencias (Visualización Pedagógica) ---
    st.subheader("Triángulo de Potencias")
    fig6, ax6 = plt.subplots(figsize=(4, 4))
    ax6.quiver(0, 0, P, 0, angles='xy', scale_units='xy', scale=1, color='b', label='P (W)')
    ax6.quiver(P, 0, 0, Q, angles='xy', scale_units='xy', scale=1, color='g', label='Q (VAR)')
    ax6.quiver(0, 0, P, Q, angles='xy', scale_units='xy', scale=1, color='r', label='S (VA)')
    ax6.set_xlim(0, S*1.1); ax6.set_ylim(0, S*1.1); ax6.grid(True); ax6.legend()
    st.pyplot(fig6)

    # --- Descarga de Datos ---
    datos_m5 = {
        'Tiempo [s]': t, 'v_fuente [V]': v_t, 'i_total [A]': i_t, 
        'v_resistencia [V]': vr_t, 'v_inductor [V]': vl_t
    }
    st.download_button("📥 Descargar Datos CA", preparar_descarga(datos_m5), "circuito_ca_rl.csv")

# ==========================================
# MÓDULO 6: CORRECCIÓN DEL FACTOR DE POTENCIA
# ==========================================
elif tema == "6. Corrección del Factor de Potencia":
    st.header("Módulo 6: Corrección del Factor de Potencia (Carga R-L + C paralelo)")
    st.write("Simulación de compensación de potencia reactiva mediante capacitores en paralelo.")

    with st.sidebar:
        st.subheader("Carga Original (R-L)")
        V_rms_6 = st.number_input("Voltaje Fuente [Vrms]", value=120.0, key="v6")
        f_6 = st.number_input("Frecuencia [Hz]", value=60.0, key="f6")
        R_6 = st.number_input("Resistencia R [Ω]", value=20.0, min_value=0.1, key="r6")
        L_6_mH = st.number_input("Inductancia L [mH]", value=100.0, min_value=0.1, key="l6")
        
        st.subheader("Compensación")
        C_comp_uF = st.slider("Capacitancia de Compensación [µF]", 0.0, 500.0, 0.0, step=10.0)

    # --- Cálculos Carga Original ---
    w6 = 2 * np.pi * f_6
    XL_6 = w6 * (L_6_mH / 1000)
    Z_L = complex(R_6, XL_6)
    I_L = V_rms_6 / abs(Z_L)
    
    P_L = (I_L**2) * R_6
    Q_L = (I_L**2) * XL_6
    phi_original = np.arctan2(Q_L, P_L)
    FP_original = np.cos(phi_original)

    # --- Cálculos Compensación ---
    XC_6 = 1 / (w6 * (C_comp_uF * 1e-6)) if C_comp_uF > 0 else float('inf')
    Q_C = (V_rms_6**2) / XC_6 if C_comp_uF > 0 else 0
    
    Q_total = Q_L - Q_C
    S_total = np.sqrt(P_L**2 + Q_total**2)
    I_fuente = S_total / V_rms_6
    phi_nuevo = np.arctan2(Q_total, P_L)
    FP_nuevo = np.cos(phi_nuevo)

    # --- Interfaz de Resultados ---
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Estado Original")
        st.metric("FP Inicial", f"{FP_original:.3f}")
        st.metric("Corriente Total", f"{I_L:.2f} A")
        st.metric("Q Original", f"{Q_L:.1f} VAR")
    
    with col_b:
        st.subheader("Estado Compensado")
        st.metric("FP Final", f"{FP_nuevo:.3f}", delta=f"{FP_nuevo-FP_original:.3f}")
        st.metric("Corriente Fuente", f"{I_fuente:.2f} A", delta=f"{I_fuente-I_L:.2f}", delta_color="inverse")
        st.metric("Q Neto", f"{Q_total:.1f} VAR")

    # --- Gráfica de Fasores de Corriente ---
    st.subheader("Diagrama Fasorial de Corrientes")
    # Fasores: I_L (atraso), I_C (adelanto 90°), I_fuente (suma)
    i_l_complex = I_L * np.exp(-1j * phi_original)
    i_c_complex = (V_rms_6 / XC_6) * 1j if C_comp_uF > 0 else 0j
    i_total_complex = i_l_complex + i_c_complex

    fig7, ax7 = plt.subplots(figsize=(6, 6))
    ax7.quiver(0, 0, i_l_complex.real, i_l_complex.imag, angles='xy', scale_units='xy', scale=1, color='red', label='I_carga (R-L)')
    if C_comp_uF > 0:
        ax7.quiver(i_l_complex.real, i_l_complex.imag, i_c_complex.real, i_c_complex.imag, angles='xy', scale_units='xy', scale=1, color='blue', label='I_capacitor')
    ax7.quiver(0, 0, i_total_complex.real, i_total_complex.imag, angles='xy', scale_units='xy', scale=1, color='black', lw=2, label='I_fuente (Total)')
    
    limit = max(I_L, I_fuente) * 1.2
    ax7.set_xlim(-limit/4, limit); ax7.set_ylim(-limit, limit/4)
    ax7.axhline(0, color='gray', lw=1); ax7.axvline(0, color='gray', lw=1)
    ax7.grid(True, linestyle='--'); ax7.legend(); ax7.set_title("Compensación de Corriente")
    st.pyplot(fig7)

    st.info(f"👉 **Efecto:** Al agregar {C_comp_uF} µF, la corriente que la fuente debe suministrar bajó de {I_L:.2f}A a {I_fuente:.2f}A.")

    # --- Descarga de Datos ---
    datos_m6 = {
        'Capacitancia [uF]': [C_comp_uF], 'FP_Original': [FP_original], 'FP_Nuevo': [FP_nuevo],
        'I_Carga [A]': [I_L], 'I_Fuente_Compensada [A]': [I_fuente], 'P [W]': [P_L], 'Q_Neto [VAR]': [Q_total]
    }
    st.download_button("📥 Descargar Reporte de Compensación", preparar_descarga(datos_m6), "compensacion_fp.csv")

# ==========================================
# MÓDULO 7: PARÁMETROS NO SINUSOIDALES
# ==========================================
elif tema == "7. Parámetros No Sinusoidales":
    st.header("Módulo 7: Análisis bajo Condiciones No Sinusoidales")
    st.write("Estudio de distorsión armónica y potencias (P, Q, S, D) en sistemas no lineales.")

    with st.sidebar:
        st.subheader("Configuración de Señal")
        V_rms_7 = st.number_input("Voltaje Fuente (Sinusoidal) [Vrms]", value=120.0)
        I1_rms = st.number_input("Corriente Fundamental [Arms]", value=10.0)
        
        st.markdown("---")
        st.subheader("Contenido Armónico (Corriente)")
        h3 = st.slider("3er Armónico (%)", 0, 100, 30) / 100
        h5 = st.slider("5to Armónico (%)", 0, 100, 20) / 100
        h7 = st.slider("7mo Armónico (%)", 0, 100, 10) / 100
        phi1_deg = st.slider("Desfase Fundamental (grados)", -90, 90, 30)

    # --- Cálculos de Corriente RMS ---
    phi1_rad = np.radians(phi1_deg)
    I3_rms = I1_rms * h3
    I5_rms = I1_rms * h5
    I7_rms = I1_rms * h7
    
    # Corriente RMS Total (Teorema de Parseval)
    I_total_rms = np.sqrt(I1_rms**2 + I3_rms**2 + I5_rms**2 + I7_rms**2)
    THD_i = np.sqrt(I3_rms**2 + I5_rms**2 + I7_rms**2) / I1_rms
    
    # --- CÁLCULOS DE POTENCIA ---
    # Nota: Si V es puramente sinusoidal, solo la corriente fundamental produce Potencia Activa y Reactiva.
    P_7 = V_rms_7 * I1_rms * np.cos(phi1_rad)    # Potencia Activa [W]
    Q_7 = V_rms_7 * I1_rms * np.sin(phi1_rad)    # Potencia Reactiva [VAR]
    S_7 = V_rms_7 * I_total_rms                  # Potencia Aparente Total [VA]
    
    # Potencia de Distorsión (D)
    # S^2 = P^2 + Q^2 + D^2  =>  D = sqrt(S^2 - P^2 - Q^2)
    D_7 = np.sqrt(max(0, S_7**2 - P_7**2 - Q_7**2))
    
    # Factores de Potencia
    FP_desplazamiento = np.cos(phi1_rad)         # DPF (cos phi)
    FP_verdadero = P_7 / S_7                     # True PF
    
    # --- Interfaz de Resultados ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Potencia Activa (P)", f"{P_7:.1f} W")
    col2.metric("Potencia Reactiva (Q)", f"{Q_7:.1f} VAR")
    col3.metric("Potencia Aparente (S)", f"{S_7:.1f} VA")

    col4, col5, col6 = st.columns(3)
    col4.metric("Potencia Distorsión (D)", f"{D_7:.1f} VAD")
    col5.metric("FP Desplazamiento", f"{FP_desplazamiento:.3f}")
    col6.metric("FP Verdadero (PF)", f"{FP_verdadero:.3f}")

    # --- Gráficas ---
    t = np.linspace(0, 2/60, 1000)
    w = 2 * np.pi * 60
    v_t = V_rms_7 * np.sqrt(2) * np.sin(w * t)
    i_total_t = (I1_rms * np.sqrt(2) * np.sin(w * t - phi1_rad) + 
                 I3_rms * np.sqrt(2) * np.sin(3 * w * t) + 
                 I5_rms * np.sqrt(2) * np.sin(5 * w * t) + 
                 I7_rms * np.sqrt(2) * np.sin(7 * w * t))

    st.subheader("Análisis Visual")
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        fig_t = plt.figure(figsize=(8, 5))
        plt.plot(t*1000, v_t/V_rms_7, 'b', alpha=0.3, label="v(t) norm")
        plt.plot(t*1000, i_total_t, 'r', lw=2, label="i_total(t)")
        plt.title("Formas de Onda"); plt.legend(); plt.grid(True); plt.xlabel("ms")
        st.pyplot(fig_t)
    
    with c_g2:
        # Gráfica de barras de corrientes RMS
        fig_s = plt.figure(figsize=(8, 5))
        plt.bar(['Funda.', '3ro', '5to', '7mo'], [I1_rms, I3_rms, I5_rms, I7_rms], color='orange')
        plt.title("Espectro de Corriente (RMS)"); plt.ylabel("Amperios")
        st.pyplot(fig_s)

    # --- Descarga de Datos ---
    datos_m7 = {
        'Tiempo [s]': t, 'v_t [V]': v_t, 'i_t [A]': i_total_t,
        'P [W]': [P_7]*1000, 'Q [VAR]': [Q_7]*1000, 'S [VA]': [S_7]*1000, 'D [VAD]': [D_7]*1000
    }
    st.download_button("📥 Descargar Reporte Armónico", preparar_descarga(datos_m7), "analisis_armonico.csv")

# ==========================================
# MÓDULO 8: AUTOEVALUACIÓN DE CA Y ARMÓNICOS
# ==========================================
elif tema == "8. Autoevaluación de CA y Armónicos":
    st.header("📝 Examen de Afianzamiento: Circuitos en CA")
    st.write("Mida su comprensión sobre los conceptos de los Módulos 5, 6 y 7.")

    with st.form("examen_ca"):
        # --- Pregunta 1 ---
        st.subheader("1. Impedancia R-L")
        q1 = st.radio(
            "En un circuito R-L serie, si la frecuencia de la fuente aumenta, ¿qué sucede con la magnitud de la impedancia total |Z|?",
            ("Disminuye", "Se mantiene igual", "Aumenta", "Se vuelve cero")
        )

        # --- Pregunta 2 ---
        st.subheader("2. Desfase V-I")
        q2 = st.radio(
            "En una carga inductiva pura, ¿cuál es la relación de fase entre voltaje y corriente?",
            ("La corriente adelanta al voltaje 90°", "El voltaje adelanta a la corriente 90°", "Están en fase", "El voltaje adelanta 180°")
        )

        # --- Pregunta 3 ---
        st.subheader("3. Factor de Potencia (FP)")
        q3 = st.radio(
            "Un factor de potencia de 0.7 en atraso indica que la carga es predominantemente:",
            ("Capacitiva", "Resistiva pura", "Inductiva", "No lineal")
        )

        # --- Pregunta 4 ---
        st.subheader("4. Compensación de FP")
        q4 = st.radio(
            "Al colocar un capacitor en paralelo con una carga R-L, ¿qué componente de la potencia se reduce desde la perspectiva de la fuente?",
            ("Potencia Activa (P)", "Potencia Reactiva (Q)", "Ambas (P y Q)", "Ninguna")
        )

        # --- Pregunta 5 ---
        st.subheader("5. Potencia Activa en Armónicos")
        q5 = st.radio(
            "Si el voltaje es una senoidal pura de 60Hz y la corriente tiene un 3er armónico (180Hz), ¿cuánta potencia activa produce ese 3er armónico?",
            ("Proporcional a su amplitud", "El triple que la fundamental", "Cero", "Depende del valor eficaz")
        )

        # --- Pregunta 6 ---
        st.subheader("6. Potencia de Distorsión (D)")
        q6 = st.radio(
            "¿En qué condición aparece el término de Potencia de Distorsión (D) en el balance de potencias?",
            ("Siempre que hay inductores", "Solo cuando hay capacitores", "Cuando existen armónicos en V o I", "En circuitos de CD")
        )

        # --- Pregunta 7 ---
        st.subheader("7. THD y Factor de Potencia")
        q7 = st.radio(
            "Si el THD de corriente aumenta pero el desfase de la fundamental se mantiene igual, el Factor de Potencia Verdadero:",
            ("Aumenta", "Disminuye", "Se mantiene igual", "No se puede determinar")
        )

        # --- Pregunta 8 ---
        st.subheader("8. Cálculo de RMS")
        q8 = st.radio(
            "Si una corriente tiene una fundamental de 10A (RMS) y un 3er armónico de 10A (RMS), ¿cuál es el valor RMS total?",
            ("20 A", "10 A", "14.14 A (sqrt(10^2 + 10^2))", "0 A")
        )

        # --- Pregunta 9 ---
        st.subheader("9. Triángulo de Potencias")
        q9 = st.radio(
            "¿Qué representa la hipotenusa en el triángulo de potencias clásico (sin armónicos)?",
            ("Potencia Activa (P)", "Potencia Reactiva (Q)", "Potencia Aparente (S)", "Factor de Potencia")
        )

        # --- Pregunta 10 ---
        st.subheader("10. Efecto de la Compensación en la Corriente")
        q10 = st.radio(
            "¿Por qué es deseable corregir el Factor de Potencia en una planta industrial?",
            ("Para aumentar el consumo de Watts", "Para reducir la corriente total y las pérdidas en conductores", "Para aumentar el voltaje de red", "Para eliminar los armónicos")
        )

        # Botón de envío
        enviado = st.form_submit_button("Finalizar y Calificar")

        if enviado:
            aciertos = 0
            respuestas = [
                (q1, "Aumenta", "XL = 2*pi*f*L, si f sube, XL sube."),
                (q2, "El voltaje adelanta a la corriente 90°", "ELI the ICE man: en L (Inductor), E (Voltaje) adelanta a I."),
                (q3, "Inductiva", "'Atraso' siempre refiere a que la corriente se queda atrás del voltaje."),
                (q4, "Potencia Reactiva (Q)", "El capacitor suministra los VARs que la bobina necesita."),
                (q5, "Cero", "La ortogonalidad indica que frecuencias distintas no producen potencia neta."),
                (q6, "Cuando existen armónicos en V o I", "D surge de la distorsión no lineal."),
                (q7, "Disminuye", "PF = (I1/Irms) * DPF. Si THD sube, Irms sube y PF baja."),
                (q8, "14.14 A (sqrt(10^2 + 10^2))", "Uso del teorema de Parseval para valores RMS."),
                (q9, "Potencia Aparente (S)", "S = sqrt(P^2 + Q^2)."),
                (q10, "Para reducir la corriente total y las pérdidas en conductores", "Menos corriente significa conductores más delgados y menos multas.")
            ]

            st.markdown("---")
            for i, (resp, correcta, explicacion) in enumerate(respuestas):
                if resp == correcta:
                    st.success(f"Pregunta {i+1}: Correcto. {explicacion}")
                    aciertos += 1
                else:
                    st.error(f"Pregunta {i+1}: Incorrecto. La respuesta era '{correcta}'. {explicacion}")
            
            puntuacion = (aciertos / 10) * 100
            st.metric("Tu Calificación Final", f"{puntuacion}%")
            if aciertos >= 8:
                st.balloons()
                st.write("¡Excelente dominio de CA!")
