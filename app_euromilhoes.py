import random
import streamlit as st

# Função para gerar números do Euromilhões com base em critérios
def gerar_numeros_euromilhoes():
    # Definindo o intervalo dos números para o Euromilhões
    numeros = random.sample(range(1, 51), 5)  # 5 números principais entre 1 e 50
    estrelas = random.sample(range(1, 13), 2)  # 2 estrelas entre 1 e 12
    return sorted(numeros), sorted(estrelas)

# Função principal da app Euromilhões
def run():
    st.title("Gerador de Números do Euromilhões")
    
    st.sidebar.header("Configurações do Gerador")

    if st.button("Gerar Números"):
        numeros, estrelas = gerar_numeros_euromilhoes()
        st.write(f"Números principais sorteados: {numeros}")
        st.write(f"Estrelas sorteadas: {estrelas}")
