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
    
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(imagem)
    
    texto_desconto = f"Desconto: {desconto}%"
    texto_valor = f"De €{preco_original:.2f} por €{preco_atual:.2f}"
    texto_cupom = f"Use o código: {cupom}" if cupom else ""

    largura, altura = imagem.size
    draw.text((10, altura - 100), texto_desconto, fill="white", font=font)
    draw.text((10, altura - 70), texto_valor, fill="white", font=font)
    if cupom:
        draw.text((10, altura - 40), texto_cupom, fill="white", font=font)

    return imagem

# Função para gerar o post com link
def gerar_post(produto, link_referencia, tags):
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
    if tags:
        post_texto += "\n\n" + " ".join([f"#{tag.strip()}" for tag in tags])

    return post_texto

# Função para gerar os links de compartilhamento para as redes sociais
def gerar_links_compartilhamento(post_texto, link_referencia, imagem_url):
    facebook_link = f"https://www.facebook.com/sharer/sharer.php?u={link_referencia}"
    twitter_link = f"https://twitter.com/intent/tweet?url={link_referencia}&text={post_texto}"
    linkedin_link = f"https://www.linkedin.com/shareArticle?mini=true&url={link_referencia}&title={post_texto}"
    whatsapp_link = f"https://wa.me/?text={post_texto} {link_referencia}"
    pinterest_link = f"https://www.pinterest.com/pin/create/button/?url={link_referencia}&media={imagem_url}&description={post_texto}"

    return facebook_link, twitter_link, linkedin_link, whatsapp_link, pinterest_link

# Header com navegação
st.set_page_config(page_title="App de Ofertas", layout="wide")

st.markdown("<h1 style='text-align: center;'>App de Ofertas e Funcionalidades</h1>", unsafe_allow_html=True)
st.sidebar.title("Menu")

# Menu de navegação
opcao = st.sidebar.radio("Escolha uma funcionalidade", ["Gerar Post de Oferta", "Outra Funcionalidade"])

if opcao == "Gerar Post de Oferta":
    st.subheader("Gerar Post de Oferta")
    # Passo 1: Nome do Produto
    nome_produto = st.text_input("Nome do Produto")
    
    # Passo 2: Produto com desconto
    tem_desconto = st.radio("O produto tem desconto?", ["Sim", "Não"])
    if tem_desconto == "Sim":
        desconto_percentual = st.number_input("Porcentagem de Desconto (%)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_original = preco_atual / (1 - desconto_percentual / 100)
    else:
        preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

    cupom = st.text_input("Código de Cupom (se houver)")
    desconto = calcular_desconto(preco_original, preco_atual)
    imagem_url = st.text_input("URL da Imagem do Produto")
    link_referencia = st.text_input("Link de Afiliado")
    tags = st.text_input("Insira tags separadas por vírgula (ex: #amazon, #oferta)")

    if st.button("Gerar Post"):
        if nome_produto and preco_atual > 0 and link_referencia and imagem_url:
            produto = {
                "nome": nome_produto,
                "preco_original": preco_original,
                "preco_atual": preco_atual,
                "desconto": desconto,
                "imagem": imagem_url,
                "cupom": cupom
            }
            post_texto = gerar_post(produto, link_referencia, tags.split(","))
            imagem_com_texto = criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto, cupom)
            
            legenda_imagem = f"**{nome_produto}** - Desconto: {desconto}%"
            st.image(imagem_com_texto, caption=legenda_imagem, use_container_width=True)
            st.text_area("Post Gerado:", post_texto, height=200)

            links = gerar_links_compartilhamento(post_texto, link_referencia, imagem_url)
            st.markdown("**Compartilhe nas Redes Sociais:**")
            st.markdown(f"[Facebook]({links[0]}) | [Twitter]({links[1]}) | [LinkedIn]({links[2]}) | [WhatsApp]({links[3]}) | [Pinterest]({links[4]})")
        else:
            st.error("Preencha todas as informações para gerar o post.")

elif opcao == "Outra Funcionalidade":
    st.subheader("Nova Funcionalidade em Desenvolvimento")
    st.write("Aqui você pode adicionar futuras funcionalidades.")
