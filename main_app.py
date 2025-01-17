import streamlit as st
from app_ofertas import run as run_ofertas
from app_euromilhoes import run as run_euromilhoes

# Função de execução principal para o menu de seleção
def main():
    st.title("Selecione a Aplicação")

    app_selecionada = st.sidebar.selectbox(
        "Escolha a aplicação",
        ("App de Ofertas", "App de Euromilhões")
    )

    if app_selecionada == "App de Ofertas":
        run_ofertas()
    elif app_selecionada == "App de Euromilhões":
        run_euromilhoes()

if __name__ == "__main__":
    main()
