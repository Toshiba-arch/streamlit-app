import streamlit as st
import random
import requests

# Função para gerar números aleatórios do Euromilhões
def gerar_numeros_euromilhoes():
    # Gerar 5 números entre 1 e 50
    numeros = random.sample(range(1, 51), 5)
    # Gerar 2 estrelas entre 1 e 12
    estrelas = random.sample(range(1, 13), 2)
    
    return sorted(numeros), sorted(estrelas)

# Função para obter os últimos sorteios e detalhes através da API pública
def obter_ultimos_sorteios():
    url = "https://api.euro-millions.com/results"  # Substitua com a URL correta da API, se necessário
    params = {
        "country": "PT",  # Ou qualquer país de sua preferência
        "limit": 3,  # Limite de 3 sorteios mais recentes
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao obter os resultados dos sorteios!")
        return []

# Interface Streamlit para o Gerador de Números do Euromilhões
def run():
    st.title("Gerador de Números do Euromilhões")

    # Exibir os 3 últimos sorteios
    st.header("Últimos 3 Sorteios")
    sorteios = obter_ultimos_sorteios()
    
    if sorteios:
        for i, sorteio in enumerate(sorteios):
            st.subheader(f"Sorteio #{i+1}")
            numeros = sorteio['numbers']
            estrelas = sorteio['stars']
            premio = sorteio['prize']
            pais = sorteio['country']
            
            st.write(f"**Números sorteados:** {', '.join(map(str, numeros))}")
            st.write(f"**Estrelas sorteadas:** {', '.join(map(str, estrelas))}")
            st.write(f"**Prêmios Atribuídos:** €{premio}")
            st.write(f"**País do Sorteio:** {pais}")
            st.markdown("---")

    # Gerar novos números do Euromilhões
    st.header("Gerar Novos Números")
    if st.button("Gerar Números do Euromilhões"):
        numeros, estrelas = gerar_numeros_euromilhoes()
        st.write(f"**Números Gerados:** {', '.join(map(str, numeros))}")
        st.write(f"**Estrelas Geradas:** {', '.join(map(str, estrelas))}")
        
    st.markdown("""
    **Dica**: Se você estiver interessado em participar do Euromilhões, consulte sempre os resultados oficiais e certifique-se de jogar com responsabilidade.
    """)

# Chamar a função de execução
if __name__ == "__main__":
    run()
