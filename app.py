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
        "15. Autoevaluación: Rectificadores",
        "16. Puente Controlado (Carga R y RL)",
        "17. Puente Controlado (Carga R y RL)",
        "18. Bidireccionalidad de Potencia (Fuente I)",
        "19. Bidireccionalidad de Potencia (Fuente I)-extendido",
        "20. Efecto de la Inductancia de Línea (Ls)",
        "21. Rectificador Trifásico (6 Pulsos)",
        "22. Calidad en Sistemas Trifásicos",
        "23. Rectificadores Multi-pulso",
        "24. Autoevaluación: Sistemas Multi-pulso",
        "25. Traslape en Sistemas Trifásicos",
        "26. Troceadores y Cuadrantes de Operación",
        "27. Análisis de Rizado y L Crítica",
        "28. Troceador Clase B (Regenerativo)"
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

# =========================================================
# MÓDULO 16: PUENTE TOTALMENTE CONTROLADO (SCR)
# =========================================================
elif tema == "16. Puente Controlado (Carga R y RL)":
    st.header("Módulo 16: Puente Monofásico Totalmente Controlado")
    st.write("Control de fase mediante tiristores (SCR) para regulación de voltaje CD.")

    with st.sidebar:
        st.subheader("Parámetros de Control")
        Vm_16 = st.number_input("Voltaje Pico [V]", value=170.0, key="v16")
        f_16 = st.number_input("Frecuencia [Hz]", value=60.0)
        
        # Parámetro crítico: Ángulo de disparo alfa
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 180, 45)
        
        st.markdown("---")
        st.subheader("Tipo de Carga")
        tipo_carga = st.radio("Seleccione Carga:", ["Resistiva (R)", "Inductiva (R-L)"])
        R_16 = st.number_input("Resistencia [Ω]", value=20.0)
        
        L_mH_16 = 0.0
        if tipo_carga == "Inductiva (R-L)":
            L_mH_16 = st.number_input("Inductancia [mH]", value=50.0, step=10.0)

    # --- Cálculos y Simulación ---
    alpha_rad = np.deg2rad(alpha_deg)
    w = 2 * np.pi * f_16
    theta = np.linspace(0, 4 * np.pi, 2000) # Dos ciclos
    v_s = Vm_16 * np.sin(theta)
    v_out = np.zeros_like(theta)
    i_out = np.zeros_like(theta)

    if tipo_carga == "Resistiva (R)":
        # En carga R, el tiristor deja de conducir en el cruce por cero (180°)
        for i, t in enumerate(theta % (np.pi)):
            if t >= alpha_rad:
                v_out[i] = np.abs(v_s[i])
        i_out = v_out / R_16
        
        # Fórmula teórica Vdc = (2*Vm/pi) * cos(alpha) solo aplica en conducción continua RL.
        # Para carga R: Vdc = (Vm/pi) * (1 + cos(alpha))
        v_dc_teo = (Vm_16 / np.pi) * (1 + np.cos(alpha_rad))

    else:
        # Carga Inductiva (Simplificación de Conducción Continua)
        # En puentes totalmente controlados con L grande, v_out puede ser negativo
        for i, t in enumerate(theta % (np.pi)):
            if t >= alpha_rad or t <= 0: # Simplificación de disparo
                v_out[i] = Vm_16 * np.sin(theta[i]) if v_s[i] > 0 else -Vm_16 * np.sin(theta[i])
        
        # En RL, v_out sigue a la fuente hasta el siguiente disparo alpha + pi
        # Usamos una lógica de ventana para mostrar el efecto del voltaje negativo
        for i in range(len(theta)):
            phi = theta[i] % np.pi
            if phi < alpha_rad:
                v_out[i] = -Vm_16 * np.abs(np.sin(theta[i]))
            else:
                v_out[i] = Vm_16 * np.abs(np.sin(theta[i]))
        
        i_out = np.full_like(theta, (2*Vm_16/np.pi * np.cos(alpha_rad))/R_16) # Promedio aprox
        v_dc_teo = (2 * Vm_16 / np.pi) * np.cos(alpha_rad)

    # --- Interfaz y Gráficas ---
    c1, c2 = st.columns(2)
    c1.metric("Vdc Teórico", f"{v_dc_teo:.2f} V")
    c1.metric("Ángulo α", f"{alpha_deg}°")

    fig16, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(theta, v_s, 'gray', ls='--', alpha=0.3, label="v_fuente(t)")
    ax1.plot(theta, v_out, 'b', lw=2, label="v_salida(t)")
    ax1.fill_between(theta, v_out, 0, color='blue', alpha=0.1)
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(); ax1.grid(True)
    
    ax2.plot(theta, i_out, 'r', lw=2, label="i_carga(t)")
    ax2.set_ylabel("Corriente [A]"); ax2.set_xlabel("Fase [rad]"); ax2.legend(); ax2.grid(True)
    
    st.pyplot(fig16)

    if tipo_carga == "Resistiva (R)":
        st.latex(r"V_{dc} = \frac{V_m}{\pi} (1 + \cos \alpha)")
        st.info("💡 En carga resistiva, el tiristor se apaga naturalmente en $\pi, 2\pi, ...$ porque la corriente cae a cero.")
    else:
        st.latex(r"V_{dc} = \frac{2 V_m}{\pi} \cos \alpha")
        st.warning("⚠️ En carga inductiva, el voltaje de salida puede ser **negativo** durante parte del ciclo debido a la energía almacenada en L.")

# =========================================================
# MÓDULO 17: PUENTE TOTALMENTE CONTROLADO (CARGA R-L)
# =========================================================
elif tema == "17. Puente Controlado (Carga R y RL)":
    st.header("Módulo 16: Puente Monofásico Totalmente Controlado")
    st.write("Análisis de la rectificación controlada con carga inductiva.")

    with st.sidebar:
        st.subheader("Parámetros de Disparo")
        Vm_16 = st.number_input("Voltaje Pico [V]", value=170.0, key="v16_p")
        f_16 = st.number_input("Frecuencia [Hz]", value=60.0, key="f16_p")
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 180, 45, key="alpha16")
        
        st.markdown("---")
        st.subheader("Carga R-L")
        R_16 = st.number_input("Resistencia [Ω]", value=10.0, key="r16_p")
        L_mH_16 = st.number_input("Inductancia [mH]", value=50.0, step=10.0, key="l16_p")
        num_ciclos = st.slider("Ciclos visibles", 1, 5, 2, key="n16_p")

    # --- Motor de Simulación Numérica ---
    w = 2 * np.pi * f_16
    alpha = np.deg2rad(alpha_deg)
    L = L_mH_16 / 1000
    
    puntos = num_ciclos * 1000
    theta = np.linspace(0, 2 * np.pi * num_ciclos, puntos)
    dt = (theta[1] - theta[0]) / w
    
    v_s = Vm_16 * np.sin(theta)
    v_out = np.zeros(puntos)
    i_out = np.zeros(puntos)
    
    # Resolver ecuación diferencial: v_out = Ri + L(di/dt)
    current = 0.0
    for i in range(1, puntos):
        # Lógica de conmutación del puente completo SCR
        phi = theta[i] % np.pi
        if phi >= alpha:
            v_rect = np.abs(v_s[i])
        else:
            # En conducción continua (RL), el voltaje sigue a la rama anterior
            v_rect = -np.abs(v_s[i])
            
        v_out[i] = v_rect
        
        # Integración de Euler para la corriente
        di = (v_out[i] - R_16 * current) / L * dt
        current += di
        if current < 0: current = 0 # El SCR bloquea corriente negativa
        i_out[i] = current

    # --- Resultados y Métricas ---
    v_dc_teo = (2 * Vm_16 / np.pi) * np.cos(alpha)
    i_avg = np.mean(i_out[int(puntos/2):]) # Promedio del último tramo
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Vdc Teórico", f"{v_dc_teo:.2f} V")
    col2.metric("Idc Promedio", f"{i_avg:.2f} A")
    col3.metric("Ángulo Disparo", f"{alpha_deg}°")

    # --- Visualización ---
    fig16, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    x_eje = theta / (2 * np.pi)
    
    ax1.plot(x_eje, v_s, 'gray', ls='--', alpha=0.3, label="v_fuente")
    ax1.plot(x_eje, v_out, 'b', lw=2, label="v_salida (SCR)")
    ax1.fill_between(x_eje, v_out, 0, color='blue', alpha=0.1)
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(); ax1.grid(True)
    
    ax2.plot(x_eje, i_out, 'r', lw=2, label="i_carga (RL)")
    ax2.set_ylabel("Corriente [A]"); ax2.set_xlabel("Ciclos"); ax2.legend(); ax2.grid(True)
    
    st.pyplot(fig16)

    # --- Bloque de Información Teórica ---
    st.info(f"""
    **Análisis de la Carga Inductiva (R-L):**
    1. **Voltaje Negativo:** Observe que para $\\alpha = {alpha_deg}^\circ$, el voltaje $v_{{out}}$ tiene secciones negativas. Esto se debe a que la energía almacenada en el inductor mantiene el SCR en conducción.
    2. **Fórmula:** En régimen permanente y conducción continua: $V_{{dc}} = \\frac{{2 V_m}}{{\pi}} \cos \\alpha$.
    3. **Control:** Note que si $\\alpha > 90^\circ$, el voltaje promedio se vuelve negativo.
    """)

# =========================================================
# MÓDULO 18: BIDIRECCIONALIDAD DE POTENCIA (CARGA I_dc)
# =========================================================
elif tema == "18. Bidireccionalidad de Potencia (Fuente I)":
    st.header("Módulo 17: Operación en Dos Cuadrantes")
    st.write("Exploración del flujo de potencia bidireccional (Rectificación e Inversión).")

    with st.sidebar:
        st.subheader("Control del Convertidor")
        Vm_17 = st.number_input("Voltaje Pico Fuente CA [V]", value=170.0, key="v17")
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 180, 45, key="alpha17")
        
        st.markdown("---")
        st.subheader("Modelo de Carga Activa")
        # Fuente de corriente ajustable que representa un motor o línea HVDC
        Idc_val = st.number_input("Corriente de Carga Idc [A]", value=10.0, min_value=0.1)
        num_ciclos = 2

    # --- Cálculos de Potencia ---
    alpha_rad = np.deg2rad(alpha_deg)
    w = 2 * np.pi * 60
    puntos = num_ciclos * 1000
    theta = np.linspace(0, 2 * np.pi * num_ciclos, puntos)
    
    v_s = Vm_17 * np.sin(theta)
    v_out = np.zeros(puntos)
    p_inst = np.zeros(puntos) # Potencia instantánea
    
    for i in range(puntos):
        phi = theta[i] % np.pi
        if phi >= alpha_rad:
            v_out[i] = np.abs(v_s[i])
        else:
            v_out[i] = -np.abs(v_s[i])
        
        # Potencia P = V_out * I_dc
        p_inst[i] = v_out[i] * Idc_val

    # --- Resultados ---
    v_dc_avg = (2 * Vm_17 / np.pi) * np.cos(alpha_rad)
    p_avg = v_dc_avg * Idc_val
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Vdc Promedio", f"{v_dc_avg:.2f} V")
    col2.metric("Potencia Media (P)", f"{p_avg:.2f} W")
    
    if p_avg >= 0:
        col3.success("Modo: RECTIFICADOR")
    else:
        col3.warning("Modo: INVERSOR")

    # --- Visualización ---
    fig17, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True)
    x_eje = theta / (2 * np.pi)
    
    # Gráfica 1: Voltaje de Salida
    ax1.plot(x_eje, v_s, 'gray', ls='--', alpha=0.3, label="v_fuente CA")
    ax1.plot(x_eje, v_out, 'b', lw=2, label="v_salida (CD)")
    ax1.fill_between(x_eje, v_out, 0, color='blue', alpha=0.1)
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(loc='upper right'); ax1.grid(True)
    
    # Gráfica 2: Potencia Instantánea
    ax2.plot(x_eje, p_inst, 'purple', lw=2, label="Potencia p(t)")
    ax2.axhline(0, color='black', lw=1)
    ax2.fill_between(x_eje, p_inst, 0, where=(p_inst >= 0), color='green', alpha=0.2, label="Entrega a CD")
    ax2.fill_between(x_eje, p_inst, 0, where=(p_inst < 0), color='red', alpha=0.2, label="Retorno a CA")
    ax2.set_ylabel("Potencia [W]"); ax2.set_xlabel("Ciclos"); ax2.legend(loc='upper right'); ax2.grid(True)
    
    st.pyplot(fig17)

    st.info(f"""
    **Lección de Bidireccionalidad:**
    * **α < 90°:** El voltaje promedio es positivo. La potencia fluye hacia la carga CD (Rectificación).
    * **α = 90°:** El voltaje promedio es cero. La potencia neta transferida es nula.
    * **α > 90°:** El voltaje promedio es negativo. Como la corriente $I_{{dc}}$ mantiene su dirección, la potencia es negativa, lo que significa que fluye de la fuente CD hacia la red CA (Inversión).
    """)

# =========================================================
# MÓDULO 19: CALIDAD, REACTIVOS Y ESPECTRO ARMÓNICO
# =========================================================
elif tema == "19. Bidireccionalidad de Potencia (Fuente I)-extendido":
    st.header("Módulo 17: Calidad de Energía y Potencia Reactiva")
    st.write("Análisis de flujo de potencia, THD y consumo de reactivos.")

    with st.sidebar:
        st.subheader("Configuración")
        Vm_17 = st.number_input("Voltaje Pico Fuente [V]", value=170.0, key="v17_q")
        f_17 = st.number_input("Frecuencia [Hz]", value=60.0, key="f17_q")
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 180, 45, key="alpha17_q")
        Idc_val = st.number_input("Corriente de Carga Idc [A]", value=10.0, key="idc17_q")
        num_ciclos = 4

    # --- Simulación ---
    alpha_rad = np.deg2rad(alpha_deg)
    w = 2 * np.pi * f_17
    puntos = num_ciclos * 2048 # Potencia de 2 para mejor FFT
    theta = np.linspace(0, 2 * np.pi * num_ciclos, puntos)
    
    v_s = Vm_17 * np.sin(theta)
    v_out = np.zeros(puntos)
    i_in = np.zeros(puntos)
    
    for i in range(puntos):
        phi = theta[i] % np.pi
        if phi >= alpha_rad:
            v_out[i] = np.abs(v_s[i])
            i_in[i] = Idc_val if v_s[i] >= 0 else -Idc_val
        else:
            v_out[i] = -np.abs(v_s[i])
            i_in[i] = -Idc_val if v_s[i] >= 0 else Idc_val

    # --- Cálculos de Potencia y Calidad ---
    v_rms = Vm_17 / np.sqrt(2)
    i_rms = Idc_val
    S = v_rms * i_rms # Potencia Aparente Total
    
    # Análisis FFT
    ciclo_inicio = int(puntos * (num_ciclos - 1) / num_ciclos)
    i_sample = i_in[ciclo_inicio:]
    fft_vals = np.fft.rfft(i_sample)
    fft_mag = np.abs(fft_vals) * 2 / len(i_sample)
    
    # Fundamental (Armónico 1)
    i1_rms = fft_mag[1] / np.sqrt(2)
    
    # Potencia Activa (P) y Reactiva (Q) de la fundamental
    # P = Vrms * I1rms * cos(alpha)
    P = v_rms * i1_rms * np.cos(alpha_rad)
    # Q = Vrms * I1rms * sen(alpha) -> Siempre positiva por el valor absoluto del seno
    Q = v_rms * i1_rms * np.abs(np.sin(alpha_rad))
    
    # THD y FP
    thd_i = np.sqrt(np.sum(fft_mag[2:]**2)) / fft_mag[1] * 100
    fp = P / S

    # --- Métricas ---
    st.subheader("📊 Índices de Calidad y Potencia")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("P (Activa)", f"{P:.1f} W")
    c2.metric("Q (Reactiva)", f"{Q:.1f} VAR")
    c3.metric("S (Aparente)", f"{S:.1f} VA")
    c4.metric("FP", f"{fp:.3f}")

    # --- Gráficas ---
    fig17, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    plt.subplots_adjust(hspace=0.4)
    
    # Gráfica 1: Formas de Onda
    x_ciclos = theta / (2 * np.pi)
    ax1.plot(x_ciclos, v_s/Vm_17, 'gray', ls='--', alpha=0.3, label="v_fuente (pu)")
    ax1.plot(x_ciclos, i_in/Idc_val, 'r', lw=2, label="i_línea (pu)")
    ax1.set_title("Señales en Unidades Per-Unit (pu)")
    ax1.set_xlabel("Ciclos"); ax1.legend(); ax1.grid(True)
    
    # Gráfica 2: Espectro Armónico
    harmonics = np.arange(1, 16, 2) # Armónicos impares
    mags = [fft_mag[h] for h in harmonics]
    ax2.bar(harmonics, mags, color='darkblue', alpha=0.7)
    ax2.set_title("Espectro Armónico de la Corriente de Línea")
    ax2.set_xticks(harmonics)
    ax2.set_ylabel("Amplitud [A]")
    ax2.set_xlabel("Orden del Armónico")
    for j, v in enumerate(mags):
        ax2.text(harmonics[j], v + 0.2, f"{v:.1f}", ha='center')
    
    st.pyplot(fig17)

    st.info(f"""
    **Observación sobre Potencia Reactiva:**
    * Note que incluso si la carga es una fuente de corriente ideal, el convertidor consume **{Q:.1f} VAR**.
    * Esto ocurre porque el ángulo de disparo $\\alpha$ desplaza la componente fundamental de la corriente respecto al voltaje. 
    * A $\\alpha = 90^\circ$, la potencia activa es casi nula, pero el consumo de reactivos llega a su punto máximo, comportándose como un reactor inductivo para la red.
    """)

# =========================================================
# MÓDULO 20: INDUCTANCIA DE LÍNEA Y TRASLAPE (Ls)
# =========================================================
elif tema == "20. Efecto de la Inductancia de Línea (Ls)":
    st.header("Módulo 18: Fenómeno de Traslape (Overlap)")
    st.write("Análisis de la conmutación no instantánea debido a la inductancia de red.")

    with st.sidebar:
        st.subheader("Parámetros de Red")
        Vm_18 = st.number_input("Voltaje Pico Fuente [V]", value=170.0)
        f_18 = st.number_input("Frecuencia [Hz]", value=60.0)
        Ls_mH = st.number_input("Inductancia de Línea (Ls) [mH]", value=2.0, step=0.5)
        
        st.markdown("---")
        st.subheader("Operación del Convertidor")
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 90, 30)
        Idc_val = st.number_input("Corriente de Carga Idc [A]", value=15.0)

    # --- Cálculos del Traslape ---
    w = 2 * np.pi * f_18
    Ls = Ls_mH / 1000
    alpha_rad = np.deg2rad(alpha_deg)
    
    # Cálculo del ángulo de traslape (u) para puente monofásico:
    # cos(alpha + u) = cos(alpha) - (2 * w * Ls * Idc) / Vm
    cos_val = np.cos(alpha_rad) - (2 * w * Ls * Idc_val) / Vm_18
    
    # Verificación de límite físico
    if cos_val < -1:
        st.error("⚠️ Ls o Idc demasiado altos: El convertidor entra en falla de conmutación.")
        u_rad = np.pi - alpha_rad
    else:
        u_rad = np.arccos(cos_val) - alpha_rad
    
    u_deg = np.rad2deg(u_rad)

    # --- Simulación de Formas de Onda ---
    num_ciclos = 2
    puntos = num_ciclos * 1500
    theta = np.linspace(0, 2 * np.pi * num_ciclos, puntos)
    v_s = Vm_18 * np.sin(theta)
    v_out = np.zeros(puntos)
    i_linea = np.zeros(puntos)

    for i in range(puntos):
        phi = theta[i] % np.pi
        # Intervalo de Traslape (Conmutación)
        if alpha_rad <= phi <= (alpha_rad + u_rad):
            v_out[i] = 0 # En puente monofásico el voltaje cae a cero durante el traslape
            # La corriente sube linealmente (aprox) durante el traslape
            progreso = (phi - alpha_rad) / u_rad
            val_i = -Idc_val + 2 * Idc_val * progreso
            i_linea[i] = val_i if v_s[i] >= 0 else -val_i
        # Intervalo de Conducción Normal
        elif (alpha_rad + u_rad) < phi < np.pi:
            v_out[i] = np.abs(v_s[i])
            i_linea[i] = Idc_val if v_s[i] >= 0 else -Idc_val
        else:
            v_out[i] = -np.abs(v_s[i])
            i_linea[i] = -Idc_val if v_s[i] >= 0 else Idc_val

    # --- Métricas de Desempeño ---
    v_dc_ideal = (2 * Vm_18 / np.pi) * np.cos(alpha_rad)
    caida_v = (2 * w * Ls * Idc_val) / np.pi
    v_dc_real = v_dc_ideal - caida_v

    c1, c2, c3 = st.columns(3)
    c1.metric("Ángulo de Traslape (μ)", f"{u_deg:.2f}°")
    c2.metric("Vdc con Caída", f"{v_dc_real:.2f} V")
    c3.metric("Pérdida por Ls", f"{caida_v:.2f} V")

    # --- Gráficas ---
    fig18, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True)
    x_ciclos = theta / (2 * np.pi)
    
    ax1.plot(x_ciclos, v_s, 'gray', ls='--', alpha=0.3, label="v_fuente")
    ax1.plot(x_ciclos, v_out, 'b', lw=2, label="v_salida (con Notch)")
    ax1.fill_between(x_ciclos, v_out, 0, color='blue', alpha=0.1)
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(); ax1.grid(True)
    
    ax2.plot(x_ciclos, i_linea, 'r', lw=2, label="i_línea (con rampa)")
    ax2.set_ylabel("Corriente [A]"); ax2.set_xlabel("Ciclos"); ax2.legend(); ax2.grid(True)
    
    st.pyplot(fig18)

    st.info(f"""
    **Observaciones sobre el Traslape:**
    * **Muescas de Voltaje (Notches):** Note las caídas a cero en el voltaje de salida justo en el momento del disparo. Esto ensucia el voltaje que ven otras cargas en el PCC (Point of Common Coupling).
    * **Pendiente de Corriente:** La corriente de línea ya no es una onda cuadrada perfecta; ahora tiene una rampa finita definida por $L_s$.
    * **Regulación:** A mayor corriente de carga ($I_{{dc}}$) o mayor inductancia ($L_s$), el área perdida de voltaje aumenta, reduciendo el $V_{{dc}}$ real.
    """)

# =========================================================
# MÓDULO 21: RECTIFICADOR TRIFÁSICO DE 6 PULSOS (SCR)
# =========================================================
elif tema == "21. Rectificador Trifásico (6 Pulsos)":
    st.header("Módulo 19: Puente de Graetz Trifásico Controlado")
    st.write("Análisis del rectificador industrial de 6 pulsos con control de fase.")

    with st.sidebar:
        st.subheader("Parámetros de Red Trifásica")
        Vln_rms = st.number_input("Voltaje Fase-Neutro [Vrms]", value=127.0)
        f_19 = st.number_input("Frecuencia [Hz]", value=60.0)
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 120, 30)
        
        st.markdown("---")
        st.subheader("Modelo de Carga")
        Idc_19 = st.number_input("Corriente de Carga (Constante) [A]", value=20.0)
        num_ciclos = st.slider("Ciclos de visualización", 1, 3, 1)

    # --- Generación de Voltajes Trifásicos ---
    w = 2 * np.pi * f_19
    Vm = Vln_rms * np.sqrt(2)
    puntos = num_ciclos * 2000
    theta = np.linspace(0, 2 * np.pi * num_ciclos, puntos)
    
    # Voltajes de Fase (F-N)
    va = Vm * np.sin(theta)
    vb = Vm * np.sin(theta - 2*np.pi/3)
    vc = Vm * np.sin(theta - 4*np.pi/3)
    
    # Voltajes de Línea (F-F) - Los que realmente ve la carga
    vab, vbc, vca = va - vb, vb - vc, vc - va
    vba, vcb, vac = -vab, -vbc, -vca
    
    v_out = np.zeros(puntos)
    alpha_rad = np.deg2rad(alpha_deg)

    # --- Lógica de Conmutación de 6 Pulsos ---
    # Cada pulso dura 60 grados. La referencia de alpha=0 comienza en 
    # el cruce de voltajes de línea (30° respecto al origen de Va).
    offset = np.pi/6 # 30 grados
    
    for i in range(puntos):
        phi = (theta[i] - offset) % (2*np.pi)
        # Secuencia de conducción (6 intervalos de 60°)
        if alpha_rad <= phi < alpha_rad + np.pi/3:
            v_out[i] = vab[i] # T1 y T6
        elif alpha_rad + np.pi/3 <= phi < alpha_rad + 2*np.pi/3:
            v_out[i] = vac[i] # T1 y T2
        elif alpha_rad + 2*np.pi/3 <= phi < alpha_rad + np.pi:
            v_out[i] = vbc[i] # T3 y T2
        elif alpha_rad + np.pi <= phi < alpha_rad + 4*np.pi/3:
            v_out[i] = vba[i] # T3 y T4
        elif alpha_rad + 4*np.pi/3 <= phi < alpha_rad + 5*np.pi/3:
            v_out[i] = vca[i] # T5 y T4
        else:
            v_out[i] = vcb[i] # T5 y T6

    # --- Métricas de Desempeño ---
    Vll_rms = Vln_rms * np.sqrt(3)
    Vll_pico = Vll_rms * np.sqrt(2)
    # Fórmula: Vdc = (3 * Vll_pico / pi) * cos(alpha)
    v_dc_teo = (3 * Vll_pico / np.pi) * np.cos(alpha_rad)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Vdc Promedio", f"{v_dc_teo:.2f} V")
    c2.metric("V_línea Pico", f"{Vll_pico:.1f} V")
    c3.metric("Frec. Rizado", f"{f_19*6} Hz")

    # --- Gráficas ---
    fig19 = plt.figure(figsize=(12, 8))
    gs = fig19.add_gridspec(2, 1, height_ratios=[2, 1])
    ax1 = fig19.add_subplot(gs[0])
    ax2 = fig19.add_subplot(gs[1], sharex=ax1)
    
    x_ciclos = theta / (2 * np.pi)
    
    # Voltajes de Línea (Fondo)
    ax1.plot(x_ciclos, vab, 'gray', alpha=0.15, ls='--')
    ax1.plot(x_ciclos, vbc, 'gray', alpha=0.15, ls='--')
    ax1.plot(x_ciclos, vca, 'gray', alpha=0.15, ls='--')
    
    # Voltaje Rectificado
    ax1.plot(x_ciclos, v_out, 'b', lw=2.5, label="Voltaje de Salida CD")
    ax1.set_ylabel("Voltaje [V]"); ax1.grid(True, alpha=0.3); ax1.legend()
    ax1.set_title(f"Rectificación Trifásica a α = {alpha_deg}°")
    
    # Corriente de Fase A (Visualización del bloque de 120°)
    i_a = np.zeros(puntos)
    for i in range(puntos):
        phi = (theta[i] - offset) % (2*np.pi)
        # Fase A conduce en los primeros dos intervalos (positivo) 
        # y en el 4to y 5to (negativo)
        if alpha_rad <= phi < alpha_rad + 2*np.pi/3:
            i_a[i] = Idc_19
        elif alpha_rad + np.pi <= phi < alpha_rad + 5*np.pi/3:
            i_a[i] = -Idc_19
            
    ax2.plot(x_ciclos, i_a, 'r', lw=2, label="Corriente Fase A (i_a)")
    ax2.set_ylabel("Corriente [A]"); ax2.set_xlabel("Ciclos"); ax2.grid(True); ax2.legend()
    
    st.pyplot(fig19)

    st.latex(r"V_{dc} = \frac{3 \sqrt{2} V_{L-L,rms}}{\pi} \cos \alpha")

# =========================================================
# MÓDULO 22: CALIDAD DE ENERGÍA TRIFÁSICA (6 PULSOS)
# =========================================================
elif tema == "22. Calidad en Sistemas Trifásicos":
    st.header("Módulo 20: Índices de Desempeño en 6 Pulsos")
    st.write("Análisis armónico y de potencia reactiva para aplicaciones industriales.")

    with st.sidebar:
        st.subheader("Configuración de Red")
        Vll_rms = st.number_input("Voltaje Línea-Línea [Vrms]", value=220.0)
        f_20 = st.number_input("Frecuencia [Hz]", value=60.0)
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 120, 30)
        Idc_20 = st.number_input("Corriente CD Constante [A]", value=50.0)

    # --- Generación de Señales ---
    w = 2 * np.pi * f_20
    alpha_rad = np.deg2rad(alpha_deg)
    Vm_linea = Vll_rms * np.sqrt(2)
    Vm_fase = Vm_linea / np.sqrt(3)
    
    num_ciclos = 4
    puntos = num_ciclos * 2048
    theta = np.linspace(0, 2 * np.pi * num_ciclos, puntos)
    
    # Voltaje de Fase A (Referencia para FP y Reactivos)
    va = Vm_fase * np.sin(theta)
    
    # Generación de i_a (Bloques de 120°)
    # La corriente i_a está centrada en el voltaje de fase, desplazada por alpha
    i_a = np.zeros(puntos)
    offset = np.pi/6 # 30 grados de desfase natural entre fase y línea
    
    for i in range(puntos):
        phi = (theta[i] - offset) % (2*np.pi)
        if alpha_rad <= phi < alpha_rad + 2*np.pi/3:
            i_a[i] = Idc_20
        elif alpha_rad + np.pi <= phi < alpha_rad + 5*np.pi/3:
            i_a[i] = -Idc_20

    # --- Análisis de Fourier (FFT) ---
    ciclo_inicio = int(puntos * (num_ciclos - 1) / num_ciclos)
    i_sample = i_a[ciclo_inicio:]
    fft_vals = np.fft.rfft(i_sample)
    fft_mag = np.abs(fft_vals) * 2 / len(i_sample)
    
    i1_rms = fft_mag[1] / np.sqrt(2)
    i_total_rms = np.sqrt(np.mean(i_sample**2))
    thd_i = np.sqrt(np.sum(fft_mag[2:]**2)) / fft_mag[1] * 100
    
    # --- Potencias Trifásicas ---
    # P = sqrt(3) * Vll_rms * I1_rms * cos(alpha)
    P_tri = np.sqrt(3) * Vll_rms * i1_rms * np.cos(alpha_rad)
    # Q = sqrt(3) * Vll_rms * I1_rms * sen(alpha)
    Q_tri = np.sqrt(3) * Vll_rms * i1_rms * np.abs(np.sin(alpha_rad))
    S_tri = np.sqrt(3) * Vll_rms * i_total_rms
    fp_tri = P_tri / S_tri

    # --- Métricas ---
    st.subheader("📊 Resultados de Calidad de Energía")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Potencia Activa (P)", f"{P_tri/1000:.2f} kW")
    c2.metric("Potencia Reactiva (Q)", f"{Q_tri/1000:.2f} kVAR")
    c3.metric("THD Corriente", f"{thd_i:.2f} %")
    c4.metric("Factor Potencia", f"{fp_tri:.3f}")

    # --- Gráficas ---
    fig20, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    plt.subplots_adjust(hspace=0.4)
    
    # Temporal: Voltaje Fase A vs Corriente Fase A
    x_c = theta / (2 * np.pi)
    ax1.plot(x_c, va/Vm_fase, 'gray', ls='--', alpha=0.4, label="v_fase_a (pu)")
    ax1.plot(x_c, i_a/Idc_20, 'r', lw=2, label="i_línea_a (pu)")
    ax1.set_title("Relación de Fase y Desplazamiento")
    ax1.set_xlabel("Ciclos"); ax1.grid(True); ax1.legend()
    
    # Espectro: Solo impares no múltiplos de 3 (5, 7, 11, 13...)
    h_idx = [1, 5, 7, 11, 13]
    h_mags = [fft_mag[h] for h in h_idx]
    ax2.bar([str(h) for h in h_idx], h_mags, color='teal')
    ax2.set_title("Espectro Armónico (Armónicos Dominantes)")
    ax2.set_ylabel("Amplitud [A]"); ax2.set_xlabel("Orden del Armónico")
    
    st.pyplot(fig20)

    st.info("""
    **Puntos para Discusión en Clase:**
    1. **Cancelación de Armónicos Triplen:** Observe que el 3er armónico es prácticamente cero. Esta es la mayor ventaja del sistema trifásico.
    2. **THD Teórico:** En un puente de 6 pulsos ideal, el THD de corriente es de aproximadamente 31%, comparado con el 48% del monofásico.
    3. **Reactivos en Alta Potencia:** Note cómo el valor de **Q** aumenta proporcionalmente a la potencia del sistema. En la industria, esto justifica el uso de bancos de capacitores o compensadores estáticos (SVC) junto a los rectificadores.
    """)

# =========================================================
# MÓDULO 23: RECTIFICADORES DE MULTI-PULSO (6, 12, 18, 24)
# =========================================================
elif tema == "23. Rectificadores Multi-pulso":
    st.header("Módulo 21: Rectificadores de n-Pulsos")
    st.write("Estudio de la cancelación de armónicos mediante desfase de transformadores.")

    with st.sidebar:
        st.subheader("Configuración de Pulsos")
        n_pulsos = st.selectbox("Número de pulsos (n):", [6, 12, 18, 24])
        Vll_rms = st.number_input("Voltaje Línea-Línea [Vrms]", value=440.0)
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 90, 15)
        Idc_total = st.number_input("Corriente CD Total [A]", value=100.0)

    # --- Lógica de Simulación Multi-pulso ---
    f = 60.0
    w = 2 * np.pi * f
    alpha_rad = np.deg2rad(alpha_deg)
    num_puentes = n_pulsos // 6
    desfase_entre_puentes = (2 * np.pi) / (n_pulsos) # p.ej. 30° para 12 pulsos
    
    puntos = 4096
    theta = np.linspace(0, 2 * np.pi, puntos)
    v_out_total = np.zeros(puntos)
    i_linea_primario = np.zeros(puntos)
    
    Vm_linea = Vll_rms * np.sqrt(2)
    
    for k in range(num_puentes):
        shift = k * desfase_entre_puentes
        v_out_k = np.zeros(puntos)
        
        # Generación de voltajes de línea desfasados para cada puente
        vab = Vm_linea * np.sin(theta + shift)
        vbc = Vm_linea * np.sin(theta - 2*np.pi/3 + shift)
        vca = Vm_linea * np.sin(theta - 4*np.pi/3 + shift)
        vba, vcb, vac = -vab, -vbc, -vca
        
        # Lógica de 6 pulsos para el puente 'k'
        offset_ref = np.pi/6 
        for i in range(puntos):
            phi = (theta[i] - offset_ref + shift) % (2*np.pi)
            if alpha_rad <= phi < alpha_rad + np.pi/3: v_out_k[i] = vab[i]
            elif alpha_rad + np.pi/3 <= phi < alpha_rad + 2*np.pi/3: v_out_k[i] = vac[i]
            elif alpha_rad + 2*np.pi/3 <= phi < alpha_rad + np.pi: v_out_k[i] = vbc[i]
            elif alpha_rad + np.pi <= phi < alpha_rad + 4*np.pi/3: v_out_k[i] = vba[i]
            elif alpha_rad + 4*np.pi/3 <= phi < alpha_rad + 5*np.pi/3: v_out_k[i] = vca[i]
            else: v_out_k[i] = vcb[i]
            
            # Corriente reflejada al primario (simplificada)
            # Cada puente aporta una componente desfasada a la corriente total
            if alpha_rad <= phi < alpha_rad + 2*np.pi/3:
                i_linea_primario[i] += (Idc_total / num_puentes) * np.cos(shift)
            elif alpha_rad + np.pi <= phi < alpha_rad + 5*np.pi/3:
                i_linea_primario[i] -= (Idc_total / num_puentes) * np.cos(shift)

        v_out_total += v_out_k / num_puentes

    # --- Análisis FFT ---
    fft_vals = np.fft.rfft(i_linea_primario)
    fft_mag = np.abs(fft_vals) * 2 / puntos
    thd_i = np.sqrt(np.sum(fft_mag[2:100]**2)) / fft_mag[1] * 100

    # --- Métricas ---
    st.subheader(f"📊 Análisis del Sistema de {n_pulsos} Pulsos")
    c1, c2, c3 = st.columns(3)
    c1.metric("Vdc Promedio", f"{np.mean(v_out_total):.2f} V")
    c2.metric("THD Corriente (I_linea)", f"{thd_i:.2f} %")
    c3.metric("Primer Armónico", f"Orden {n_pulsos-1} y {n_pulsos+1}")

    # --- Gráficas ---
    fig21, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    ax1.plot(theta/(2*np.pi), v_out_total, 'b', lw=2, label=f"Voltaje CD ({n_pulsos} pulsos)")
    ax1.set_title("Voltaje de Salida Rectificado")
    ax1.grid(True); ax1.legend()
    
    # Espectro Armónico
    h_max = 50
    ax2.bar(range(1, h_max, 2), fft_mag[1:h_max:2], color='darkred')
    ax2.set_title("Espectro de Corriente en el Primario")
    ax2.set_xlim(0, h_max)
    ax2.set_xlabel("Orden Armónico"); ax2.set_ylabel("Amplitud [A]")
    
    st.pyplot(fig21)

    st.info(f"""
    **Efecto de la Configuración de {n_pulsos} Pulsos:**
    1. **Cancelación:** Observe cómo desaparecen los armónicos de orden menor a {n_pulsos-1}.
    2. **Calidad CD:** El rizado de voltaje es casi imperceptible, con una frecuencia fundamental de {60*n_pulsos} Hz.
    3. **Aplicación:** Esta configuración reduce drásticamente la necesidad de filtros de armónicos pesados en la red.
    """)

# =========================================================
# MÓDULO 24: AUTOEVALUACIÓN Y FORMULARIO (MULTI-PULSO)
# =========================================================
elif tema == "24. Autoevaluación: Sistemas Multi-pulso":
    st.header("Módulo 22: Consolidación de Rectificación de Potencia")
    st.write("Resumen técnico y evaluación sobre sistemas de n-pulsos y calidad de energía.")

    # --- Formulario Técnico Avanzado ---
    st.subheader("📓 Formulario de Alta Potencia")
    with st.expander("Ver Fórmulas de Sistemas Trifásicos y Multi-pulso"):
        st.markdown(r"""
        ### 1. Puente de Graetz (6 Pulsos)
        * **Voltaje CD Promedio:** $V_{dc} = \frac{3 \sqrt{2} V_{LL,rms}}{\pi} \cos \alpha \approx 1.35 V_{LL,rms} \cos \alpha$
        * **Voltaje CD con Traslape ($L_s$):** $V_{dc} = \frac{3 \sqrt{2} V_{LL,rms}}{\pi} \cos \alpha - \frac{3 \omega L_s I_{dc}}{\pi}$
        * **Armónicos de Corriente presentes:** $h = 6k \pm 1$ (5, 7, 11, 13...)
        
        ### 2. Sistemas de n-Pulsos
        * **Ángulo de desfase necesario entre puentes:** $\phi = \frac{60^\circ}{m}$ (donde $m$ es el número de puentes de 6 pulsos).
        * **Armónicos en el primario:** $h = nk \pm 1$ (ej. para 12 pulsos: 11, 13, 23, 25...).
        * **Frecuencia del rizado de salida:** $f_{ripple} = n \cdot f_{red}$
        
        ### 3. Potencia y Reactivos
        * **Potencia Activa Trifásica:** $P = \sqrt{3} V_{LL,rms} I_{1,rms} \cos \alpha$
        * **Potencia Reactiva Trifásica:** $Q = \sqrt{3} V_{LL,rms} I_{1,rms} \sin \alpha$
        * **Factor de Potencia (FP):** $FP = \frac{3}{\pi} \cos \alpha$ (para 6 pulsos ideal).
        """)

    st.markdown("---")
    st.subheader("📝 Quiz de Verificación")

    # --- Estructura del Quiz ---
    preguntas_adv = [
        {
            "id": 1,
            "pregunta": "¿Cuál es el desfase eléctrico requerido entre los secundarios de un transformador para un sistema de 12 pulsos?",
            "opciones": ["15°", "30°", "60°", "0°"],
            "correcta": 1,
            "explicacion": "Para 12 pulsos se requieren dos puentes de 6 pulsos desfasados 30° (60°/2) para cancelar los armónicos 5 y 7."
        },
        {
            "id": 2,
            "pregunta": "En un rectificador de 6 pulsos, ¿qué sucede con el factor de potencia si el ángulo de disparo (alpha) aumenta?",
            "opciones": [
                "El FP mejora porque se reduce la distorsión.",
                "El FP empeora debido al incremento del desplazamiento (cos alpha).",
                "El FP permanece constante.",
                "El FP se vuelve unitario a los 90°."
            ],
            "correcta": 1,
            "explicacion": "El FP depende tanto de la distorsión como del desplazamiento. Al aumentar alpha, el desplazamiento aumenta, reduciendo el FP significativamente."
        },
        {
            "id": 3,
            "pregunta": "¿Cuál es el primer armónico de corriente que aparece en el primario de un rectificador de 18 pulsos?",
            "opciones": ["5to", "11vo", "17vo", "23vo"],
            "correcta": 2,
            "explicacion": "Siguiendo la regla h = nk ± 1, para n=18, los primeros armónicos son 18-1=17 y 18+1=19."
        },
        {
            "id": 4,
            "pregunta": "El fenómeno de traslape (overlap) causado por Ls provoca que el voltaje CD promedio:",
            "opciones": ["Aumente ligeramente.", "Se mantenga igual.", "Disminuya.", "Se vuelva puramente senoidal."],
            "correcta": 2,
            "explicacion": "El traslape 'roba' área al voltaje de salida durante la conmutación, lo que resulta en una caída del valor promedio Vdc."
        }
    ]

    # --- Lógica de Interfaz ---
    for p in preguntas_adv:
        st.markdown(f"**{p['id']}. {p['pregunta']}**")
        resp = st.radio(f"Seleccione su respuesta ({p['id']}):", p['opciones'], key=f"adv_q{p['id']}")
        
        if st.button(f"Comprobar {p['id']}", key=f"adv_btn{p['id']}"):
            idx_resp = p['opciones'].index(resp)
            if idx_resp == p['correcta']:
                st.success(f"¡Excelente! {p['explicacion']}")
            else:
                st.error(f"Siga analizando. {p['explicacion']}")
        st.markdown("---")

    st.info("💡 **Consejo Académico:** Utilice este módulo para que los alumnos verifiquen la relación entre el número de pulsos y la pureza de la corriente antes de pasar a los convertidores CD-CD.")

# =========================================================
# MÓDULO 25: TRASLAPE EN RECTIFICADORES TRIFÁSICOS (Ls)
# =========================================================
elif tema == "25. Traslape en Sistemas Trifásicos":
    st.header("Módulo 23: Efecto de Ls y Ángulo de Traslape (μ)")
    st.write("Análisis de la caída de tensión inductiva y muescas de conmutación en 6 pulsos.")

    with st.sidebar:
        st.subheader("Parámetros de Red y Carga")
        Vll_rms = st.number_input("Voltaje Línea-Línea [Vrms]", value=220.0)
        Ls_mH = st.number_input("Inductancia de Línea (Ls) [mH]", value=1.5, step=0.1)
        alpha_deg = st.slider("Ángulo de Disparo (α) [°]", 0, 90, 20)
        Idc_23 = st.number_input("Corriente de Carga Idc [A]", value=40.0)

    # --- Cálculos del Fenómeno de Traslape ---
    w = 2 * np.pi * 60
    Ls = Ls_mH / 1000
    alpha_rad = np.deg2rad(alpha_deg)
    Vm_linea = Vll_rms * np.sqrt(2)
    
    # Ecuación de traslape trifásico: 
    # cos(alpha + mu) = cos(alpha) - (sqrt(2) * w * Ls * Idc) / Vll_linea_pico
    # Nota: Para 6 pulsos, la caída es (3 * w * Ls * Idc) / pi
    cos_mu_val = np.cos(alpha_rad) - (np.sqrt(2) * w * Ls * Idc_23) / (Vll_rms * np.sqrt(2))
    
    if cos_mu_val < -1:
        st.error("⚠️ Falla de conmutación: Ls o Idc excesivos para este ángulo alpha.")
        mu_rad = 0.1 # Valor mínimo para evitar errores de dibujo
    else:
        mu_rad = np.arccos(cos_mu_val) - alpha_rad
    
    mu_deg = np.rad2deg(mu_rad)

    # --- Generación de Formas de Onda ---
    puntos = 2000
    theta = np.linspace(0, 2 * np.pi, puntos)
    vab = Vm_linea * np.sin(theta + np.pi/6)
    vac = Vm_linea * np.sin(theta - np.pi/6)
    # ... (Omitiendo el resto de las combinaciones por brevedad, simulamos el notch)
    
    v_out = np.zeros(puntos)
    offset = np.pi/6
    for i in range(puntos):
        phi = (theta[i] - offset) % (np.pi/3) # Cada 60 grados
        if phi < mu_rad:
            # Durante el traslape, el voltaje es el promedio de dos voltajes de línea
            # Simplificación pedagógica del notch:
            v_out[i] = Vm_linea * np.cos(alpha_rad + phi/2) * np.cos(mu_rad/2) * 0.85 # Ajuste visual
        else:
            v_out[i] = Vm_linea * np.sin(phi + np.pi/3 + alpha_rad)

    # --- Métricas ---
    v_dc_ideal = (3 * Vm_linea / np.pi) * np.cos(alpha_rad)
    caida_v = (3 * w * Ls * Idc_23) / np.pi
    v_dc_real = v_dc_ideal - caida_v

    c1, c2, c3 = st.columns(3)
    c1.metric("Ángulo μ (Traslape)", f"{mu_deg:.2f}°")
    c2.metric("Vdc Real", f"{v_dc_real:.2f} V")
    c3.metric("Caída ΔV_Ls", f"{caida_v:.2f} V")

    # --- Gráfica de Voltaje de Salida ---
    fig23, ax = plt.subplots(figsize=(10, 5))
    ax.plot(theta/(2*np.pi), v_out, 'b', lw=2, label="v_out con Traslape")
    ax.set_title(f"Voltaje de Salida con Muescas de Conmutación (α={alpha_deg}°, μ={mu_deg:.1f}°)")
    ax.set_ylabel("Voltaje [V]"); ax.grid(True)
    st.pyplot(fig23)

    st.info(f"""
    **Efecto de la Inductancia Ls en 3φ:**
    1. **Muescas (Notches):** Observe cómo el voltaje no salta instantáneamente; hay una transición suave que reduce el área efectiva del voltaje CD.
    2. **Caída de Tensión:** La caída de tensión NO es resistiva ($I^2R$), sino proporcional a la frecuencia y a la inductancia.
    3. **Límite de Inversión:** En modo inversor ($\\alpha > 90^\circ$), el traslape es crítico, ya que si $\\alpha + \\mu > 180^\circ$, ocurre una **falla de conmutación** catastrófica.
    """)

# =========================================================
# MÓDULO 26: TROCEADORES ELEMENTALES POR CUADRANTES
# =========================================================
elif tema == "26. Troceadores y Cuadrantes de Operación":
    st.header("Módulo 24: Clasificación de Troceadores (Choppers)")
    st.write("Análisis de convertidores CD-CD según su capacidad de manejo de potencia y cuadrantes.")

    with st.sidebar:
        st.subheader("Configuración de Control")
        V_dc = st.number_input("Voltaje de Fuente (Vdc) [V]", value=200.0)
        D = st.slider("Ciclo de Trabajo (D)", 0.0, 1.0, 0.5)
        
        st.markdown("---")
        tipo_chopper = st.selectbox("Clase de Troceador:", 
            ["Clase A (1er Cuadrante - Reductor)", 
             "Clase B (2do Cuadrante - Regenerativo)",
             "Clase C (1er y 2do Cuadrante)",
             "Clase D (1er y 4to Cuadrante)",
             "Clase E (4 Cuadrantes - Puente H)"])

    # --- Lógica de Visualización de Formas de Onda ---
    t = np.linspace(0, 0.01, 1000) # 10ms para visualización
    f_sw = 500
    pwm = (t % (1/f_sw)) < (D/f_sw)
    
    # Inicialización segura de variables de dibujo
    rects = []
    v_plot = np.zeros_like(t)

    if "Clase A" in tipo_chopper:
        v_plot = V_dc * pwm
        rects.append(plt.Rectangle((0,0), 1, 1, color='green', alpha=0.3))
        desc = "Motores de CD en marcha simple. La energía fluye de fuente a carga."
    
    elif "Clase B" in tipo_chopper:
        v_plot = V_dc * (1 - pwm) 
        rects.append(plt.Rectangle((-1,0), 1, 1, color='orange', alpha=0.3))
        desc = "Frenado regenerativo. La carga devuelve energía a la fuente (E > Vdc)."
        
    elif "Clase C" in tipo_chopper:
        v_plot = V_dc * pwm
        rects.append(plt.Rectangle((-1,0), 2, 1, color='blue', alpha=0.2))
        desc = "Ideal para tracción eléctrica (Aceleración y Frenado)."
        
    elif "Clase D" in tipo_chopper:
        # Reversibilidad de voltaje
        v_plot = V_dc * (2*pwm - 1)
        rects.append(plt.Rectangle((0,-1), 1, 2, color='purple', alpha=0.2))
        desc = "Voltaje reversible. Permite transferencia de energía en ambos sentidos."
        
    else: # Clase E - Puente Completo
        v_plot = V_dc * (2*pwm - 1)
        rects.append(plt.Rectangle((-1,-1), 2, 2, color='red', alpha=0.15))
        desc = "Control total: Marcha adelante/atrás y frenado en ambos sentidos."

    # --- Gráfica de Salida ---
    st.info(f"**Análisis:** {desc}")
    fig24, ax = plt.subplots(figsize=(10, 3))
    ax.plot(t*1000, v_plot, 'g', lw=2)
    ax.set_ylabel("Vo [V]"); ax.set_xlabel("Tiempo [ms]"); ax.grid(True, alpha=0.3)
    st.pyplot(fig24)

    # --- Diagrama de Cuadrantes en Sidebar ---
    fig_q, ax_q = plt.subplots(figsize=(4, 4))
    ax_q.axhline(0, color='black', lw=1); ax_q.axvline(0, color='black', lw=1)
    ax_q.set_xlim(-1.2, 1.2); ax_q.set_ylim(-1.2, 1.2)
    ax_q.set_xlabel("Corriente (Io)"); ax_q.set_ylabel("Voltaje (Vo)")
    ax_q.set_title("Cuadrantes de Operación")
    
    for r in rects:
        ax_q.add_patch(r)
    
    st.sidebar.pyplot(fig_q)

# =========================================================
# MÓDULO 27: TROCEADOR CLASE A - CARGA R-L-E
# =========================================================
elif tema == "27. Análisis de Rizado y L Crítica":
    st.header("Módulo 25: Diseño del Inductor y Rizado de Corriente")
    st.write("Cálculo del rizado en la armadura y determinación del régimen de conducción.")

    with st.sidebar:
        st.subheader("Parámetros del Sistema")
        V_dc = st.number_input("Voltaje Fuente (Vdc) [V]", value=240.0)
        f_sw = st.number_input("Frecuencia PWM [Hz]", value=2000.0)
        D = st.slider("Ciclo de Trabajo (D)", 0.05, 0.95, 0.5)
        
        st.markdown("---")
        st.subheader("Parámetros del Motor (Carga)")
        Ra = st.number_input("Resistencia Armadura (Ra) [Ω]", value=0.5)
        La_mH = st.number_input("Inductancia (La) [mH]", value=10.0, step=1.0)
        E_emf = st.number_input("F.E.M. (E) [V]", value=100.0)

    # --- Cálculos Técnicos ---
    T = 1 / f_sw
    L = La_mH / 1000
    tau = L / Ra
    
    # Voltaje promedio de salida
    Va_avg = D * V_dc
    # Corriente promedio (Estado estacionario)
    Ia_avg = (Va_avg - E_emf) / Ra if Va_avg > E_emf else 0.0
    
    # Rizado de corriente aproximado (suponiendo Ra despreciable para delta i)
    delta_i = (V_dc - Va_avg) * (D * T) / L
    
    # Corrientes máximas y mínimas
    I_max = Ia_avg + (delta_i / 2)
    I_min = Ia_avg - (delta_i / 2)
    
    # Inductancia Crítica para evitar DCM
    L_critica = ((1 - D) * Ra * T) / (2 * np.log((1 + np.exp(T/tau))/(1 + np.exp(D*T/tau)))) # Exacta
    L_crit_aprox = (V_dc * D * (1 - D) * T) / (2 * Ia_avg) if Ia_avg > 0 else 0

    # --- Métricas ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Ia Promedio", f"{Ia_avg:.2f} A")
    c2.metric("Rizado Δi", f"{delta_i:.2f} A")
    
    if I_min > 0:
        c3.success("Régimen: Continuo (CCM)")
    else:
        c3.warning("Régimen: Discontinuo (DCM)")

    # --- Simulación Temporal ---
    t_sim = np.linspace(0, 2*T, 1000)
    v_sw = np.where((t_sim % T) < D*T, V_dc, 0)
    
    # Respuesta simplificada de corriente (triangular aproximada)
    i_sim = np.zeros_like(t_sim)
    curr = Ia_avg - (delta_i / 2)
    for i in range(1, len(t_sim)):
        dt = t_sim[i] - t_sim[i-1]
        v_inst = v_sw[i]
        di = (v_inst - Ra * curr - E_emf) / L * dt
        curr += di
        i_sim[i] = max(0, curr)

    # --- Gráficas ---
    fig25, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1.plot(t_sim*1000, v_sw, 'b', lw=2, label="v_armadura(t)")
    ax1.axhline(E_emf, color='r', ls='--', label="E (FEM)")
    ax1.set_ylabel("Voltaje [V]"); ax1.legend(); ax1.grid(True)
    
    ax2.plot(t_sim*1000, i_sim, 'g', lw=2, label="i_armadura(t)")
    ax2.fill_between(t_sim*1000, i_sim, 0, color='g', alpha=0.1)
    ax2.set_ylabel("Corriente [A]"); ax2.set_xlabel("Tiempo [ms]"); ax2.legend(); ax2.grid(True)
    
    st.pyplot(fig25)

    st.latex(r"\Delta i = \frac{V_{dc} \cdot D \cdot (1-D)}{f_{sw} \cdot L}")
    
    st.info(f"""
    **Análisis de Diseño:**
    * **Rizado:** Con $L = {La_mH}$ mH, el rizado es del { (delta_i/Ia_avg*100 if Ia_avg > 0 else 0):.1f}% respecto a la media.
    * **Efecto de la frecuencia:** Si aumenta $f_{{sw}}$, verá cómo $\Delta i$ disminuye, permitiendo inductores más pequeños.
    * **Condición Crítica:** Para mantener conducción continua con esta carga, se requeriría una $L > {L_crit_aprox*1000:.2f}$ mH.
    """)

# =========================================================
# MÓDULO 28 (FINAL): ÍNDICES DE REGENERACIÓN Y POTENCIA
# =========================================================
elif tema == "28. Troceador Clase B (Regenerativo)":
    # ... (Sidebar y parámetros iguales al bloque anterior)

    # --- Cálculos de Potencia e Índices ---
    T = 1 / f_sw
    L = La_mH / 1000
    Vo_avg = (1 - D) * V_dc # Voltaje promedio en terminales de la fuente
    
    # Corriente promedio de frenado
    Ia_avg = (E_gen - Vo_avg) / Ra if E_gen > Vo_avg else 0.0
    
    # 1. Potencia Total Generada por el Motor (como generador)
    P_gen = E_gen * Ia_avg
    
    # 2. Pérdidas por efecto Joule en la armadura (Resistencia)
    # Nota: Para rigor, se usa Ia_rms, pero en CCM con bajo rizado Ia_avg es buena aprox.
    P_loss = (Ia_avg**2) * Ra
    
    # 3. Potencia Real Recuperada (la que llega a la fuente Vdc)
    P_rec = P_gen - P_loss # También calculable como Vo_avg * Ia_avg
    
    # 4. Eficiencia de la Regeneración
    eficiencia = (P_rec / P_gen * 100) if P_gen > 0 else 0.0

    # --- Métricas de Aprendizaje ---
    st.subheader("📊 Índices de Desempeño Energético")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("P. Generada (E*Ia)", f"{P_gen:.1f} W")
    c2.metric("P. Perdida (I²R)", f"{P_loss:.1f} W", delta_color="inverse")
    c3.metric("P. Recuperada", f"{P_rec:.1f} W")
    c4.metric("Eficiencia η", f"{eficiencia:.1f} %")

    # --- Simulación y Gráfica (Igual al bloque anterior) ---
    # ... [Código de simulación de i_regeneracion] ...

    # --- Bloque de Análisis para el Estudiante ---
    st.markdown("---")
    st.write("### 💡 Análisis de los Resultados")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"""
        **¿Por qué la eficiencia es del {eficiencia:.1f}%?**
        * El motor genera **{P_gen:.1f} W** de potencia mecánica convertida a eléctrica.
        * Sin embargo, el paso de corriente por $R_a$ disipa **{P_loss:.1f} W** en forma de calor.
        * Solo el remanente (**{P_rec:.1f} W**) logra vencer la barrera de potencial de la fuente $V_{{dc}}$.
        """)
    with col_b:
        st.write("""
        **Influencia del Ciclo de Trabajo (D):**
        * Si **aumenta D**, el voltaje promedio $V_{o}$ disminuye.
        * Esto aumenta la diferencia $(E - V_{o})$, lo que dispara la corriente de frenado.
        * **Cuidado:** Una corriente muy alta aumenta las pérdidas cuadráticas ($I^2R$), bajando la eficiencia aunque se recupere más potencia total.
        """)
