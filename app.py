import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# CONFIGURACIÓN VISUAL KAFUCHES
st.set_page_config(page_title="Kafuches Card Admin", page_icon="🌿")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital@0;1&family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    h1, h2 { font-family: 'Lora', serif; color: #012F7E; }
    .stButton>button { 
        background-color: #00FF3B; 
        color: #012F7E; 
        border-radius: 20px; 
        font-weight: bold; 
        border: none;
        padding: 10px 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Kafuches Card: Central de Bienestar")

# CONEXIÓN CON TU HOJA (ID: 1CXKVc1JerJqRnl3c1bA5QaZF37ySRHODI572ap3nkvM)
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("registro_puntos"):
    st.subheader("Cargar Saldo a Cliente")
    col1, col2 = st.columns(2)
    with col1:
        cedula = st.text_input("Cédula")
        nombre = st.text_input("Nombre Completo")
    with col2:
        celular = st.text_input("WhatsApp")
        monto = st.number_input("Saldo Ganado ($)", min_value=0)
    
    if st.form_submit_button("Guardar Bienestar"):
        if cedula and nombre:
            nueva_fila = pd.DataFrame([{
                "Fecha": pd.Timestamp.now().strftime("%d/%m/%Y"),
                "Cédula": cedula,
                "Nombre Cliente": nombre,
                "Celular": celular,
                "Saldo Ganado ($)": monto,
                "Saldo Usado ($)": 0
            }])
            # Aquí se conecta con la hoja que compartiste
            data_actual = conn.read()
            actualizada = pd.concat([data_actual, nueva_fila], ignore_index=True)
            conn.update(data=actualizada)
            st.success(f"¡Listo! ${monto} cargados a {nombre}")
