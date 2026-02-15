import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Mi Kafuches Card", page_icon="🌿", layout="centered")

# DISEÑO DE TARJETA PREMIUM CON LOGO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital@0;1&family=Poppins:wght@400;600&display=swap');
    
    .stApp { background-color: #FFFFFF; }
    
    .card-container {
        background: linear-gradient(135deg, #012F7E 0%, #001a4d 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0px 15px 30px rgba(1, 47, 126, 0.4);
        max-width: 400px;
        margin: 0 auto;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .logo-img {
        width: 140px;
        margin-bottom: 20px;
    }
    
    .nombre-cliente {
        font-family: 'Lora', serif;
        font-size: 22px;
        font-style: italic;
        margin-bottom: 5px;
    }
    
    .monto-saldo {
        font-family: 'Poppins', sans-serif;
        color: #00FF3B;
        font-size: 48px;
        font-weight: 600;
        margin-top: 10px;
        text-shadow: 0px 0px 15px rgba(0, 255, 59, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# URL DEL LOGO DE KAFUCHES
logo_url = "https://kafuches.com/wp-content/uploads/2023/05/Logo-Kafuches-PNG.png" 

st.title("🌿 Mi Bienestar Kafuches")

cedula_consulta = st.text_input("Ingresa tu cédula para consultar tu saldo:")

if cedula_consulta:
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        
        # Buscar cliente (asegurando que la cédula sea texto)
        df['Cédula'] = df['Cédula'].astype(str).str.strip()
        cliente_data = df[df['Cédula'] == str(cedula_consulta).strip()]
        
        if not cliente_data.empty:
            nombre = cliente_data.iloc[-1]['Nombre Cliente']
            ganado = pd.to_numeric(cliente_data['Saldo Ganado ($)'], errors='coerce').sum()
            usado = pd.to_numeric(cliente_data['Saldo Usado ($)'], errors='coerce').sum()
            saldo_total = ganado - usado
            
            st.markdown(f"""
                <div class="card-container">
                    <img src="{logo_url}" class="logo-img">
                    <div class="nombre-cliente">Hola, {nombre}</div>
                    <div style="opacity:0.8; font-size:14px;">SALDO DISPONIBLE</div>
                    <div class="monto-saldo">${saldo_total:,.0f}</div>
                    <div style="margin-top:20px; font-size:12px; opacity:0.6;">Kafuches Card • Bienestar que fluye</div>
                </div>
                """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.info("No encontramos registros. ¡Visítanos para empezar a acumular bienestar!")
    except:
        st.error("Error de conexión. Verifica los Secrets en Streamlit.")
