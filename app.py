import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Laboratorio de Ortogonalidad en CA")
st.write("Mueve los deslizadores para ver cómo interactúan las frecuencias.")

# Sliders en la barra lateral
n = st.sidebar.slider("Frecuencia Voltaje (n)", 1, 10, 1)
m = st.sidebar.slider("Frecuencia Corriente (m)", 1, 10, 2)
phi = st.sidebar.slider("Desfase (grados)", 0, 360, 0)

t = np.linspace(0, 1, 1000)
v = np.sin(2 * np.pi * n * t)
i = np.sin(2 * np.pi * m * t + np.radians(phi))
p = v * i
p_avg = np.mean(p)

fig, ax = plt.subplots(2, 1, figsize=(10, 8))
ax[0].plot(t, v, label="v(t)")
ax[0].plot(t, i, label="i(t)", linestyle="--")
ax[0].legend()

ax[1].plot(t, p, color="black", label="p(t)")
ax[1].fill_between(t, p, 0, where=(p>=0), color='green', alpha=0.3)
ax[1].fill_between(t, p, 0, where=(p<0), color='orange', alpha=0.3)
ax[1].axhline(p_avg, color='purple', label=f'Promedio = {p_avg:.4f}')
ax[1].legend()

st.pyplot(fig)

if np.isclose(p_avg, 0, atol=1e-5):
    st.success("¡Las señales son ORTOGONALES! La potencia neta es cero.")
else:
    st.warning("Las señales NO son ortogonales. Hay transferencia de potencia activa.")
