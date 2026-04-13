import streamlit as st
from groq import Groq

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="NÚCLEO AXEL v3.0", layout="wide")

# ESTILO CSS PARA IMITAR TU APP_AXEL.PY
st.markdown("""
    <style>
    /* Color de fondo de la barra lateral (Gris) */
    [data-testid="stSidebar"] {
        background-color: #ebebeb;
    }
    /* Estilo de los botones laterales */
    .stButton>button {
        background-color: #f0f0f0;
        border: 1px solid #d1d1d1;
        border-radius: 5px;
        color: #555;
        text-align: left;
    }
    /* El botón de Nuevo Chat */
    div.stButton > button:first-child {
        background-color: #2b5797;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Tu clave de Groq
API_KEY = "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"
client = Groq(api_key=API_KEY)

# --- BARRA LATERAL (Igual a tu imagen) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #333;'>NÚCLEO AXEL</h1>", unsafe_allow_html=True)
    
    if st.button("+ Nuevo Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.write("") # Espacio
    
    # Botones de sesiones (como los de tu captura)
    st.button("Sesión 12-04_185458", use_container_width=True)
    st.button("Sesión 12-04_185408", use_container_width=True)

# --- CUADRO DE CHAT (Lado derecho) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Contenedor blanco para el chat
chat_placeholder = st.container()

with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada de texto abajo
if prompt := st.chat_input("Escribe a Axel..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")