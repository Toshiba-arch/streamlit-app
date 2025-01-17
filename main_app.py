import streamlit as st
from app_ofertas import run as run_ofertas
from app_euromilhoes import run as run_euromilhoes

st.title("App Principal")

# Sidebar com dropdown para selecionar a aplicação
app_selecionada = st.sidebar.selectbox(
    "Selecione a aplicação:",
    ("Gerador de Ofertas", "Gerador de Números do Euromilhões"),
)

# Carregar a aplicação selecionada
if app_selecionada == "Gerador de Ofertas":
    run_ofertas()
elif app_selecionada == "Gerador de Números do Euromilhões":
    run_euromilhoes()
