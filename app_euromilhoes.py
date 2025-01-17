import random
import streamlit as st

# Função para gerar números do Euromilhões (aleatórios)
def gerar_numeros_aleatorios():
    # O Euromilhões é composto por 5 números principais e 2 estrelas
    numeros_principais = random.sample(range(1, 51), 5)  # Números principais (1 a 50)
    estrelas = random.sample(range(1, 13), 2)  # Estrelas (1 a 12)

    return sorted(numeros_principais), sorted(estrelas)

# Função para gerar números com maior probabilidade de prêmio (simplificado)
def gerar_numeros_probabilidade():
    # Exemplo simples de probabilidade: números mais frequentes
    # Listamos os números que foram mais sorteados em sorteios passados
    # Esta lista pode ser atualizada conforme os sorteios.
    numeros_frequentes = [1, 7, 10, 19, 23, 34, 38, 42, 46, 50]  # Exemplos de números mais sorteados
    estrelas_frequentes = [2, 8, 10]  # Exemplos de estrelas mais frequentes

    # Selecionamos 5 números principais e 2 estrelas das listas de números frequentes
    numeros_principais = random.sample(numeros_frequentes, 5)
    estrelas = random.sample(estrelas_frequentes, 2)

    return sorted(numeros_principais), sorted(estrelas)

# Função para exibir o histórico de resultados (últimos 3 sorteios fictícios)
def exibir_historico():
    # Para fins de exemplo, vamos apenas exibir as 3 últimas combinações (estas são fictícias)
    # Você pode modificar para puxar os resultados de uma fonte real (site ou API).
    resultados_anteriores = [
        ([1, 5, 15, 24, 46], [2, 9]),  # Resultado fictício 1
        ([8, 17, 21, 33, 49], [3, 11]),  # Resultado fictício 2
        ([4, 7, 19, 27, 43], [1, 10])   # Resultado fictício 3
    ]

    st.subheader("Últimos 3 Sorteios do Euromilhões")
    for sorteio in resultados_anteriores:
        numeros, estrelas = sorteio
        st.write(f"Números: {numeros}, Estrelas: {estrelas}")

# Função para gerar o link para o último sorteio
def gerar_link_resultados():
    return "https://www.euro-millions.com/results"  # Link para o site oficial dos resultados do Euromilhões

# Interface Streamlit
def app():
    st.title("Gerador de Números do Euromilhões")

    # Opção para escolher entre gerar números aleatórios ou com maior probabilidade
    opcao = st.radio("Escolha uma opção", ("Gerar Números Aleatórios", "Gerar Números com Maior Probabilidade"))

    if opcao == "Gerar Números Aleatórios":
        # Gerar números aleatórios
        numeros, estrelas = gerar_numeros_aleatorios()
        st.subheader("Números Sorteados Aleatoriamente")
        st.write(f"Números principais: {numeros}")
        st.write(f"Estrelas: {estrelas}")

    elif opcao == "Gerar Números com Maior Probabilidade":
        # Gerar números com maior probabilidade
        numeros, estrelas = gerar_numeros_probabilidade()
        st.subheader("Números Sorteados com Maior Probabilidade")
        st.write(f"Números principais: {numeros}")
        st.write(f"Estrelas: {estrelas}")
    
    # Mostrar histórico dos últimos sorteios
    exibir_historico()

    # Link para resultados oficiais
    st.markdown("[Clique aqui para ver os resultados oficiais do Euromilhões](https://www.euro-millions.com/results)")

if __name__ == "__main__":
    app()
