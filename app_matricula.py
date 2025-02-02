import streamlit as st
import requests

# Configuração da página
title = "Verificador de Matriculas"
#st.set_page_config(page_title="Verificador de Matriculas", layout="wide")

# Função para consultar o veículo pela matrícula
def obter_informacoes_veiculo(matricula):
    # Substitua pela URL da API que fornece dados de veículos com base na matrícula
    url = f"https://api.example.com/consultar_matricula/{matricula}"

    headers = {
        'Authorization': 'Bearer seu_token_aqui',  # Se necessário
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            return f"Erro na consulta: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {e}"

# Função para consultar dados do veículo pelo VIN
def obter_dados_por_vin(vin):
    # Substitua pela URL da API que fornece dados de veículos com base no VIN
    url = f"https://auto.dev/api/vin/(dados_vin)"

    headers = {
        'Authorization': 'ZrQEPSkKdG9zaGliYS5zYWxhQGdtYWlsLmNvbQ==',  # Se necessário
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            dados = response.json()
            return dados
        else:
            return f"Erro na consulta: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {e}"

# Função principal para a interface Streamlit
def run():
    st.title("Consulta de Dados de Veículos")

    # Input para matrícula
    matricula = st.text_input("Digite a matrícula do veículo (ex: 12-34-AB):")
    
    # Input para VIN
    vin = st.text_input("Ou digite o VIN do veículo:")

    if st.button("Consultar"):
        if matricula:
            dados_veiculo = obter_informacoes_veiculo(matricula)
            st.write(dados_veiculo)
        elif vin:
            dados_vin = obter_dados_por_vin(vin)
            st.write(dados_vin)
        else:
            st.write("Por favor, insira uma matrícula ou VIN.")

if __name__ == "__main__":
    run()
