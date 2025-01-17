import streamlit as st
from app_euromilhoes import run as run_euromilhoes
from app_ofertas import run as run_ofertas
from app_matricula import run as run_matricula  # Importando a nova app

# Título principal da app
st.title("App de Funcionalidades Diversas")

# Criar uma dropdown para selecionar a funcionalidade desejada
opcao = st.selectbox(
    "Selecione a funcionalidade",
    ["Gerador de Números do Euromilhões", "Consultor de Promoções", "Consulta de Marca do Carro pela Matrícula"]
)

# De acordo com a seleção, chamamos a função correspondente
if opcao == "Gerador de Números do Euromilhões":
    run_euromilhoes()
elif opcao == "Consultor de Promoções":
    run_ofertas()
elif opcao == "Consulta de Marca do Carro pela Matrícula":
    run_matricula()  # Chama a nova app para consulta de matrícula
