import streamlit as st
from app_ofertas import run as run_ofertas
from app_euromilhoes import run as run_euromilhoes

def main():
    # Personalizando a largura do menu lateral e título
    st.markdown(
        """
        <style>
        .css-1d391kg {width: 200px;}  # Ajuste a largura do menu lateral
        h1 {font-size: 24px;}          # Menor título principal
        .css-18e3th9 {font-size: 20px;} # Título em uma área específica
        </style>
        """, unsafe_allow_html=True)

    # Título da aplicação
    st.header("Selecione a Aplicação")

    # Dropdown para selecionar a aplicação
    app_selecionada = st.sidebar.selectbox(
        "Escolha a aplicação",
        ("App de Ofertas", "App de Euromilhões")
    )

    # Condicional para escolher qual aplicação executar
    if app_selecionada == "App de Ofertas":
        run_ofertas()
    elif app_selecionada == "App de Euromilhões":
        run_euromilhoes()

if __name__ == "__main__":
    main()
