import streamlit as st
import random

# Lista de números mais frequentes (exemplo hipotético)
numeros_frequentes = [1, 7, 19, 23, 33, 44, 50]

# Função para gerar números aleatórios
def gerar_numeros_aleatorios():
    numeros = random.sample(range(1, 51), 5)  # Números principais entre 1 e 50
    estrelas = random.sample(range(1, 13), 2)  # Estrelas entre 1 e 12
    return numeros, estrelas

# Função para gerar números com base em critérios
def gerar_numeros_criterio(criterio='aleatorio'):
    if criterio == 'frequentes':
        # Se o critério for 'frequentes', retorna números mais frequentes (como exemplo)
        numeros = random.sample(numeros_frequentes, 5)  # Escolhe 5 números frequentes
    else:
        # Caso contrário, gera números aleatórios
        numeros, estrelas = gerar_numeros_aleatorios()
        return numeros, estrelas
    estrelas = random.sample(range(1, 13), 2)  # Estrelas entre 1 e 12
    return numeros, estrelas

# Função para a interface de geração de números
def run():
    st.title("Gerador de Números do Euromilhões")
    st.write("Gerar números aleatórios ou com base em critérios.")

    criterio = st.selectbox("Selecione o critério para gerar números", ['Aleatório', 'Mais Frequentes'])

    # Botão para gerar números
    if st.button("Gerar Números"):
        numeros, estrelas = gerar_numeros_criterio(criterio=criterio.lower())
        st.write(f"Números principais: {', '.join(map(str, numeros))}")
        st.write(f"Estrelas: {', '.join(map(str, estrelas))}")
