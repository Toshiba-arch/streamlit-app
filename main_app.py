import streamlit as st
from app_euromilhoes import run as run_euromilhoes
from app_ofertas import run as run_ofertas
from app_matricula import run as run_matricula
from auto_post_app import auto_post_app as run_auto_post_app
from app_chatbot import run as run_chatbot  # Importando a funcionalidade do chatbot

# Título principal da app
st.title("App de Funcionalidades Diversas")

# Criar uma dropdown para selecionar a funcionalidade desejada
opcao = st.selectbox(
    "Selecione a funcionalidade",
    [
        "Chatbot Interativo",
        "Gerador de Números do Euromilhões",
        "Criação de Posts de Vendas - Basico",
        "Criação de Posts de Vendas",
        "Consulta de Marca do Carro pela Matrícula"
    ]
)

# De acordo com a seleção, chamamos a função correspondente
if opcao == "Chatbot Interativo":
    run_chatbot()
elif opcao == "Gerador de Números do Euromilhões":
    run_euromilhoes()
elif opcao == "Criação de Posts de Vendas - Basico":
    run_ofertas()
elif opcao == "Criação de Posts de Vendas":
    auto_post_app()
elif opcao == "Consulta de Marca do Carro pela Matrícula":
    run_matricula()
