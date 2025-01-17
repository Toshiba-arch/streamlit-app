import streamlit as st
from app_euromilhoes import run as run_euromilhoes
from app_ofertas import run as run_ofertas

# Função para exibir o menu de escolha e chamar a aplicação correta
def app():
    st.sidebar.title("Menu de Funcionalidades")
    opcao = st.sidebar.radio("Selecione uma aplicação", ("Euromilhões", "Promoções"))

    if opcao == "Euromilhões":
        run_euromilhoes()
    elif opcao == "Promoções":
        run_ofertas()

if __name__ == "__main__":
    app()
