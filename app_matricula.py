import streamlit as st
import requests

def obter_informacoes_veiculo(matricula):
    # Simulação de resposta para futura implementação da API
    return {"erro": "API de matrícula ainda não disponível"}

def obter_dados_por_vin(vin):
    url = f"https://auto.dev/api/vin/{vin}"
    headers = {
        'Authorization': 'ZrQEPSkKdG9zaGliYS5zYWxhQGdtYWlsLmNvbQ=='
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"erro": f"Erro na consulta: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro na requisição: {e}"}

def exibir_dados_veiculo(dados):
    if "erro" in dados:
        st.error(dados["erro"])
        return
    
    st.subheader("Informações do Veículo")
    st.write(f"**Marca:** {dados.get('make', {}).get('name', 'N/A')}")
    st.write(f"**Modelo:** {dados.get('model', {}).get('name', 'N/A')}")
    st.write(f"**Ano:** {dados.get('years', [{}])[0].get('year', 'N/A')}")
    
    if "engine" in dados:
        st.subheader("Motor")
        engine = dados["engine"]
        st.write(f"**Tipo:** {engine.get('type', 'N/A')}")
        st.write(f"**Cilindros:** {engine.get('cylinder', 'N/A')}")
        st.write(f"**Tamanho:** {engine.get('size', 'N/A')} L")
        st.write(f"**Combustível:** {engine.get('fuelType', 'N/A')}")
    
    if "transmission" in dados:
        st.subheader("Transmissão")
        st.write(f"**Marchas:** {dados['transmission'].get('numberOfSpeeds', 'N/A')}")
    
    if "categories" in dados:
        st.subheader("Categorias")
        st.write(f"**Tipo:** {dados['categories'].get('vehicleType', 'N/A')}")
        st.write(f"**Estilo:** {dados['categories'].get('vehicleStyle', 'N/A')}")
    
    if "colors" in dados:
        st.subheader("Cores Disponíveis")
        for color in dados["colors"]:
            if color["category"] == "Exterior":
                cores = [option["name"] for option in color["options"]]
                st.write(", ".join(cores))
    
    if "options" in dados:
        st.subheader("Opções e Pacotes")
        for option in dados["options"]:
            st.write(f"**{option['category']}:**")
            for item in option["options"]:
                st.write(f"- {item['name']}")

def run():
    st.title("Consulta de Dados de Veículos")
    matricula = st.text_input("Digite a matrícula do veículo:")
    vin = st.text_input("Ou digite o VIN do veículo:")
    if st.button("Consultar"):
        if matricula:
            dados_matricula = obter_informacoes_veiculo(matricula)
            exibir_dados_veiculo(dados_matricula)
        elif vin:
            dados_vin = obter_dados_por_vin(vin)
            exibir_dados_veiculo(dados_vin)
        else:
            st.warning("Por favor, insira uma matrícula ou um VIN.")

if __name__ == "__main__":
    run()
