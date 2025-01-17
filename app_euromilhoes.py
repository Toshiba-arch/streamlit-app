import requests
import streamlit as st

# API pública para resultados históricos do Euromilhões (substitua a URL com a API real que você encontrar)
api_url = "https://api.euro-millions.com/results"  # Exemplo de API pública, pode ser substituída por uma real

def obter_sorteios_reais():
    try:
        # Realiza a requisição para a API pública
        response = requests.get(api_url)
        
        # Verifica se a requisição foi bem-sucedida (status 200)
        response.raise_for_status()
        
        # Processa os dados da resposta (JSON)
        dados = response.json()
        
        # Mostra os 3 últimos sorteios (ajustar conforme a estrutura da API real)
        sorteios = []
        for sorteio in dados.get("resultados", [])[:3]:
            sorteios.append({
                "data": sorteio['data'],
                "pais": sorteio['pais'],
                "numeros": sorteio['numeros'],
                "premio": sorteio['premio']
            })
        
        return sorteios
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição da API: {e}")
        return None

# Função para gerar números aleatórios para o Euromilhões
def gerar_numeros_euromilhoes():
    import random
    # O Euromilhões tem 5 números de 1 a 50 e 2 estrelas de 1 a 12
    numeros = random.sample(range(1, 51), 5)
    estrelas = random.sample(range(1, 13), 2)
    return sorted(numeros), sorted(estrelas)

# Função principal para mostrar a interface Streamlit
def main():
    st.title("Gerador de Números e Resultados do Euromilhões")
    
    # Opção para mostrar os últimos sorteios ou gerar novos números
    escolha = st.radio("Escolha uma opção", ("Gerar Números Aleatórios", "Últimos Sorteios"))
    
    if escolha == "Gerar Números Aleatórios":
        st.subheader("Gerar Números Aleatórios para o Euromilhões")
        numeros, estrelas = gerar_numeros_euromilhoes()
        st.write(f"Números Sorteados: {numeros}")
        st.write(f"Estrelas Sorteadas: {estrelas}")
    
    elif escolha == "Últimos Sorteios":
        st.subheader("Últimos Sorteios do Euromilhões")
        sorteios = obter_sorteios_reais()
        if sorteios:
            for sorteio in sorteios:
                st.write(f"**Data**: {sorteio['data']}")
                st.write(f"**País de Atribuição**: {sorteio['pais']}")
                st.write(f"**Números Sorteados**: {', '.join(map(str, sorteio['numeros']))}")
                st.write(f"**Prêmio**: {sorteio['premio']}")
                st.write("---")
        else:
            st.error("Erro ao obter os últimos sorteios.")
    
if __name__ == "__main__":
    main()
