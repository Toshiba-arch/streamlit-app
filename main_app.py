import streamlit as st
import app_ofertas
import app_euromilhoes

# Título principal
st.title("Aplicação Multifunções")

# Dropdown para selecionar a funcionalidade
app_selecionada = st.sidebar.selectbox(
    "Selecione a funcionalidade",
    ["Gerador de Ofertas", "Gerador de Números do Euromilhões"]
)

# Redirecionar para a funcionalidade selecionada
if app_selecionada == "Gerador de Ofertas":
    app_ofertas.run()
elif app_selecionada == "Gerador de Números do Euromilhões":
    app_euromilhoes.run()
