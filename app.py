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
    # Carregar a imagem do produto
    response = requests.get(imagem_url)
    imagem = Image.open(BytesIO(response.content))
    
    # Usar a fonte padrão do PIL
    font = ImageFont.load_default()
    
    # Adicionar o texto sobre a imagem
    draw = ImageDraw.Draw(imagem)
    
    # Definir texto de desconto e cupom
    texto_desconto = f"Desconto: {desconto}%"
    texto_valor = f"De €{preco_original:.2f} por €{preco_atual:.2f}"
    
    if cupom:
        texto_cupom = f"Use o código: {cupom}!"
    else:
        texto_cupom = ""

    # Tamanho da imagem
    largura, altura = imagem.size

    # Posicionar o texto
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

    post_texto = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!  
📉 Economize **{desconto}%**!  
"""

    if cupom:
        post_texto += f"💥 Use o código de cupom: **{cupom}** para mais descontos! \n"
    
    post_texto += f"👉 [Compre agora]({link_referencia})"
    
    if tags:
        post_texto += f"\n\n# {' #'.join(tags)}"  # Adiciona as tags ao final

    return post_texto

# Função para gerar os links de compartilhamento para as redes sociais
def gerar_links_compartilhamento(post_texto, link_referencia, imagem_url):
    # Facebook
    facebook_link = f"https://www.facebook.com/sharer/sharer.php?u={link_referencia}"

    # Twitter
    twitter_link = f"https://twitter.com/intent/tweet?url={link_referencia}&text={post_texto}"

    # LinkedIn
    linkedin_link = f"https://www.linkedin.com/shareArticle?mini=true&url={link_referencia}&title={post_texto}"

    # WhatsApp
    whatsapp_link = f"https://wa.me/?text={post_texto} {link_referencia}"

    # Pinterest
    pinterest_link = f"https://www.pinterest.com/pin/create/button/?url={link_referencia}&media={imagem_url}&description={post_texto}"

    return facebook_link, twitter_link, linkedin_link, whatsapp_link, pinterest_link

# Interface Streamlit
st.title("Gerador de Conteúdo com Ofertas da Amazon")
st.sidebar.header("Configurações")

# Estilo CSS para reduzir o tamanho da fonte
st.markdown("""
    <style>
        .small-font input, .small-font textarea {
            font-size: 14px;
        }
        .small-font h3 {
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Passo 1: Inserir apenas o nome do produto
st.header("Adicionar nome do produto", anchor="nome_produto")
nome_produto = st.text_input("Nome do Produto", key="nome_produto", help="Insira o nome do produto", label_visibility="collapsed")

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

# Passo 4: Inserir código de cupom (se houver)
cupom = st.text_input("Código de Cupom (se houver)")

# Cálculo do desconto se o preço original e atual forem inseridos
desconto = 0
if preco_original > 0 and preco_atual < preco_original:
    desconto = calcular_desconto(preco_original, preco_atual)

# Passo 5: Inserir o link da imagem do produto
st.header("Inserir Link da Imagem do Produto")
imagem_url = st.text_input("Cole o URL da Imagem do Produto")

# Passo 6: Gerar link com o Site Stripe
st.header("Gerar Link de Afiliado")
st.markdown("Acesse o Site Stripe da Amazon enquanto navega no site da Amazon e copie o link de afiliado gerado.")
link_referencia = st.text_input("Cole aqui o Link de Afiliado gerado pelo Site Stripe")

# Passo 7: Inserir tags
st.header("Inserir Tags para o Post")
tags = st.text_input("Digite as tags separadas por vírgula (ex: oferta, desconto, produto, amazon)")

# Transformar as tags em uma lista
tags = [tag.strip() for tag in tags.split(',')] if tags else []

# Botão para gerar post
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
        
        post_texto = gerar_post(produto, link_referencia, tags)
        
        # Exibir a imagem com o texto sobreposto
        imagem_com_texto = criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto, cupom)
        
        # Gerar links de compartilhamento
        facebook_link, twitter_link, linkedin_link, whatsapp_link, pinterest_link = gerar_links_compartilhamento(post_texto, link_referencia, imagem_url)
        
        # Gerar o link para visualizar o post gerado em uma nova aba
        post_resultado_link = f"data:text/html,<html><body><h2>Post Gerado</h2><p>{post_texto}</p><img src='{imagem_com_texto}'/></body></html>"

        # Link para abrir em uma nova aba
        st.markdown(f"[Visualizar o Post Gerado em Nova Aba]({post_resultado_link})", unsafe_allow_html=True)

        # Mostrar o post gerado
        st.subheader("Post Gerado")
        st.text_area("Copie o texto abaixo para compartilhar nas redes sociais", post_texto, height=200)

        st.markdown("**Clique para Compartilhar nas Redes Sociais**:")
        st.markdown(f"[Compartilhar no Facebook]({facebook_link})")
        st.markdown(f"[Compartilhar no Twitter]({twitter_link})")
        st.markdown(f"[Compartilhar no LinkedIn]({linkedin_link})")
        st.markdown(f"[Compartilhar no WhatsApp]({whatsapp_link})")
        st.markdown(f"[Compartilhar no Pinterest]({pinterest_link})")
