import streamlit as st

# Função para calcular o desconto
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

# Passo 2: Inserir manualmente o preço atual
st.header("Inserir preço atual do produto")
preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

# Passo 3: Inserir manualmente o preço original (opcional)
st.header("Inserir preço original do produto (opcional)")
preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")

# Cálculo automático do desconto (caso o preço original seja fornecido)
desconto = 0
if preco_original > 0 and preco_atual < preco_original:
    desconto = calcular_desconto(preco_original, preco_atual)

# Passo 4: Inserir manualmente a imagem
st.header("Inserir Imagem do Produto")
imagem_url = st.text_input("Cole o URL da Imagem do Produto")

# Passo 5: Gerar link com o Site Stripe
st.header("Gerar Link de Afiliado")
st.markdown("Acesse o Site Stripe da Amazon enquanto navega no site da Amazon e copie o link de afiliado gerado.")
link_referencia = st.text_input("Cole aqui o Link de Afiliado gerado pelo Site Stripe")

# Exibir a imagem do produto (se o link for válido)
if imagem_url:
    st.image(imagem_url, caption="Imagem do Produto", use_container_width=True)  # Usando use_container_width

# Botão para gerar post
if st.button("Gerar Post"):
    if nome_produto and link_referencia and preco_atual and imagem_url:
        produto = {
            "nome": nome_produto,
            "preco_original": preco_original,
            "preco_atual": preco_atual,
            "desconto": desconto,
            "imagem": imagem_url
        }
        post = criar_post(produto, link_referencia)
        st.subheader("Post Gerado")
        st.markdown(post, unsafe_allow_html=True)
    else:
        st.error("Por favor, insira todos os detalhes do produto e o link de afiliado.")
