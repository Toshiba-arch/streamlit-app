import streamlit as st

# Função para criar o post
def criar_post(produto, link_referencia):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_com_desconto = produto.get('preco_com_desconto', preco_original)
    desconto = produto.get('desconto', 0)

    post = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **€{preco_original:.2f}** por apenas **€{preco_com_desconto:.2f}**!  
📉 Economize **{desconto}%**!  
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
preco_com_desconto = st.number_input("Preço com Desconto (€)", min_value=0.0, step=0.01, format="%.2f")
desconto = st.number_input("Percentual de Desconto (%)", min_value=0, step=1)

# Passo 2: Gerar link com o Site Stripe
st.header("Gerar Link de Afiliado")
st.markdown("Acesse o Site Stripe da Amazon enquanto navega no site da Amazon e copie o link de afiliado gerado.")
link_referencia = st.text_input("Cole aqui o Link de Afiliado gerado pelo Site Stripe")

# Botão para gerar post
if st.button("Gerar Post"):
    if nome_produto and link_referencia:
        produto = {
            "nome": nome_produto,
            "preco_original": preco_original,
            "preco_com_desconto": preco_com_desconto,
            "desconto": desconto
        }
        post = criar_post(produto, link_referencia)
        st.subheader("Post Gerado")
        st.markdown(post, unsafe_allow_html=True)
    else:
        st.error("Por favor, insira todos os detalhes do produto e o link de afiliado.")
