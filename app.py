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
        "8. Autoevaluación de CA y Armónicos",
        "9. Rectificador de Media Onda (R-L)",
        "10. Diodo de Marcha Libre (Freewheeling)",
        "11. Efecto de Inductancia de Línea",
        "12. Onda Completa con Filtro C y Ls",
        "13. Onda Completa con Filtro L-C",
        "14. Filtro Tipo Pi (C-L-C)",
        "15. Autoevaluación: Rectificadores"
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

# ==========================================
# MÓDULO 9: RECTIFICADOR DE MEDIA ONDA (R-L)
# ==========================================
elif tema == "9. Rectificador de Media Onda (R-L)":
    st.header("Módulo 9: Rectificador de Media Onda con Carga Resistiva-Inductiva")
    st.write("Análisis del efecto de la inductancia en el ángulo de conducción del diodo.")

    with st.sidebar:
        st.subheader("Parámetros de Entrada")
        Vm_9 = st.number_input("Voltaje Pico de Fuente (Vm)", value=170.0)
        f_9 = st.number_input("Frecuencia [Hz]", value=60.0, key="f9")
        R_9 = st.number_input("Resistencia R [Ω]", value=10.0, min_value=1.0)
        L_9_mH = st.number_input("Inductancia L [mH]", value=20.0, min_value=0.0)

    # --- Cálculos del Rectificador ---
    w9 = 2 * np.pi * f_9
    L_9 = L_9_mH / 1000
    Z_9 = np.sqrt(R_9**2 + (w9*L_9)**2)
    phi_9 = np.arctan2(w9*L_9, R_9) # Ángulo de impedancia
    
    # Encontrar beta (ángulo de extinción) numéricamente
    # i(beta) = (Vm/Z) * [sin(beta - phi) + sin(phi)*exp(-beta/(w*tau))] = 0
    tau_9 = L_9 / R_9
    def ecuacion_corriente(ang):
        return np.sin(ang - phi_9) + np.sin(phi_9) * np.exp(-ang / (w9 * tau_9))

    # Buscamos beta entre pi y 2*pi
    angulos_busqueda = np.linspace(np.pi + 0.01, 2*np.pi - 0.01, 500)
    beta = np.pi + 0.5 # Valor por defecto
    for a in angulos_busqueda:
        if ecuacion_corriente(a) < 0:
            beta = a
            break

    # --- Generación de Ondas ---
    theta = np.linspace(0, 2*np.pi, 1000)
    t_9 = theta / w9
    v_s = Vm_9 * np.sin(theta)
    
    # Corriente instantánea i(t)
    i_t = np.zeros_like(theta)
    indices_conduccion = np.where(theta <= beta)[0]
    i_t[indices_conduccion] = (Vm_9 / Z_9) * (np.sin(theta[indices_conduccion] - phi_9) + 
                                              np.sin(phi_9) * np.exp(-theta[indices_conduccion] / (w9 * tau_9)))
    
    # Voltaje en la carga v_o(t)
    v_o = np.where(theta <= beta, v_s, 0)
    
    # --- Parámetros de Salida ---
    V_dc_9 = (Vm_9 / (2*np.pi)) * (1 - np.cos(beta))
    I_dc_9 = V_dc_9 / R_9
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ángulo φ (Impedancia)", f"{np.degrees(phi_9):.2f}°")
    col2.metric("Ángulo β (Extinción)", f"{np.degrees(beta):.2f}°")
    col3.metric("Voltaje CD Promedio", f"{V_dc_9:.2f} V")

    # --- Gráficas ---
    fig10, (ax_v, ax_i) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax_v.plot(theta, v_s, 'gray', linestyle='--', alpha=0.5, label="v_source(t)")
    ax_v.plot(theta, v_o, 'b', lw=2, label="v_output(t)")
    ax_v.axvline(beta, color='r', ls=':', label=f'β = {np.degrees(beta):.1f}°')
    ax_v.set_ylabel("Voltaje [V]"); ax_v.legend(); ax_v.grid(True)
    
    ax_i.plot(theta, i_t, 'r', lw=2, label="i_output(t)")
    ax_i.set_ylabel("Corriente [A]"); ax_i.set_xlabel("Fase [rad]"); ax_i.legend(); ax_i.grid(True)
    
    st.pyplot(fig10)

    st.info(f"💡 **Observación Pedagógica:** Note que aunque el voltaje de fuente cruza por cero en π (180°), la corriente continúa hasta β debido a la energía almacenada en el inductor. En el intervalo entre π y β, el voltaje de salida es negativo.")

    # --- Descarga de Datos ---
    datos_m9 = {'Fase [rad]': theta, 'V_fuente [V]': v_s, 'V_carga [V]': v_o, 'I_carga [A]': i_t}
    st.download_button("📥 Descargar Datos de Rectificación", preparar_descarga(datos_m9), "rectificador_media_onda.csv")

# ==========================================
# MÓDULO 10: DIODO DE MARCHA LIBRE
# ==========================================
elif tema == "10. Diodo de Marcha Libre (Freewheeling)":
    st.header("Módulo 10: Rectificador con Diodo de Marcha Libre")
    st.write("Efecto de la conmutación de corriente entre el diodo rectificador y el diodo de marcha libre.")

    with st.sidebar:
        st.subheader("Parámetros de Diseño")
        Vm_10 = st.number_input("Voltaje Pico Fuente [V]", value=170.0, key="vm10")
        f_10 = st.number_input("Frecuencia [Hz]", value=60.0, key="f10")
        R_10 = st.number_input("Resistencia R [Ω]", value=10.0, key="r10")
        L_10_mH = st.number_input("Inductancia L [mH]", value=50.0, key="l10")

    # --- Cálculos ---
    w10 = 2 * np.pi * f_10
    L_10 = L_10_mH / 1000
    tau_10 = L_10 / R_10
    
    theta = np.linspace(0, 2*np.pi, 1000)
    v_s = Vm_10 * np.sin(theta)
    
    # Corriente en el primer intervalo (0 a pi): Diodo principal conduce
    Z_10 = np.sqrt(R_10**2 + (w10*L_10)**2)
    phi_10 = np.arctan2(w10*L_10, R_10)
    
    i_t = np.zeros_like(theta)
    v_o = np.zeros_like(theta)
    
    # Simulación por intervalos
    for i, th in enumerate(theta):
        if th <= np.pi:
            # Diodo principal conduce, Vo = Vs
            v_o[i] = v_s[i]
            i_t[i] = (Vm_10 / Z_10) * (np.sin(th - phi_10) + np.sin(phi_10) * np.exp(-th / (w10 * tau_10)))
        else:
            # Diodo de marcha libre conduce, Vo = 0
            v_o[i] = 0
            # Corriente decae exponencialmente desde el valor en pi
            I_pi = (Vm_10 / Z_10) * (np.sin(np.pi - phi_10) + np.sin(phi_10) * np.exp(-np.pi / (w10 * tau_10)))
            i_t[i] = I_pi * np.exp(-(th - np.pi) / (w10 * tau_10))

    # --- Resultados ---
    V_dc_10 = Vm_10 / np.pi
    I_dc_10 = V_dc_10 / R_10
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Voltaje CD (Teórico)", f"{V_dc_10:.2f} V")
    c2.metric("Corriente CD (Promedio)", f"{I_dc_10:.2f} A")
    c3.metric("Constante de Tiempo τ", f"{tau_10*1000:.2f} ms")

    # --- Gráficas ---
    fig11, (ax_v, ax_i) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax_v.plot(theta, v_s, 'gray', ls='--', alpha=0.4, label="v_fuente(t)")
    ax_v.plot(theta, v_o, 'b', lw=2, label="v_output(t)")
    ax_v.fill_between(theta, v_o, 0, color='blue', alpha=0.1)
    ax_v.set_ylabel("Voltaje [V]"); ax_v.legend(); ax_v.grid(True)
    
    ax_i.plot(theta, i_t, 'r', lw=2, label="i_carga(t)")
    ax_i.set_ylabel("Corriente [A]"); ax_i.set_xlabel("Fase [rad]"); ax_i.legend(); ax_i.grid(True)
    
    st.pyplot(fig11)

    st.success(f"✅ **Conclusión Pedagógica:** Observe que el voltaje de salida ya no tiene la parte negativa del módulo anterior. La corriente es más suave (menos rizado) porque el inductor descarga su energía a través del diodo de marcha libre durante todo el semiciclo negativo.")

# ==========================================
# MÓDULO 11: EFECTO DE L_s (CORRIENTE CONSTANTE)
# ==========================================
elif tema == "11. Efecto de Inductancia de Línea":
    st.header("Módulo 11: Inductancia de Línea con Corriente de Carga Constante")
    st.write("Análisis del fenómeno de conmutación asumiendo una carga altamente inductiva ($L \\to \\infty$).")

    with st.sidebar:
        st.subheader("Parámetros del Sistema")
        Vm_11 = st.number_input("Voltaje Pico Fuente [V]", value=170.0, key="vm11_s")
        f_11 = st.number_input("Frecuencia [Hz]", value=60.0, key="f11_s")
        Ls_mH = st.slider("Inductancia de Línea Ls [mH]", 0.1, 15.0, 5.0, step=0.1)
        Id_11 = st.number_input("Corriente de Carga Constante (Id) [A]", value=10.0)

    # --- Cálculos de Conmutación ---
    w11 = 2 * np.pi * f_11
    Ls = Ls_mH / 1000
    
    # En media onda monofásica con Id constante:
    # El diodo no conduce instantáneamente. La corriente sube de 0 a Id
    # siguiendo la ecuación: Ls*(di/dt) = Vm*sin(wt)
    # Integrando: i(wt) = (Vm / (w*Ls)) * (1 - cos(wt))
    
    # Hallamos el ángulo de conmutación 'u' donde i(u) = Id
    # cos(u) = 1 - (Id * w * Ls) / Vm
    val_cos_u = 1 - (Id_11 * w11 * Ls) / Vm_11
    
    if val_cos_u < -1:
        st.error("⚠️ La caída inductiva es excesiva: la corriente Id no puede alcanzarse con esta Ls.")
        u_rad = np.pi
    else:
        u_rad = np.arccos(val_cos_u)
    
    u_deg = np.degrees(u_rad)
    
    # Caída de voltaje promedio (V_gamma)
    # V_gamma = (w * Ls * Id) / (2 * pi)  <-- Para media onda
    V_gamma = (w11 * Ls * Id_11) / (2 * np.pi)
    V_dc_ideal = Vm_11 / np.pi
    V_dc_real = V_dc_ideal - V_gamma

    # --- Resultados ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Ángulo de Conmutación (u)", f"{u_deg:.2f}°")
    c2.metric("Caída de Voltaje (ΔV)", f"{V_gamma:.2f} V")
    c3.metric("Vdc Real en Carga", f"{V_dc_real:.2f} V")

    # --- Generación de Gráficas ---
    theta = np.linspace(0, 2*np.pi, 1000)
    v_s = Vm_11 * np.sin(theta)
    
    v_o = np.zeros_like(theta)
    i_s = np.zeros_like(theta)
    
    for i, th in enumerate(theta):
        if th < u_rad:
            # Intervalo de conmutación: i sube, Vo = 0 (diodo principal en conmutación)
            v_o[i] = 0
            i_s[i] = (Vm_11 / (w11 * Ls)) * (1 - np.cos(th))
        elif u_rad <= th <= np.pi:
            # Conducción plena: Vo = Vs, i = Id
            v_o[i] = v_s[i]
            i_s[i] = Id_11
        elif np.pi < th <= (np.pi + (w11 * Ls * Id_11 / Vm_11)): 
            # Efecto de persistencia por Ls (simplificado)
            v_o[i] = v_s[i]
            # La corriente aquí empezaría a bajar... 
            # Para este modelo de Id constante, asumimos que el diodo de marcha libre (si existe) 
            # o el corte ocurre cerca de pi.
            i_s[i] = Id_11 
        else:
            v_o[i] = 0
            i_s[i] = 0

    fig12, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(theta, v_s, 'gray', ls='--', alpha=0.4, label="v_fuente(t)")
    ax1.plot(theta, v_o, 'b', lw=2, label="v_carga(t)")
    ax1.fill_between(theta, 0, v_s, where=(theta < u_rad), color='red', alpha=0.2, label="Área de pérdida (ΔV)")
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(); ax1.grid(True)
    
    ax2.plot(theta, i_s, 'r', lw=2, label="i_linea(t)")
    ax2.axhline(Id_11, color='black', ls=':', label="Nivel Id")
    ax2.set_ylabel("Corriente [A]"); ax2.set_xlabel("Fase [rad]"); ax2.legend(); ax2.grid(True)
    
    st.pyplot(fig12)

    st.info(f"👉 **Análisis:** Al considerar la carga como una fuente de corriente constante **Id**, el ángulo de conmutación **u** representa el tiempo que tarda la corriente de línea en subir desde 0 hasta el valor de la carga. Durante este tiempo (**{u_deg:.1f}°**), el voltaje en la carga es cero, lo que reduce el voltaje promedio final.")

# =========================================================
# MÓDULO 12: ONDA COMPLETA (CON CONTROL DE CICLOS)
# =========================================================
elif tema == "12. Onda Completa con Filtro C y Ls":
    st.header("Módulo 12: Rectificador de Onda Completa (Simulación de N Ciclos)")
    st.write("Estudio del transitorio y estado estable con control de tiempo de observación.")

    with st.sidebar:
        st.subheader("Parámetros del Circuito")
        Vm_12 = st.number_input("Voltaje Pico Fuente [V]", value=170.0, key="vm12_c")
        f_12 = st.number_input("Frecuencia [Hz]", value=60.0, key="f12_c")
        
        st.markdown("---")
        st.subheader("Configuración de Tiempo")
        # Nueva entrada para el número de ciclos
        num_ciclos = st.slider("Número de ciclos a simular", 1, 20, 5)
        
        st.markdown("---")
        st.subheader("Componentes")
        Ls_mH_12 = st.slider("Inductancia de Línea Ls [mH]", 0.1, 10.0, 1.0, step=0.1)
        C_uF_12 = st.number_input("Capacitor de Filtro [µF]", value=1000.0, step=100.0)
        R_12 = st.number_input("Resistencia de Carga [Ω]", value=50.0, min_value=1.0)

    # --- Configuración de Simulación Dinámica ---
    w = 2 * np.pi * f_12
    Ls = Ls_mH_12 / 1000
    C = C_uF_12 * 1e-6
    
    # Ajustamos la resolución según el número de ciclos para mantener precisión
    puntos_por_ciclo = 1000
    puntos = num_ciclos * puntos_por_ciclo
    theta = np.linspace(0, 2 * np.pi * num_ciclos, puntos) 
    dt = (theta[1] - theta[0]) / w
    
    v_s_abs = np.abs(Vm_12 * np.sin(theta))
    v_c = np.zeros(puntos)
    i_s = np.zeros(puntos)
    
    v_cap = 0.0 
    i_linea = 0.0
    
    # Simulación paso a paso
    for i in range(1, puntos):
        i_load = v_cap / R_12
        if v_s_abs[i] > v_cap or i_linea > 1e-3:
            di = ((v_s_abs[i] - v_cap) / Ls) * dt
            i_linea += di
            if i_linea < 0: i_linea = 0
            
            dv = ((i_linea - i_load) / C) * dt
            v_cap += dv
        else:
            i_linea = 0
            dv = (-i_load / C) * dt
            v_cap += dv
            
        v_c[i] = v_cap
        i_s[i] = i_linea

    # --- Cálculos de Estado Estable (tomando el último ciclo) ---
    ultimo_ciclo_idx = int(puntos * (num_ciclos - 1) / num_ciclos) if num_ciclos > 1 else 0
    v_avg = np.mean(v_c[ultimo_ciclo_idx:])
    v_ripple = np.max(v_c[ultimo_ciclo_idx:]) - np.min(v_c[ultimo_ciclo_idx:])
    i_pico_arranque = np.max(i_s)

    # --- Métricas ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Vdc (Último Ciclo)", f"{v_avg:.2f} V")
    col2.metric("Rizado (ΔV)", f"{v_ripple:.2f} V")
    col3.metric("I_pico de Arranque", f"{i_pico_arranque:.2f} A")

    # --- Gráficas ---
    fig13, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Eje X en número de ciclos para mayor claridad pedagógica
    x_ciclos = theta / (2 * np.pi)
    
    ax1.plot(x_ciclos, v_s_abs, 'gray', ls='--', alpha=0.2, label="|v_fuente|")
    ax1.plot(x_ciclos, v_c, 'b', lw=2, label="v_capacitor(t)")
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(); ax1.grid(True)
    ax1.set_title(f"Simulación de {num_ciclos} Ciclos")
    
    ax2.plot(x_ciclos, i_s, 'r', lw=1.5, label="i_linea(t)")
    ax2.fill_between(x_ciclos, i_s, 0, color='red', alpha=0.1)
    ax2.set_ylabel("Corriente [A]"); ax2.set_xlabel("Ciclos"); ax2.legend(); ax2.grid(True)
    
    st.pyplot(fig13)

    st.info(f"💡 **Sugerencia para clase:** Pida a los estudiantes que simulen 20 ciclos con una **C** muy grande para ver cuánto tarda el sistema en alcanzar el régimen permanente (tiempo de asentamiento).")

# =========================================================
# MÓDULO 13: ONDA COMPLETA L-C (CON MÉTRICAS)
# =========================================================
elif tema == "13. Onda Completa con Filtro L-C":
    st.header("Módulo 13: Rectificador con Filtro L-C")
    st.write("Análisis de filtrado y desempeño en régimen permanente.")

    with st.sidebar:
        st.subheader("Parámetros del Sistema")
        Vm_13 = st.number_input("Voltaje Pico Fuente [V]", value=170.0, key="v13_m")
        f_13 = st.number_input("Frecuencia [Hz]", value=60.0, key="f13_m")
        num_ciclos_13 = st.slider("Ciclos a simular", 2, 20, 8, key="n13_m")
        
        st.markdown("---")
        st.subheader("Componentes del Filtro")
        Lf_mH = st.number_input("Inductancia Filtro (Lf) [mH]", value=100.0, step=10.0, key="lf13_m")
        Cf_uF = st.number_input("Capacitancia Filtro (Cf) [µF]", value=470.0, step=50.0, key="cf13_m")
        R_13 = st.number_input("Resistencia Carga [Ω]", value=50.0, key="r13_m")

    # --- Simulación ---
    w = 2 * np.pi * f_13
    Lf = Lf_mH / 1000
    Cf = Cf_uF * 1e-6
    puntos = num_ciclos_13 * 1200
    theta = np.linspace(0, 2 * np.pi * num_ciclos_13, puntos)
    dt = (theta[1] - theta[0]) / w
    
    v_s = Vm_13 * np.sin(theta)
    v_s_abs = np.abs(v_s)
    v_out = np.zeros(puntos)
    i_f = np.zeros(puntos)
    i_in = np.zeros(puntos)
    
    v_c_val = 0.0
    i_l_val = 0.0
    
    for i in range(1, puntos):
        i_load = v_c_val / R_13
        if v_s_abs[i] > v_c_val or i_l_val > 1e-4:
            di_l = ((v_s_abs[i] - v_c_val) / Lf) * dt
            i_l_val += di_l
            if i_l_val < 0: i_l_val = 0
            dv_c = ((i_l_val - i_load) / Cf) * dt
            v_c_val += dv_c
        else:
            i_l_val = 0
            dv_c = (-i_load / Cf) * dt
            v_c_val += dv_c
        v_out[i] = v_c_val
        i_f[i] = i_l_val
        i_in[i] = i_l_val if v_s[i] >= 0 else -i_l_val

    # --- Cálculo de Parámetros de Desempeño (Último Ciclo) ---
    ultimo_ciclo_idx = int(puntos * (num_ciclos_13 - 1) / num_ciclos_13)
    v_segmento = v_out[ultimo_ciclo_idx:]
    v_avg = np.mean(v_segmento)
    v_max = np.max(v_segmento)
    v_min = np.min(v_segmento)
    v_ripple = v_max - v_min
    factor_rizado = (v_ripple / v_avg) * 100 if v_avg > 0 else 0
    
    # Inductancia Crítica Teórica Lc = R / (3w)
    Lc_teorica = (R_13 / (3 * w)) * 1000 # en mH

    # --- Interfaz de Resultados ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Vdc Promedio", f"{v_avg:.2f} V")
    c2.metric("Rizado ΔV", f"{v_ripple:.2f} V")
    c3.metric("Factor Rizado", f"{factor_rizado:.2f} %")
    c4.metric("Lc Crítica", f"{Lc_teorica:.1f} mH")

    # --- Gráficas ---
    fig14, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    plt.subplots_adjust(hspace=0.35)
    x_ciclos = theta / (2 * np.pi)
    
    ax1.plot(x_ciclos, v_s, 'gray', ls='--', alpha=0.3, label="v_fuente")
    ax1.plot(x_ciclos, v_out, 'b', lw=2, label="v_carga")
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(loc='upper right'); ax1.grid(True)
    
    ax2.plot(x_ciclos, i_f, 'g', lw=2, label="i_inductor (Filtro)")
    ax2.set_ylabel("i_L [A]"); ax2.legend(loc='upper right'); ax2.grid(True)
    
    ax3.plot(x_ciclos, i_in, 'r', lw=2, label="i_entrada (Red)")
    ax3.set_ylabel("i_in [A]"); ax3.set_xlabel("Ciclos"); ax3.legend(loc='upper right'); ax3.grid(True)
    
    st.pyplot(fig14)

    if Lf_mH < Lc_teorica:
        st.warning(f"⚠️ **Conducción Discontinua:** La inductancia actual ({Lf_mH} mH) es menor a la crítica ({Lc_teorica:.1f} mH). La corriente i_L llega a cero, lo que aumenta el rizado y degrada la regulación.")
    else:
        st.success(f"✅ **Conducción Continua:** El filtro opera correctamente por encima de la inductancia crítica.")

# =========================================================
# MÓDULO 14: ONDA COMPLETA CON FILTRO TIPO PI (C-L-C)
# =========================================================
elif tema == "14. Filtro Tipo Pi (C-L-C)":
    st.header("Módulo 14: Rectificador con Filtro Tipo Pi ($\pi$)")
    st.write("Análisis de la topología C1 - L - C2 para filtrado de alto desempeño.")

    with st.sidebar:
        st.subheader("Parámetros de Entrada")
        Vm_14 = st.number_input("Voltaje Pico Fuente [V]", value=170.0, key="v14_p")
        f_14 = st.number_input("Frecuencia [Hz]", value=60.0, key="f14_p")
        num_ciclos_14 = st.slider("Ciclos a simular", 2, 15, 6, key="n14_p")
        
        st.markdown("---")
        st.subheader("Componentes del Filtro PI")
        C1_uF = st.number_input("Capacitor C1 (Entrada) [µF]", value=470.0, step=50.0)
        Lf_mH = st.number_input("Inductancia L (Choque) [mH]", value=50.0, step=5.0)
        C2_uF = st.number_input("Capacitor C2 (Salida) [µF]", value=1000.0, step=100.0)
        R_14 = st.number_input("Resistencia de Carga [Ω]", value=50.0)

    # --- Simulación Numérica (Espacio de Estados) ---
    w = 2 * np.pi * f_14
    C1, Lf, C2 = C1_uF*1e-6, Lf_mH*1e-3, C2_uF*1e-6
    puntos = num_ciclos_14 * 2000 
    theta = np.linspace(0, 2 * np.pi * num_ciclos_14, puntos)
    dt = (theta[1] - theta[0]) / w
    
    v_s = Vm_14 * np.sin(theta)
    v_s_abs = np.abs(v_s)
    
    v_c1 = np.zeros(puntos); v_c2 = np.zeros(puntos)
    i_l = np.zeros(puntos); i_in = np.zeros(puntos)
    
    vc1, vc2, il = 0.0, 0.0, 0.0
    
    for i in range(1, puntos):
        i_load = vc2 / R_14
        
        # 1. Carga de C1 desde el puente de diodos
        if v_s_abs[i] > vc1:
            # Corriente que entra desde la red para cargar C1 y alimentar la etapa L-C2
            i_cap1 = C1 * (v_s_abs[i] - vc1) / dt
            i_in_val = i_cap1 + il
            vc1 = v_s_abs[i]
        else:
            # Puente bloqueado: C1 se descarga hacia la etapa L-C2
            dvc1 = (-il / C1) * dt
            vc1 += dvc1
            i_in_val = 0
            
        # 2. Dinámica del inductor Lf y capacitor C2
        dil = ((vc1 - vc2) / Lf) * dt
        il += dil
        if il < 0: il = 0
        
        dvc2 = ((il - i_load) / C2) * dt
        vc2 += dvc2
        
        v_c1[i], v_c2[i], i_l[i] = vc1, vc2, il
        i_in[i] = i_in_val if v_s[i] >= 0 else -i_in_val

    # --- Métricas de Desempeño (Último Ciclo) ---
    u_idx = int(puntos * (num_ciclos_14 - 1) / num_ciclos_14)
    v_avg = np.mean(v_c2[u_idx:])
    v_rip = np.max(v_c2[u_idx:]) - np.min(v_c2[u_idx:])
    i_pico_in = np.max(np.abs(i_in))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Vdc Final", f"{v_avg:.2f} V")
    c2.metric("Rizado ΔV", f"{v_rip:.4f} V")
    c3.metric("I_pico Entrada", f"{i_pico_in:.2f} A")
    c4.metric("Factor Rizado", f"{(v_rip/v_avg)*100:.3f} %")

    # --- Gráficas ---
    fig15, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 11), sharex=True)
    plt.subplots_adjust(hspace=0.3)
    x_ciclos = theta / (2 * np.pi)
    
    # Voltajes
    ax1.plot(x_ciclos, v_s_abs, 'gray', ls='--', alpha=0.2, label="|v_fuente|")
    ax1.plot(x_ciclos, v_c1, 'orange', alpha=0.6, label="v_C1 (Intermedio)")
    ax1.plot(x_ciclos, v_c2, 'b', lw=2, label="v_C2 (Salida)")
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(loc='upper right'); ax1.grid(True)
    
    # Corrientes de Filtrado
    ax2.plot(x_ciclos, i_l, 'g', lw=2, label="i_L (Inductor Filtro)")
    ax2.set_ylabel("i_L [A]"); ax2.legend(loc='upper right'); ax2.grid(True)
    
    # Corriente de Línea (Entrada CA)
    ax3.plot(x_ciclos, i_in, 'r', lw=1.5, label="i_entrada (Red CA)")
    ax3.axhline(0, color='black', lw=1)
    ax3.set_ylabel("i_in [A]"); ax3.set_xlabel("Ciclos"); ax3.legend(loc='upper right'); ax3.grid(True)
    
    st.pyplot(fig15)

    st.info("💡 **Nota didáctica:** Observe que el filtro Pi logra un rizado de voltaje extremadamente bajo, pero a costa de introducir pulsos de corriente muy altos en la entrada debido al capacitor C1.")

# =========================================================
# MÓDULO 15: AUTOEVALUACIÓN (QUIZ INTERACTIVO)
# =========================================================
elif tema == "15. Autoevaluación: Rectificadores":
    st.header("Módulo 15: Autoevaluación de Conceptos")
    st.write("""
    Ponga a prueba sus conocimientos sobre el comportamiento de los rectificadores con diferentes tipos de filtro y efectos parásitos.
    """)

    # --- Estructura del Quiz ---
    preguntas = [
        {
            "id": 1,
            "pregunta": "¿Qué efecto tiene el aumento de la Inductancia de Línea (Ls) en un rectificador?",
            "opciones": [
                "Aumenta el voltaje promedio de salida.",
                "Reduce el voltaje promedio debido al ángulo de conmutación (u).",
                "No tiene efecto en el voltaje, solo en la corriente.",
                "Elimina completamente el rizado de voltaje."
            ],
            "correcta": 1,
            "explicacion": "La inductancia de línea impide el cambio instantáneo de corriente entre diodos, creando una caída de voltaje promedio (V_gamma)."
        },
        {
            "id": 2,
            "pregunta": "En un filtro capacitivo simple, si la resistencia de carga (R) disminuye (mayor carga), ¿qué sucede con el rizado?",
            "opciones": [
                "El rizado disminuye porque el capacitor se descarga más lento.",
                "El rizado permanece igual.",
                "El rizado aumenta porque la constante de tiempo RC disminuye.",
                "El rizado desaparece."
            ],
            "correcta": 2,
            "explicacion": "Al disminuir R, la corriente de carga aumenta y el capacitor se descarga más rápido entre pulsos, incrementando el rizado (delta V)."
        },
        {
            "id": 3,
            "pregunta": "¿Cuál es la principal ventaja de un filtro L-C respecto a un filtro C puramente capacitivo?",
            "opciones": [
                "Es más barato y ligero.",
                "Produce picos de corriente de entrada más altos.",
                "Mejora el factor de potencia al suavizar los pulsos de corriente de entrada.",
                "Siempre entrega un voltaje mayor que el voltaje pico de entrada."
            ],
            "correcta": 2,
            "explicacion": "El inductor de choque limita el di/dt de entrada, evitando los pulsos estrechos y altos típicos del filtro capacitivo."
        },
        {
            "id": 4,
            "pregunta": "En el Filtro Tipo Pi (C1-L-C2), ¿qué componente es el principal responsable de la corriente de irrupción (Inrush Current)?",
            "opciones": [
                "El inductor L.",
                "El capacitor de entrada C1.",
                "La resistencia de carga R.",
                "El capacitor de salida C2."
            ],
            "correcta": 1,
            "explicacion": "C1 está conectado directamente a la salida del puente; al estar descargado, demanda una corriente masiva en el primer semiciclo."
        }
    ]

    # --- Lógica de Interfaz ---
    if 'score' not in st.session_state:
        st.session_state.score = 0
    
    for p in preguntas:
        st.markdown(f"**{p['id']}. {p['pregunta']}**")
        resp = st.radio(f"Seleccione una opción para la pregunta {p['id']}:", p['opciones'], key=f"q{p['id']}")
        
        if st.button(f"Verificar Pregunta {p['id']}", key=f"btn{p['id']}"):
            idx_resp = p['opciones'].index(resp)
            if idx_resp == p['correcta']:
                st.success(f"¡Correcto! {p['explicacion']}")
            else:
                st.error(f"Incorrecto. {p['explicacion']}")
        st.markdown("---")

    st.info("💡 **Consejo:** Puede regresar a los módulos de simulación para cambiar los parámetros y observar estos fenómenos gráficamente antes de responder.")
    # --- Formulario Técnico ---
    st.subheader("📓 Formulario: Rectificadores No Controlados")
    
    with st.expander("Ver Fórmulas y Definiciones"):
        st.markdown(r"""
        ### 1. Parámetros de Desempeño Generales
        * **Valor Promedio (CD):** $V_{dc} = \frac{1}{T} \int_{0}^{T} v(t) dt$
        * **Valor Eficaz (RMS):** $V_{rms} = \sqrt{\frac{1}{T} \int_{0}^{T} v^2(t) dt}$
        * **Factor de Rizado (RF):** $RF = \frac{V_{ac}}{V_{dc}} \times 100\% = \frac{\sqrt{V_{rms}^2 - V_{dc}^2}}{V_{dc}} \times 100\%$
        
        ### 2. Onda Completa con Filtro Capacitivo ($C$)
        * **Voltaje de Rizado aproximado ($\Delta V$):** $\Delta V \approx \frac{V_m}{2 \cdot f \cdot R \cdot C}$
        * **Voltaje CD Promedio:** $V_{dc} \approx V_m - \frac{\Delta V}{2}$
        
        ### 3. Filtro $L-C$ (Conducción Continua)
        * **Inductancia Crítica ($L_c$):** $L_c \geq \frac{R}{3\omega} = \frac{R}{6\pi f}$
        * **Voltaje CD Promedio:** $V_{dc} = \frac{2 V_m}{\pi}$ (Ideal, despreciando caídas en $L$)
        * **Factor de Rizado:** $RF \approx \frac{\sqrt{2}}{3 (4 \omega^2 L C - 1)}$
        
        ### 4. Efecto de la Inductancia de Línea ($L_s$)
        * **Caída de Voltaje por Conmutación ($\Delta V_{comm}$):** $\Delta V_{comm} = \frac{2 \omega L_s I_{dc}}{\pi}$ (para monofásico)
        * **Voltaje de Salida Real:** $V_{dc} = \frac{2 V_m}{\pi} - \frac{2 f L_s I_{dc}}{1}$ 
        """)

    st.markdown("---")
