import streamlit as st
import requests
from bs4 import BeautifulSoup

# Função para extrair o preço e a imagem usando o link de afiliado
def obter_dados_produto(link_referencia):
    try:
        # Fazer uma solicitação à página do produto
        response = requests.get(link_referencia)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extrair preço (Amazon pode alterar as classes, então isso pode precisar de ajuste)
        preco_original = soup.find("span", class_="a-price-whole")
        preco_atual = soup.find("span", class_="a-price-symbol")
        
        # Verificar se encontrou os dados corretamente
        if preco_original and preco_atual:
            preco_original = float(preco_original.get_text().replace(",", "."))
            preco_atual = float(preco_atual.get_text().replace(",", "."))
        else:
            preco_original = preco_atual = 0.0
        
        # Buscar imagem do produto
        imagem_produto = soup.find("img", id="imgTagWrapperId")
        if imagem_produto:
            imagem_url = imagem_produto.get("src")
        else:
            imagem_url = ""
        
        return preco_original, preco_atual, imagem_url
    except Exception as e:
        st.error(f"Erro ao tentar obter dados do produto: {str(e)}")
        return 0.0, 0.0, ""

# Função para calcular desconto
def calcular_desconto(preco_original, preco_atual):
    if preco_original > preco_atual:
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    return 0

# Função para criar o post
def criar_post(produto, link_referencia):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']
    imagem_url = produto['imagem']

    if desconto > 0:
        post = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!  
📉 Economize **{desconto}%**!  
![Imagem do Produto]({imagem_url})  
👉 [Compre agora]({link_referencia})  
        """
    else:
        post = f"""📢 **Confira este produto!** 📢  
🔹 **{nome}**  
💰 Preço atual: **€{preco_atual:.2f}**!  
![Imagem do Produto]({imagem_url})  
👉 [Compre agora]({link_referencia})  
        """
    return post

# Interface Streamlit
st.title("Gerador de Conteúdo com Ofertas da Amazon")
st.sidebar.header("Configurações")

# Passo 1: Inserir apenas o nome do produto
st.header("Adicionar nome do produto")
nome_produto = st.text_input("Nome do Produto")

# Passo 2: Gerar link com o Site Stripe
st.header("Gerar Link de Afiliado e Pré-Visualização")
st.markdown("Acesse o Site Stripe da Amazon enquanto navega no site da Amazon e copie o link de afiliado gerado.")
link_referencia = st.text_input("Cole aqui o Link de Afiliado gerado pelo Site Stripe")

# Obter dados do produto a partir do link
if link_referencia:
    preco_original, preco_atual, imagem_url = obter_dados_produto(link_referencia)
    if preco_original > 0 and preco_atual > 0:
        # Calcular o desconto
        desconto = calcular_desconto(preco_original, preco_atual)
        
        # Exibir a imagem do produto
        if imagem_url:
            st.image(imagem_url, caption="Imagem do Produto", use_column_width=True)
        
        produto = {
            "nome": nome_produto,
            "preco_original": preco_original,
            "preco_atual": preco_atual,
            "desconto": desconto,
            "imagem": imagem_url
        }
        
        # Gerar o post
        if st.button("Gerar Post"):
            post = criar_post(produto, link_referencia)
            st.subheader("Post Gerado")
            st.markdown(post, unsafe_allow_html=True)
    else:
        st.warning("Não foi possível obter dados do produto. Verifique o link e tente novamente.")
