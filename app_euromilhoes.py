import streamlit as st
import random

# Definir a configuração da página
title = "Gerador de Números do Euromilhões"
#st.set_page_config(page_title="Gerador de Números do Euromilhões", layout="wide")

# Função que gera os números do Euromilhões aleatoriamente
def gerar_numeros_aleatorios():
    numeros_principais = random.sample(range(1, 51), 5)  # Números principais
    estrelas = random.sample(range(1, 13), 2)  # Estrelas
    return sorted(numeros_principais), sorted(estrelas)

# Função que gera os números com base em maior probabilidade (simplificado)
def gerar_numeros_probabilidade():
    # Exemplo de números com maior chance (simplificado)
    numeros_frequentes = [1, 7, 10, 19, 23, 34, 38, 42, 46, 50]
    estrelas_frequentes = [2, 8, 10]
    numeros_principais = random.sample(numeros_frequentes, 5)
    estrelas = random.sample(estrelas_frequentes, 2)
    return sorted(numeros_principais), sorted(estrelas)

# Função para mostrar a interface da aplicação
def run():
    st.title("Gerador de Números do Euromilhões")

    # Opções de escolha para o usuário
    opcao = st.radio("Escolha uma opção", ("Gerar Números Aleatórios", "Gerar Números com Maior Probabilidade"))

    if opcao == "Gerar Números Aleatórios":
        if st.button("Gerar Números"):
            numeros, estrelas = gerar_numeros_aleatorios()
            st.subheader("Números Sorteados Aleatoriamente")
            st.write(f"Números principais: {numeros}")
            st.write(f"Estrelas: {estrelas}")
    
    elif opcao == "Gerar Números com Maior Probabilidade":
        if st.button("Gerar Números"):
            numeros, estrelas = gerar_numeros_probabilidade()
            st.subheader("Números Sorteados com Maior Probabilidade")
            st.write(f"Números principais: {numeros}")
            st.write(f"Estrelas: {estrelas}")

    # Link para os resultados oficiais do Euromilhões
    st.markdown("[Clique aqui para ver os resultados oficiais do Euromilhões](https://www.jogossantacasa.pt/web/SCCartazResult/euroMilhoes)")
    st.markdown("[Clique aqui para ver as estatisticas dos numeros mais sorteados do Euromilhões](https://www.jogossantacasa.pt/web/SCEstatisticas/)")
