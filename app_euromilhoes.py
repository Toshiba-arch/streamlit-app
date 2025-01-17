import streamlit as st
import random

def gerar_numeros_euromilhoes():
    numeros = random.sample(range(1, 51), 5)  # Números principais entre 1 e 50
    estrelas = random.sample(range(1, 13), 2)  # Estrelas entre 1 e 12
    return numeros, estrelas

# Função para a interface de geração de números
def run():
    st.title("Gerador de Números do Euromilhões")
    st.write("Gerar números aleatórios do Euromilhões.")

    # Botão para gerar números
    if st.button("Gerar Números"):
        numeros, estrelas = gerar_numeros_euromilhoes()
        st.write(f"Números principais: {', '.join(map(str, numeros))}")
        st.write(f"Estrelas: {', '.join(map(str, estrelas))}")
