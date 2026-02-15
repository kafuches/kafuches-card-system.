import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Mi Kafuches Card", page_icon="💳")

# ESTILO DE TARJETA DE LUJO
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    .card {
        background-color: #012F7E;
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.3);
        margin-top: 20px;
    }
    .saldo { color: #00FF3B; font-size: 40px; font-weight: bold; }
    .nombre { font-family: 'Lora', serif; font-size: 24px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Consulta tu Kafuches Card")
cedula_consulta = st.text_input("Ingresa tu Cédula para ver tu saldo:")

if cedula_consulta:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    # Buscar al cliente
    cliente = df[df['Cédula'].astype(str) == str(cedula_consulta)]
    
    if not cliente.empty:
        nombre = cliente.iloc[-1]['Nombre Cliente']
        # Sumamos todos los saldos ganados y restamos los usados
        total_ganado = df[df['Cédula'].astype(str) == str(cedula_consulta)]['Saldo Ganado ($)'].sum()
        total_usado = df[df['Cédula'].astype(str) == str(cedula_consulta)]['Saldo Usado ($)'].sum()
        saldo_final = total_ganado - total_usado
        
        st.markdown(f"""
            <div class="card">
                <div class="nombre">Hola, {nombre}</div>
                <div>Tu saldo disponible para bienestar es:</div>
                <div class="saldo">${saldo_final:,.0f} COP</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No encontramos registros para esta cédula. ¡Sigue disfrutando de Kafuches para acumular bienestar!")
