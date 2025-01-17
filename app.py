import streamlit as st

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

    if desconto > 0:
        post = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!  
📉 Economize **{desconto}%**!  
👉 [Compre agora]({link_referencia})  
        """
    else:
        post = f"""📢 **Confira este produto!** 📢  
🔹 **{nome}**  
💰 Preço atual: **€{preco_atual:.2f}**!  
👉 [Compre agora]({link_referencia})  
        """
    return post

# Interface Streamlit
st.title("Gerador de Conteúdo com Ofertas da Amazon")
st.sidebar.header("Configurações")

# Passo 1: Inserir detalhes do produto manualmente
st.header("Adicionar detalhes do produto")
nome_produto = st.text_input("Nome do Produto")
preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

# Cálculo automático do desconto
desconto = calcular_desconto(preco_original, preco_atual)

# Passo 2: Gerar link com o Site Stripe
st.header("Gerar Link de Afiliado e Pré-Visualização")
st.markdown("Acesse o Site Stripe da Amazon enquanto navega no site da Amazon e copie o link de afiliado gerado.")
link_referencia = st.text_input("Cole aqui o Link de Afiliado gerado pelo Site Stripe")

# Exibir pré-visualização da imagem (se o link for válido)
if link_referencia:
    st.image(link_referencia, caption="Pré-visualização do Produto", use_column_width=True)

# Botão para gerar post
if st.button("Gerar Post"):
    if nome_produto and link_referencia:
        produto = {
            "nome": nome_produto,
            "preco_original": preco_original,
            "preco_atual": preco_atual,
            "desconto": desconto
        }
        post = criar_post(produto, link_referencia)
        st.subheader("Post Gerado")
        st.markdown(post, unsafe_allow_html=True)
    else:
        st.error("Por favor, insira todos os detalhes do produto e o link de afiliado.")
