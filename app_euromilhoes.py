import streamlit as st
import random
from collections import Counter
import requests

# Função para obter os últimos resultados (simulada aqui)
def obter_ultimos_resultados():
    # Simulação de resultados passados do Euromilhões
    resultados_passados = [
        {"numeros": [1, 7, 19, 23, 33], "estrelas": [5, 10]},
        {"numeros": [4, 9, 16, 28, 40], "estrelas": [1, 9]},
        {"numeros": [11, 14, 25, 30, 37], "estrelas": [3, 12]},
        {"numeros": [1, 5, 12, 21, 35], "estrelas": [2, 11]},
        {"numeros": [2, 8, 14, 27, 44], "estrelas": [4, 6]},
    ]
    return resultados_passados

# Função para calcular a frequência dos números e estrelas
def calcular_frequencia(resultados_passados):
    numeros = [num for resultado in resultados_passados for num in resultado["numeros"]]
    estrelas = [estrela for resultado in resultados_passados for estrela in resultado["estrelas"]]
    
    frequencia_numeros = Counter(numeros)
    frequencia_estrelas = Counter(estrelas)
    
    return frequencia_numeros, frequencia_estrelas

# Função para gerar os números baseados na frequência
def gerar_numeros_mais_frequentes(frequencia_numeros, frequencia_estrelas):
    numeros_frequentes = [num for num, _ in frequencia_numeros.most_common(5)]
    estrelas_frequentes = [estrela for estrela, _ in frequencia_estrelas.most_common(2)]
    
    return numeros_frequentes, estrelas_frequentes

# Função para gerar números aleatórios para o Euromilhões
def gerar_numeros_aleatorios():
    numeros_aleatorios = random.sample(range(1, 51), 5)  # 5 números de 1 a 50
    estrelas_aleatorias = random.sample(range(1, 13), 2)  # 2 estrelas de 1 a 12
    return sorted(numeros_aleatorios), sorted(estrelas_aleatorias)

# Interface Streamlit
st.title("Gerador de Números do Euromilhões")

menu = st.sidebar.selectbox("Escolha uma opção", ("Gerar Números Aleatórios", "Gerar Números Baseados em Frequência"))

# Exibir os resultados aleatórios ou baseados em frequência
if menu == "Gerar Números Aleatórios":
    if st.button("Gerar Números Aleatórios"):
        numeros, estrelas = gerar_numeros_aleatorios()
        st.subheader("Números Gerados Aleatoriamente")
        st.write(f"Números: {numeros}")
        st.write(f"Estrelas: {estrelas}")

elif menu == "Gerar Números Baseados em Frequência":
    # Obter os últimos resultados
    resultados_passados = obter_ultimos_resultados()
    
    # Calcular a frequência dos números e estrelas
    frequencia_numeros, frequencia_estrelas = calcular_frequencia(resultados_passados)
    
    if st.button("Gerar Números Baseados em Frequência"):
        numeros_frequentes, estrelas_frequentes = gerar_numeros_mais_frequentes(frequencia_numeros, frequencia_estrelas)
        st.subheader("Números Gerados Baseados em Frequência")
        st.write(f"Números Frequentes: {numeros_frequentes}")
        st.write(f"Estrelas Frequentes: {estrelas_frequentes}")
