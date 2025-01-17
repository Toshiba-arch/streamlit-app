import streamlit as st
import requests

# Função para buscar produtos na API da Amazon
def buscar_produtos(amazon_api_key, amazon_api_secret, keywords):
    # Exemplo básico de estrutura para busca na Amazon API
    url = "https://api.amazon.com/advertising-api/v1/products"
    headers = {
        "Authorization": f"Bearer {amazon_api_key}",
        "Content-Type": "application/json"
    }
    params = {
        "keywords": keywords,
        "marketplace": "BR",
        "item_count": 10
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar produtos: " + str(response.status_code))
        return []

# Função para criar o post
def criar_post(produto, link_referencia):
    nome = produto['title']
    preco_original = produto['price']['amount']
    preco_com_desconto = produto.get('discounted_price', preco_original)
    desconto = produto.get('discount_percent', 0)

    post = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **R${preco_original}** por apenas **R${preco_com_desconto}**!  
📉 Economize **{desconto}%**!  
👉 [Compre agora]({link_referencia})  
    """
    return post

# Interface Streamlit
st.title("Gerador de Conteúdo com Ofertas da Amazon")
st.sidebar.header("Configurações")

# Configurações do usuário
amazon_api_key = st.sidebar.text_input("API Key da Amazon", type="password")
amazon_api_secret = st.sidebar.text_input("API Secret da Amazon", type="password")
keywords = st.text_input("Palavra-chave para busca (ex: smartphone)")

# Botão de busca
if st.button("Buscar Ofertas"):
    if not amazon_api_key or not amazon_api_secret:
        st.error("Por favor, insira as credenciais da API da Amazon.")
    else:
        produtos = buscar_produtos(amazon_api_key, amazon_api_secret, keywords)
        if produtos:
            st.success(f"Foram encontrados {len(produtos)} produtos!")
            for produto in produtos:
                link_referencia = f"https://www.amazon.com/dp/{produto['asin']}?tag=seu_id_de_associado"
                post = criar_post(produto, link_referencia)
                st.markdown(post, unsafe_allow_html=True)
        else:
            st.warning("Nenhum produto encontrado.")
