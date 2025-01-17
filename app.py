import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Função para calcular o desconto
def calcular_desconto(preco_original, preco_atual):
    if preco_original > preco_atual:
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    return 0

# Função para gerar imagem com texto sobre o produto
def criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto):
    # Carregar a imagem do produto
    response = requests.get(imagem_url)
    imagem = Image.open(BytesIO(response.content))
    
    # Adicionar o texto sobre a imagem
    draw = ImageDraw.Draw(imagem)
    font = ImageFont.load_default()
    
    # Definir texto de desconto
    texto_desconto = f"Desconto: {desconto}%"
    texto_valor = f"De €{preco_original:.2f} por €{preco_atual:.2f}"

    # Tamanho da imagem
    largura, altura = imagem.size

    # Posicionar o texto
    draw.text((10, altura - 50), texto_desconto, fill="white", font=font)
    draw.text((10, altura - 30), texto_valor, fill="white", font=font)

    return imagem

# Função para gerar o post com link
def gerar_post(produto, link_referencia):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']

    post_texto = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!  
📉 Economize **{desconto}%**!  
👉 [Compre agora]({link_referencia})  
"""
    return post_texto

# Interface Streamlit
st.title("Gerador de Conteúdo com Ofertas da Amazon")
st.sidebar.header("Configurações")

# Passo 1: Inserir apenas o nome do produto
st.header("Adicionar nome do produto")
nome_produto = st.text_input("Nome do Produto")

# Passo 2: Selecionar se o produto tem desconto
st.header("O produto tem desconto?")
tem_desconto = st.radio("Selecione a opção:", ('Sim', 'Não'))

# Passo 3: Inserir preços e desconto
if tem_desconto == 'Sim':
    st.header("Informar Desconto e Preço Atual")
    desconto_percentual = st.number_input("Porcentagem de Desconto (%)", min_value=0.0, step=0.01, format="%.2f")
    preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")
    preco_original = preco_atual / (1 - desconto_percentual / 100)  # Cálculo automático do preço original
else:
    st.header("Inserir preços do produto")
    preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
    preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

# Cálculo do desconto se o preço original e atual forem inseridos
desconto = 0
if preco_original > 0 and preco_atual < preco_original:
    desconto = calcular_desconto(preco_original, preco_atual)

# Passo 4: Inserir o link da imagem do produto
st.header("Inserir Link da Imagem do Produto")
imagem_url = st.text_input("Cole o URL da Imagem do Produto")

# Passo 5: Gerar link com o Site Stripe
st.header("Gerar Link de Afiliado")
st.markdown("Acesse o Site Stripe da Amazon enquanto navega no site da Amazon e copie o link de afiliado gerado.")
link_referencia = st.text_input("Cole aqui o Link de Afiliado gerado pelo Site Stripe")

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
        
        post_texto = gerar_post(produto, link_referencia)
        
        st.subheader("Post Gerado")
        
        # Exibir o link de afiliado com o preview do Facebook
        st.markdown(f"**Clique abaixo para compartilhar no Facebook com o preview da imagem**:")
        st.markdown(f"[Compartilhar no Facebook](https://www.facebook.com/sharer/sharer.php?u={link_referencia})")

        # Gerar a imagem com o texto sobreposto
        imagem_com_texto = criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto)
        
        # Exibir a imagem com o texto
        st.image(imagem_com_texto, caption="Imagem com Desconto", use_container_width=True)  # Atualizado

        # Exibir o texto do post gerado
        st.text_area("Copie o texto abaixo para compartilhar nas redes sociais", post_texto, height=200)

        st.markdown("""
        **Dica**: Ao copiar o texto gerado e colá-lo no **Facebook**, a imagem com o texto sobreposto será visualizada junto com o link clicável. 
        O **Facebook** irá gerar automaticamente o preview da imagem com o link, então você não precisa se preocupar em hospedar a imagem.
        """)
    else:
        st.error("Por favor, insira todos os detalhes do produto e o link de afiliado.")
