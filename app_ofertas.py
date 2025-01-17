import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Configuração da página (deve ser a primeira coisa)
st.set_page_config(page_title="Gerador de Conteúdo de Ofertas", layout="wide")

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

    # Texto sobre o desconto e preço
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
def gerar_post(produto, link_referencia):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']
    cupom = produto['cupom']

    post_texto = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!  
📉 Economize **{desconto}%**!  
"""

    if cupom:
        post_texto += f"💥 Use o código de cupom: **{cupom}** para mais descontos! \n"
    
    post_texto += f"👉 [Compre agora]({link_referencia})"
    
    return post_texto

# Função para gerar os links de compartilhamento para as redes sociais
def gerar_links_compartilhamento(post_texto, link_referencia, imagem_url):
    facebook_link = f"https://www.facebook.com/sharer/sharer.php?u={link_referencia}"
    twitter_link = f"https://twitter.com/intent/tweet?url={link_referencia}&text={post_texto}"
    linkedin_link = f"https://www.linkedin.com/shareArticle?mini=true&url={link_referencia}&title={post_texto}"
    whatsapp_link = f"https://wa.me/?text={post_texto} {link_referencia}"
    pinterest_link = f"https://www.pinterest.com/pin/create/button/?url={link_referencia}&media={imagem_url}&description={post_texto}"

    return facebook_link, twitter_link, linkedin_link, whatsapp_link, pinterest_link

# Função principal da app de ofertas
def run():
    st.title("Gerador de Conteúdo de Ofertas")

    nome_produto = st.text_input("Nome do Produto")
    tem_desconto = st.radio("O produto tem desconto?", ('Sim', 'Não'))

    if tem_desconto == 'Sim':
        desconto_percentual = st.number_input("Porcentagem de Desconto (%)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_original = preco_atual / (1 - desconto_percentual / 100)
    else:
        preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

    cupom = st.text_input("Código de Cupom (se houver)")
    imagem_url = st.text_input("Link da Imagem do Produto")
    link_referencia = st.text_input("Link de Afiliado")

    desconto = calcular_desconto(preco_original, preco_atual)

    if st.button("Gerar Post"):
        if nome_produto and link_referencia and preco_atual and imagem_url:
            produto = {
                "nome": nome_produto,
                "preco_original": preco_original,
                "preco_atual": preco_atual,
                "desconto": desconto,
                "imagem": imagem_url,
                "cupom": cupom
            }

            post_texto = gerar_post(produto, link_referencia)

            # Gerar e exibir o post
            imagem_com_texto = criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto, cupom)
            st.image(imagem_com_texto, caption=f"Oferta de {nome_produto}", use_container_width=True)

            st.text_area("Texto do Post para Compartilhar", post_texto, height=200)

            facebook_link, twitter_link, linkedin_link, whatsapp_link, pinterest_link = gerar_links_compartilhamento(post_texto, link_referencia, imagem_url)
            st.markdown(f"[Compartilhar no Facebook]({facebook_link})")
            st.markdown(f"[Compartilhar no Twitter]({twitter_link})")
            st.markdown(f"[Compartilhar no LinkedIn]({linkedin_link})")
            st.markdown(f"[Compartilhar no WhatsApp]({whatsapp_link})")
            st.markdown(f"[Compartilhar no Pinterest]({pinterest_link})")
