import streamlit as st
import random

# Funções e código principal para o Gerador de Números do Euromilhões
def gerar_numeros_euromilhoes(qtd_estrelas, qtd_numeros):
    # Código relacionado ao gerador de números do Euromilhões
    # ...

st.title("Gerador de Números do Euromilhões")
st.sidebar.header("Menu")
st.sidebar.subheader("Gerar Números")

# Código relacionado à interface do gerador de números
# ...
import streamlit as st
import random

st.title("Gerador de Números do Euromilhões")

# Entrada de critérios
st.sidebar.header("Configurações")
quantidade = st.sidebar.slider("Quantidade de combinações a gerar", min_value=1, max_value=10, value=1)

# Critérios opcionais
st.sidebar.subheader("Configurações Avançadas")
usar_numeros_frequentes = st.sidebar.checkbox("Incluir números mais frequentes")
usar_estrelas_frequentes = st.sidebar.checkbox("Incluir estrelas mais frequentes")

# Números mais frequentes (exemplo fictício)
numeros_frequentes = [1, 2, 3, 4, 5]
estrelas_frequentes = [1, 2]

def gerar_numeros(usar_frequentes=False):
    if usar_frequentes:
        numeros = random.sample(numeros_frequentes, 5)
        estrelas = random.sample(estrelas_frequentes, 2)
    else:
        numeros = random.sample(range(1, 51), 5)
        estrelas = random.sample(range(1, 13), 2)
    return numeros, estrelas

# Gerar combinações
if st.button("Gerar Números"):
    for i in range(quantidade):
        numeros, estrelas = gerar_numeros(usar_frequentes=usar_numeros_frequentes or usar_estrelas_frequentes)
        st.write(f"Combinação {i+1}: Números: {sorted(numeros)} | Estrelas: {sorted(estrelas)}")
