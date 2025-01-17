import streamlit as st
from app_ofertas import run as run_ofertas
from app_euromilhoes import run as run_euromilhoes

# Função para o menu de navegação
def main():
    st.sidebar.title("Escolha a funcionalidade")
    
    # Dropdown com as opções
    opcao = st.sidebar.selectbox("Selecione a funcionalidade", ["Gerador de Ofertas", "Gerador de Números do Euromilhões"])

    if opcao == "Gerador de Ofertas":
        run_ofertas()  # Chama a funcionalidade de ofertas
    elif opcao == "Gerador de Números do Euromilhões":
        run_euromilhoes()  # Chama a funcionalidade de Euromilhões

if __name__ == "__main__":
    main()
