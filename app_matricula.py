import streamlit as st
import requests

# Função para consultar a API e obter as informações do carro
def obter_informacoes_veiculo(matricula):
    url = f"https://api.exemplo.com/consulta/{matricula}"  # URL fictícia, substitua pela API real
    headers = {"Authorization": "Bearer seu_token_aqui"}  # Substitua pelo seu token de autenticação, se necessário

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        dados_veiculo = response.json()
        return dados_veiculo
    else:
        return None

# Interface do Streamlit
def run():
    st.title("Consulta de Marca do Carro pela Matrícula")

    # Passo 1: Inserir a matrícula do veículo
    matricula = st.text_input("Insira a matrícula do veículo", "")

    # Passo 2: Botão para consultar
    if st.button("Consultar"):
        if matricula:
            # Chamar a função que consulta a API com a matrícula fornecida
            dados_veiculo = obter_informacoes_veiculo(matricula)
            
            if dados_veiculo:
                # Exibir as informações do veículo
                marca = dados_veiculo.get("marca", "Marca não encontrada")
                modelo = dados_veiculo.get("modelo", "Modelo não encontrado")
                ano = dados_veiculo.get("ano", "Ano não encontrado")
                
                st.subheader("Informações do Veículo:")
                st.write(f"**Marca:** {marca}")
                st.write(f"**Modelo:** {modelo}")
                st.write(f"**Ano:** {ano}")
            else:
                st.error("Não foi possível obter as informações do veículo. Verifique a matrícula.")
        else:
            st.warning("Por favor, insira uma matrícula para consultar.")
