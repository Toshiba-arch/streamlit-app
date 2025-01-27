import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib.parse

def extrair_dados_produto(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        nome = soup.find('span', {'id': 'productTitle'}).text.strip() if soup.find('span', {'id': 'productTitle'}) else "Produto Desconhecido"
        preco_original = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip() if soup.find('span', {'id': 'priceblock_ourprice'}) else "0.00"
        preco_atual = soup.find('span', {'id': 'priceblock_dealprice'}).text.strip() if soup.find('span', {'id': 'priceblock_dealprice'}) else preco_original

        return {
            "nome": nome,
            "preco_original": preco_original,
            "preco_atual": preco_atual,
        }
    except Exception as e:
        st.error(f"Erro ao acessar a página: {e}")
        return None

def calcular_desconto(preco_original, preco_atual):
    try:
        preco_original = float(preco_original.replace("€", "").replace(",", "."))
        preco_atual = float(preco_atual.replace("€", "").replace(",", "."))
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    except Exception:
        return 0

def gerar_post(produto, link_referencia):
    desconto = calcular_desconto(produto['preco_original'], produto['preco_atual'])
    post_texto = f"📢 **Oferta Imperdível!** 📢\n"
    post_texto += f"🔹 **{produto['nome']}**\n"
    post_texto += f"💰 Antes **€{produto['preco_original']}** AGORA **€{produto['preco_atual']}**!\n"
    post_texto += f"📉 Poupa já **{desconto}%**!\n"
    post_texto += f"👉 [Compra agora]({link_referencia})\n"
    
    return post_texto

def auto_post_app():
    st.title("Gerador Automático de Posts")

    url_input = st.text_input("Insira o link de referência para gerar o post automaticamente:")

    if st.button("Validar Link"):
        with st.spinner("Validando o link e carregando os dados do produto..."):
            produto = extrair_dados_produto(url_input)
            if produto:
                st.session_state.produto = produto
                st.session_state.produto_validado = True
                st.success("Produto validado com sucesso!")
            else:
                st.error("Não foi possível validar o produto.")

    if st.session_state.get("produto_validado", False):
        produto = st.session_state.produto
        post_texto = gerar_post(produto, url_input)

        st.write("### Pré-visualização do Post:")
        st.text_area("Texto do Post:", post_texto, height=200)

        # Botão para download do post
        st.download_button("Baixar Post (.txt)", data=post_texto, file_name="post_gerado.txt")

# Executando a aplicação
if __name__ == "__main__":
    auto_post_app()
