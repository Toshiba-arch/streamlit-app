import streamlit as st
from app_euromilhoes import run as run_euromilhoes
# Da mesma forma, você pode adicionar outras importações de aplicações se necessário, como:
# from app_ofertas import run as run_ofertas

# Função para exibir o menu de escolha e chamar a aplicação correta
def app():
    st.sidebar.title("Menu de Funcionalidades")
    opcao = st.sidebar.radio("Selecione uma aplicação", ("Euromilhões", "Outra Aplicação"))

    if opcao == "Euromilhões":
        run_euromilhoes()
    elif opcao == "Outra Aplicação":
        # Aqui você pode adicionar a lógica para chamar outras aplicações, se necessário
        st.title("Outra Aplicação")
        st.write("Aqui irá a lógica para outra funcionalidade.")

if __name__ == "__main__":
    app()
