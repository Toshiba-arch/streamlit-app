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
def criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto, cupom=None):
    response = requests.get(imagem_url)
    imagem = Image.open(BytesIO(response.content))

    draw = ImageDraw.Draw(imagem)
    font = ImageFont.load_default()

    texto_desconto = f"Desconto: {desconto}%"
    texto_valor = f"De €{preco_original:.2f} por €{preco_atual:.2f}"
    texto_cupom = f"Use o código: {cupom}" if cupom else ""

    largura, altura = imagem.size
    draw.text((10, altura - 50), texto_desconto, fill="white", font=font)
    draw.text((10, altura - 30), texto_valor, fill="white", font=font)
    if cupom:
        draw.text((10, altura - 10), texto_cupom, fill="white", font=font)

    return imagem

# Função para gerar o post com link
def gerar_post(produto, link_referencia, tags):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']
    cupom = produto['cupom']

    tags_str = ' '.join([f"#{tag}" for tag in tags])
    post_texto = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!  
📉 Economize **{desconto}%**!  
{tags_str}
"""

    if cupom:
        post_texto += f"💥 Use o código de cupom: **{cupom}** para mais descontos! \n"
    
    post_texto += f"👉 [Compre agora]({link_referencia})"
    return post_texto

# Interface Streamlit
st.title("Gerador de Post para Produtos")
st.sidebar.header("Configurações")

# Entrada de dados do usuário
nome_produto = st.text_input("Nome do Produto")
preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")
imagem_url = st.text_input("URL da Imagem do Produto")
link_referencia = st.text_input("Link de Afiliado")
tags = st.text_input("Tags (separadas por vírgula)").split(',')
cupom = st.text_input("Código de Cupom (opcional)")

desconto = calcular_desconto(preco_original, preco_atual)

if st.button("Gerar Post"):
    if nome_produto and link_referencia and preco_atual and imagem_url:
        produto = {
            "nome": nome_produto,
            "preco_original": preco_original,
            "preco_atual": preco_atual,
            "desconto": desconto,
            "cupom": cupom,
        }
        
        post_texto = gerar_post(produto, link_referencia, tags)
        imagem_com_texto = criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto, cupom)
        
        st.image(imagem_com_texto, caption=f"{nome_produto} - {texto_desconto}", use_container_width=True)
        st.text_area("Texto do Post", post_texto, height=200)
    else:
        st.error("Por favor, preencha todos os campos obrigatórios.")
