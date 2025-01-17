import random
import streamlit as st

# Função para gerar números aleatórios do Euromilhões
def gerar_numeros_aleatorios():
    # O Euromilhões tem 5 números principais (1 a 50) e 2 estrelas (1 a 12)
    numeros_principais = random.sample(range(1, 51), 5)  # Números principais
    estrelas = random.sample(range(1, 13), 2)  # Estrelas

    return sorted(numeros_principais), sorted(estrelas)

# Função para gerar números com maior probabilidade de prêmio (exemplo simples)
def gerar_numeros_probabilidade():
    # Lista simplificada de números frequentemente sorteados
    numeros_frequentes = [1, 7, 10, 19, 23, 34, 38, 42, 46, 50]  # Exemplo de números mais frequentes
    estrelas_frequentes = [2, 8, 10]  # Exemplo de estrelas mais frequentes

    # Selecionando 5 números principais e 2 estrelas mais frequentes
    numeros_principais = random.sample(numeros_frequentes, 5)
    estrelas = random.sample(estrelas_frequentes, 2)

    return sorted(numeros_principais), sorted(estrelas)

# Função para exibir os últimos sorteios fictícios
def exibir_historico():
    # Sorteios fictícios para demonstração
    resultados_anteriores = [
        ([1, 5, 15, 24, 46], [2, 9]),
        ([8, 17, 21, 33, 49], [3, 11]),
        ([4, 7, 19, 27, 43], [1, 10])
    ]

    st.subheader("Últimos 3 Sorteios do Euromilhões")
    for sorteio in resultados_anteriores:
        numeros, estrelas = sorteio
        st.write(f"Números: {numeros}, Estrelas: {estrelas}")

# Função para fornecer o link para os resultados reais
def gerar_link_resultados():
    return "https://www.euro-millions.com/results"  # Link para resultados oficiais

# Interface do Streamlit
def app():
    st.title("Gerador de Números do Euromilhões")

    # Opção de escolher entre aleatório ou números com maior probabilidade
    opcao = st.radio("Escolha uma opção", ("Gerar Números Aleatórios", "Gerar Números com Maior Probabilidade"))

    if opcao == "Gerar Números Aleatórios":
        # Gerando números aleatórios
        numeros, estrelas = gerar_numeros_aleatorios()
        st.subheader("Números Sorteados Aleatoriamente")
        st.write(f"Números principais: {numeros}")
        st.write(f"Estrelas: {estrelas}")

    elif opcao == "Gerar Números com Maior Probabilidade":
        # Gerando números com maior probabilidade
        numeros, estrelas = gerar_numeros_probabilidade()
        st.subheader("Números Sorteados com Maior Probabilidade")
        st.write(f"Números principais: {numeros}")
        st.write(f"Estrelas: {estrelas}")

    # Exibindo o histórico de sorteios
    exibir_historico()

    # Link para os resultados oficiais
    st.markdown("[Clique aqui para ver os resultados oficiais do Euromilhões](https://www.euro-millions.com/results)")

if __name__ == "__main__":
    app()
